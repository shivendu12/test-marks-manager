from django.contrib import admin
from .models import SchoolClass, Subject, Student, Test, Mark

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    search_fields = ["name"]
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ["name"]
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "school_class", "roll_number"]
    list_filter = ["school_class"]
    search_fields = ["name", "roll_number"]
class MarkInline(admin.TabularInline):
    model = Mark
    extra = 0
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ["name", "school_class", "subject", "test_date", "total_marks"]
    list_filter = ["school_class", "subject"]
    inlines = [MarkInline]
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ["student", "test", "score", "is_absent"]
    list_filter = ["test__school_class", "test__subject"]
    search_fields = ["student__name"]
