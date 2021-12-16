# Django Todo API

This is a simple todo API allowing authenticated users to create tasks & tasklists.
Made with [django-rest-framework](https://www.django-rest-framework.org/), [drf_spectacular](https://drf-spectacular.readthedocs.io/) and [dj-rest-auth](https://dj-rest-auth.readthedocs.io/).

## Deploy locally

To try it out, just run the following commands :

```bash
git clone git@github.com:gerthi/djangoAPI.git
cd djangoAPI

# install the requirements
pip install -r requirements.txt

# migrate the database
python manage.py makemigrations
python manage.py migrate

# run the server
python manage.py runserver
```

Open your browser and visit [localhost:8080](http://127.0.0.1:8080/) !

## Usage

The following endpoints are available to authenticated users :

- `/tasks/` read, create, edit, delete tasks
- `/tasklists/` read, create, edit, delete tasklists
- `/docs/` view a complete swagger API documentation
- `/auth/` login & logout

## Creating users

You can either create users in the CLI by running `python manage.py createsuperuser` or through the [Djangon admin interface](http://127.0.0.1:8000/admin/).
