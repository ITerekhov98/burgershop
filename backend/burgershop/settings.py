import os

import dj_database_url
import rollbar
from environs import Env
from pathlib import Path

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['127.0.0.1', 'localhost'])

INSTALLED_APPS = [
    'burgershop.apps.products.apps.ProductsConfig',
    'burgershop.apps.restaurants.apps.RestaurantsConfig',
    'burgershop.apps.orders.apps.OrdersConfig',
    'burgershop.apps.restaurateur.apps.RestaurateurConfig',
    'burgershop.apps.geolocation.apps.GeolocationConfig',
    'burgershop.apps.main.apps.MainConfig',
    'admin_shortcuts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rangefilter',
    'phonenumber_field',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
]

ROOT_URLCONF = 'burgershop.urls'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('burgershop', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'custom_tags':'burgershop.apps.restaurateur.template_tags.custom_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'burgershop.wsgi.application'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

POSTGRES_DB = env.str('POSTGRES_DB')
POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')

DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}", 
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

INTERNAL_IPS = [
    '127.0.0.1'
]


STATICFILES_DIRS = [
    BASE_DIR.joinpath('burgershop', 'assets'),
    BASE_DIR.joinpath('bundles'),
]

YANDEX_API_TOKEN = env.str('YANDEX_API_TOKEN', '')

# ROLLBAR = {
#     'access_token': env.str('ROLLBAR_TOKEN'),
#     'environment': env.str('ROLLBAR_ENVIRONMENT', 'development'),
#     'root': BASE_DIR,
# }

# rollbar.init(**ROLLBAR)


ADMIN_SHORTCUTS_SETTINGS = {
'show_on_all_pages': False,
'hide_app_list': False,
'open_new_window': False,
}

ADMIN_SHORTCUTS = [
    {
        'title': 'Рестораны',
        'shortcuts': [
            {
                'title': 'Рестораны',
                'url_name': 'admin:restaurants_restaurant_changelist',
            }
        ]
    },
    {
        'title': 'Меню',
        'shortcuts': [
            {
                'title': 'Продукты',
                'url_name': 'admin:products_product_changelist',
            },
            {
                'title': 'Категории',
                'url_name': 'admin:products_productcategory_changelist',
            }
        ]
    },
    {
        'title': 'Заказы',
        'shortcuts': [
            {
                'title': 'Заказы',
                'url_name': 'admin:orders_order_changelist',
            }
        ]
    }
]