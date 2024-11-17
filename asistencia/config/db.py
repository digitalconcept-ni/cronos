import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# psycopg2

LOCAL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cronos',
        'USER': 'postgres',
        'PASSWORD': '00Dascher',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SERVER = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cronos',
        'USER': 'postgres',
        'PASSWORD': '#H0!@psql*',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
