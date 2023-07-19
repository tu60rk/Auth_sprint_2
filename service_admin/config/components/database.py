import os

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('FILM_POSTGRES_DB'),
        'USER': os.environ.get('FILM_POSTGRES_USER'),
        'PASSWORD': os.environ.get('FILM_POSTGRES_PASSWORD'),
        'HOST' : os.environ.get('FILM_POSTGRES_HOST', 'db'),
        'PORT' : os.environ.get('FILM_POSTGRES_PORT'),
        'OPTIONS' : {
            # Нужно явно указать схему, с которыми будет работать приложение
            'options': '-c search_path=public,content'
        }
    }
}
