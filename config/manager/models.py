
from django.db import models
from django.core.validators import MinValueValidator

class SchoolClass(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Subject(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="students"
    )
    name = models.CharField(max_length=120)
    roll_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} ({self.school_class})"

    class Meta:
        ordering = ["name"]
        unique_together = [("school_class", "name")]


class Test(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="tests"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    test_date = models.DateField(null=True, blank=True)
    total_marks = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.school_class} - {self.subject} - {self.name}"


class Mark(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="marks"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="marks"
    )
    score = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )
    is_absent = models.BooleanField(default=False)

    class Meta:
        unique_together = [("test", "student")]
        ordering = ["student__name"]
  
