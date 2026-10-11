# OnlineCourse assessment project

This is a completed version of IBM's Django final-project starter. It adds a
multi-question course assessment, persistent submissions, score evaluation,
Bootstrap-based exam and result pages, Django admin editing, tests, and a
repeatable demo-data command.

## Run locally

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open `http://127.0.0.1:8000/onlinecourse/`.

The demo command creates local-only credentials for screenshot generation:

- Admin: `admin` / `CourseDemo!2026`
- Learner: `learner` / `LearnDjango!2026`

Override them with `DEMO_ADMIN_USERNAME`, `DEMO_ADMIN_PASSWORD`,
`DEMO_LEARNER_USERNAME`, and `DEMO_LEARNER_PASSWORD` environment variables.

## Verify

```text
python manage.py check
python manage.py test
```

## Submission checklist

- `onlinecourse/models.py`: `Question`, `Choice`, and `Submission`
- `onlinecourse/admin.py`: seven model imports and the required inline/admin classes
- `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
- `onlinecourse/views.py`: `submit` and `show_exam_result`
- `onlinecourse/urls.py`: routes for both assessment views
- `03-admin-site.png`: Django admin sections
- `07-final.png`: successful mock-exam result

The starter source is maintained by the
[IBM Developer Skills Network](https://github.com/ibm-developer-skills-network/final-cloud-app-with-database).
