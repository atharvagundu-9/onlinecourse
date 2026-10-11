from django.contrib import admin
from .models import Choice, Course, Instructor, Learner, Lesson, Question, Submission


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "order"]
    list_filter = ["course"]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ["question_text", "course", "grade"]
    list_filter = ["course"]
    search_fields = ["question_text"]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["id", "learner", "course", "submitted_at"]
    list_filter = ["enrollment__course", "submitted_at"]
    filter_horizontal = ["choices"]

    @admin.display(description="Learner")
    def learner(self, obj):
        return obj.enrollment.user.username

    @admin.display(description="Course")
    def course(self, obj):
        return obj.enrollment.course.name


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
