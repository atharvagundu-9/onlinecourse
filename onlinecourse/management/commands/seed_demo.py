import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from onlinecourse.models import (
    Choice,
    Course,
    Enrollment,
    Instructor,
    Learner,
    Lesson,
    Question,
    Submission,
)


class Command(BaseCommand):
    help = "Create deterministic demo data for the final-project screenshots."

    def handle(self, *args, **options):
        User = get_user_model()
        admin_username = os.environ.get("DEMO_ADMIN_USERNAME", "admin")
        admin_password = os.environ.get("DEMO_ADMIN_PASSWORD", "CourseDemo!2026")
        learner_username = os.environ.get("DEMO_LEARNER_USERNAME", "learner")
        learner_password = os.environ.get("DEMO_LEARNER_PASSWORD", "LearnDjango!2026")

        admin_user, _ = User.objects.get_or_create(username=admin_username)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.first_name = "Course"
        admin_user.last_name = "Administrator"
        admin_user.set_password(admin_password)
        admin_user.save()

        learner_user, _ = User.objects.get_or_create(username=learner_username)
        learner_user.first_name = "Avery"
        learner_user.last_name = "Learner"
        learner_user.set_password(learner_password)
        learner_user.save()

        instructor, _ = Instructor.objects.update_or_create(
            user=admin_user,
            defaults={"full_time": True, "total_learners": 1240},
        )
        Learner.objects.update_or_create(
            user=learner_user,
            defaults={
                "occupation": Learner.DEVELOPER,
                "social_link": "https://example.com/avery",
            },
        )

        course, _ = Course.objects.update_or_create(
            name="Django Web Application Development",
            defaults={
                "description": (
                    "Build database-backed web applications with Django models, "
                    "views, templates, authentication, and Bootstrap."
                ),
                "image": "course_images/django-course.svg",
                "total_enrollment": 1240,
            },
        )
        course.instructors.set([instructor])

        lesson_one, _ = Lesson.objects.update_or_create(
            course=course,
            order=0,
            defaults={
                "title": "Django models and the ORM",
                "content": (
                    "Model relational data with Python classes and use migrations "
                    "to keep the database schema synchronized."
                ),
            },
        )
        lesson_two, _ = Lesson.objects.update_or_create(
            course=course,
            order=1,
            defaults={
                "title": "Views, templates, and forms",
                "content": (
                    "Connect URL routes to views, render dynamic templates, and "
                    "process secure POST requests."
                ),
            },
        )

        question_specs = [
            (
                course,
                "Which Django component maps Python classes to database tables?",
                3,
                [("The Object-Relational Mapper (ORM)", True), ("The template engine", False), ("The URL dispatcher", False)],
            ),
            (
                course,
                "Which practices help protect a Django POST form? Select all that apply.",
                4,
                [("Include a CSRF token", True), ("Validate submitted data on the server", True), ("Trust hidden fields without validation", False)],
            ),
            (
                course,
                "What does a Django view return for a normal web response?",
                3,
                [("An HttpResponse object", True), ("A database migration", False), ("A settings module", False)],
            ),
        ]

        questions = []
        for question_course, text, grade, choice_specs in question_specs:
            question, _ = Question.objects.update_or_create(
                course=question_course,
                question_text=text,
                defaults={"grade": grade},
            )
            questions.append(question)
            Choice.objects.filter(question=question).delete()
            Choice.objects.bulk_create(
                [
                    Choice(
                        question=question,
                        choice_text=choice_text,
                        is_correct=is_correct,
                    )
                    for choice_text, is_correct in choice_specs
                ]
            )

        enrollment, _ = Enrollment.objects.update_or_create(
            user=learner_user,
            course=course,
            defaults={"mode": Enrollment.HONOR, "rating": 5.0},
        )
        enrollment.submissions.all().delete()
        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.set(
            Choice.objects.filter(question__in=questions, is_correct=True)
        )

        self.stdout.write(self.style.SUCCESS("Demo project data is ready."))
        self.stdout.write(f"Admin: {admin_username} / {admin_password}")
        self.stdout.write(f"Learner: {learner_username} / {learner_password}")
        self.stdout.write(
            f"Result URL: /onlinecourse/course/{course.id}/submission/{submission.id}/result/"
        )
