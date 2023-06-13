from dotenv import load_dotenv

from config.settings.base import *  # noqa

DEBUG = True

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(zkzx^ewo7=6^nd)qxv11%4s2nf=h1!873%i^hdfn^@=f(0775"

ALLOWED_HOSTS = []

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432:5432",
        }
    }
else:
    DATABASES = {
        "default_local": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("POSTGRESQL_NAME"),
            "USER": os.environ.get("POSTGRESQL_USER"),
            "PASSWORD": os.environ.get("POSTGRESQL_PASSWORD"),
            "HOST": os.environ.get("POSTGRESQL_HOST"),
            "PORT": os.environ.get("POSTGRESQL_PORT"),
        },
        "default_sqlite": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT"),
        }
    }

STATIC_URL = "static/"
