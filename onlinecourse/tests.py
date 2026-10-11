from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .admin import LessonAdmin, QuestionAdmin
from .models import Choice, Course, Enrollment, Lesson, Question, Submission


class AssessmentFeatureTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="learner",
            password="test-password",
        )
        self.course = Course.objects.create(
            name="Django Essentials",
            description="Learn Django by building an online course application.",
            image="course_images/django.png",
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Models and views",
            order=0,
            content="Connect persistent models to request handlers.",
        )
        self.question = Question.objects.create(
            course=self.course,
            question_text="Which statements describe Django?",
            grade=5,
        )
        self.correct_one = Choice.objects.create(
            question=self.question,
            choice_text="It is a Python web framework.",
            is_correct=True,
        )
        self.correct_two = Choice.objects.create(
            question=self.question,
            choice_text="It includes an ORM.",
            is_correct=True,
        )
        self.incorrect = Choice.objects.create(
            question=self.question,
            choice_text="It is a database engine.",
            is_correct=False,
        )
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course,
            mode=Enrollment.HONOR,
        )

    def test_question_requires_exact_correct_choice_set(self):
        self.assertTrue(
            self.question.is_get_score([self.correct_one.id, self.correct_two.id])
        )
        self.assertFalse(self.question.is_get_score([self.correct_one.id]))
        self.assertFalse(
            self.question.is_get_score(
                [self.correct_one.id, self.correct_two.id, self.incorrect.id]
            )
        )

    def test_course_page_displays_questions_and_choices_for_enrolled_user(self):
        self.client.login(username="learner", password="test-password")
        response = self.client.get(
            reverse("onlinecourse:course_details", args=[self.course.id])
        )

        self.assertContains(response, self.course.name)
        self.assertContains(response, self.lesson.title)
        self.assertContains(response, self.question.question_text)
        self.assertContains(response, self.correct_one.choice_text)

    def test_submit_creates_submission_and_redirects_to_result(self):
        self.client.login(username="learner", password="test-password")
        response = self.client.post(
            reverse("onlinecourse:submit", args=[self.course.id]),
            {
                f"choice_{self.correct_one.id}": str(self.correct_one.id),
                f"choice_{self.correct_two.id}": str(self.correct_two.id),
            },
        )

        submission = Submission.objects.get(enrollment=self.enrollment)
        self.assertRedirects(
            response,
            reverse(
                "onlinecourse:show_exam_result",
                args=[self.course.id, submission.id],
            ),
        )
        self.assertEqual(submission.grade_percent(), 100)

    def test_result_page_shows_success_message_score_and_results(self):
        submission = Submission.objects.create(enrollment=self.enrollment)
        submission.choices.set([self.correct_one, self.correct_two])
        self.client.login(username="learner", password="test-password")

        response = self.client.get(
            reverse(
                "onlinecourse:show_exam_result",
                args=[self.course.id, submission.id],
            )
        )

        self.assertContains(response, "Congratulations!")
        self.assertContains(response, "Score: 100%")
        self.assertContains(response, "Exam results")

    def test_submission_ignores_choice_from_another_course(self):
        other_course = Course.objects.create(
            name="Other course",
            description="Not part of this exam.",
            image="course_images/other.png",
        )
        other_lesson = Lesson.objects.create(
            course=other_course,
            title="Other lesson",
            content="Other content",
        )
        other_question = Question.objects.create(
            course=other_course,
            question_text="Other question",
        )
        other_choice = Choice.objects.create(
            question=other_question,
            choice_text="Injected answer",
            is_correct=True,
        )
        self.client.login(username="learner", password="test-password")

        self.client.post(
            reverse("onlinecourse:submit", args=[self.course.id]),
            {
                f"choice_{self.correct_one.id}": str(self.correct_one.id),
                f"choice_{other_choice.id}": str(other_choice.id),
            },
        )

        submission = Submission.objects.get(enrollment=self.enrollment)
        self.assertNotIn(other_choice, submission.choices.all())

    def test_admin_configuration_is_registered(self):
        self.assertIsInstance(admin.site._registry[Lesson], LessonAdmin)
        self.assertIsInstance(admin.site._registry[Question], QuestionAdmin)
        self.assertIn(Choice, admin.site._registry)
        self.assertIn(Submission, admin.site._registry)
