from decimal import Decimal, InvalidOperation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Max, Min
from .models import SchoolClass, Subject, Student, Test, Mark
from .forms import LoginForm, ClassForm, SubjectForm, StudentForm, TestForm

def login_view(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["pin"])
        if user is not None and user.is_active:
            login(request, user); return redirect("dashboard")
        messages.error(request, "Username ya PIN galat hai.")
    return render(request, "manager/login.html", {"form": form})

def logout_view(request):
    logout(request); return redirect("login")

@login_required
def dashboard(request):
    context = {
        "class_count": SchoolClass.objects.count(), "student_count": Student.objects.count(),
        "test_count": Test.objects.count(), "classes": SchoolClass.objects.all(),
        "tests": Test.objects.select_related("school_class","subject")[:12],
    }
    return render(request, "manager/dashboard.html", context)

@login_required
def classes_view(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid(): form.save(); messages.success(request, "Class added.")
    form = ClassForm()
    return render(request, "manager/manage.html", {"title":"Manage Classes","form":form,"items":SchoolClass.objects.all(),"kind":"classes"})

@login_required
def subjects_view(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid(): form.save(); messages.success(request, "Subject added.")
    return render(request, "manager/manage.html", {"title":"Manage Subjects","form":SubjectForm(),"items":Subject.objects.all(),"kind":"subjects"})

@login_required
def students_view(request):
    if request.method == "POST":
        if request.POST.get("bulk_names"):
            cls = get_object_or_404(SchoolClass, pk=request.POST.get("bulk_class"))
            names = [x.strip() for x in request.POST["bulk_names"].splitlines() if x.strip()]
            for name in names: Student.objects.get_or_create(school_class=cls, name=name)
            messages.success(request, f"{len(names)} student names processed.")
        else:
            form = StudentForm(request.POST)
            if form.is_valid(): form.save(); messages.success(request, "Student added.")
    return render(request, "manager/students.html", {"form":StudentForm(),"students":Student.objects.select_related("school_class"),"classes":SchoolClass.objects.all()})

@login_required
def tests_view(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid(): form.save(); messages.success(request, "Test created.")
    return render(request, "manager/tests.html", {"form":TestForm(),"tests":Test.objects.select_related("school_class","subject")})

@login_required
def marks_view(request, test_id):
    test = get_object_or_404(Test.objects.select_related("school_class","subject"), pk=test_id)
    students = test.school_class.students.all()
    if request.method == "POST":
        for student in students:
            raw = request.POST.get(f"score_{student.id}", "").strip()
            absent = request.POST.get(f"absent_{student.id}") == "on"
            score = None
            if raw:
                try: score = Decimal(raw)
                except InvalidOperation: continue
                if score < 0 or score > test.total_marks: continue
            Mark.objects.update_or_create(test=test, student=student, defaults={"score":None if absent else score,"is_absent":absent})
        messages.success(request, "Marks saved.")
        return redirect("marks", test_id=test.id)
    existing = {m.student_id:m for m in test.marks.all()}
    rows = [{"student":s,"mark":existing.get(s.id)} for s in students]
    stats = test.marks.filter(score__isnull=False).aggregate(avg=Avg("score"), high=Max("score"), low=Min("score"))
    return render(request, "manager/marks.html", {"test":test,"rows":rows,"stats":stats})

@login_required
def results_view(request):
    cls_id = request.GET.get("class")
    subject_id = request.GET.get("subject")
    classes = SchoolClass.objects.all()
    selected_class = classes.filter(pk=cls_id).first() if cls_id else classes.first()
    tests = Test.objects.filter(school_class=selected_class).select_related("subject") if selected_class else Test.objects.none()
    if subject_id: tests = tests.filter(subject_id=subject_id)
    students = selected_class.students.all() if selected_class else Student.objects.none()
    results=[]
    for student in students:
        earned=Decimal("0"); possible=0; cells=[]
        for test in tests:
            mark=Mark.objects.filter(test=test,student=student).first()
            cells.append(mark)
            if mark and mark.score is not None: earned += mark.score; possible += test.total_marks
        results.append({"student":student,"cells":cells,"earned":earned,"possible":possible,"percent":(earned/possible*100) if possible else None})
    results.sort(key=lambda x: x["percent"] or Decimal("-1"), reverse=True)
    for i,row in enumerate(results,1): row["rank"]=i if row["possible"] else "—"
    return render(request,"manager/results.html",{"classes":classes,"subjects":Subject.objects.all(),"tests":tests,"results":results,"selected_class":selected_class,"selected_subject":subject_id})
