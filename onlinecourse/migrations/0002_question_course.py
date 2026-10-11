from django.db import migrations, models
import django.db.models.deletion


def copy_question_courses(apps, schema_editor):
    Question = apps.get_model("onlinecourse", "Question")
    for question in Question.objects.select_related("lesson__course").iterator():
        question.course_id = question.lesson.course_id
        question.save(update_fields=["course"])


class Migration(migrations.Migration):

    dependencies = [
        ("onlinecourse", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="onlinecourse.course",
            ),
        ),
        migrations.RunPython(copy_question_courses, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="question",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="onlinecourse.course",
            ),
        ),
        migrations.RemoveField(
            model_name="question",
            name="lesson",
        ),
    ]
