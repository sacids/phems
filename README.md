# Django BoilerPlate

Built using [Python](https://www.python.org/) and 
[Django Framework](https://www.djangoproject.com/)

## Installation
Clone Repository

```bash
https://github.com/sacids/django-boilerplate.git
cd django-boilerplate
```

To set up a development environment quickly, first install Python 3. It comes with virtualenv built-in. So create a virtual env by:

```bash
python -m virtualenv env
env/bin/activate
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

Update database settings (poe/settings.py)
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Detailed instructions
Take a look at the docs for more information.