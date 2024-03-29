from os import environ
import yaml

from designer.settings.base import *
from designer.settings.utils import get_env_setting, get_logger_config


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

LOGGING = get_logger_config()

# Keep track of the names of settings that represent dicts. Instead of overriding the values in base.py,
# the values read from disk should UPDATE the pre-configured dicts.
DICT_UPDATE_KEYS = ('JWT_AUTH',)

MEDIA_STORAGE_BACKEND = {}

CONFIG_FILE = get_env_setting('DESIGNER_CFG')
with open(CONFIG_FILE, encoding='utf-8') as f:
    config_from_yaml = yaml.load(f, Loader=yaml.FullLoader)

    # Remove the items that should be used to update dicts, and apply them separately rather
    # than pumping them into the local vars.
    dict_updates = {key: config_from_yaml.pop(key, None) for key in DICT_UPDATE_KEYS}

    for key, value in list(dict_updates.items()):
        if value:
            vars()[key].update(value)

    vars().update(config_from_yaml)

    # Load the files storage backend settings for django storages
    vars().update(MEDIA_STORAGE_BACKEND)

DB_OVERRIDES = dict(
    PASSWORD=environ.get('DB_MIGRATION_PASS', DATABASES['default']['PASSWORD']),
    ENGINE=environ.get('DB_MIGRATION_ENGINE', DATABASES['default']['ENGINE']),
    USER=environ.get('DB_MIGRATION_USER', DATABASES['default']['USER']),
    NAME=environ.get('DB_MIGRATION_NAME', DATABASES['default']['NAME']),
    HOST=environ.get('DB_MIGRATION_HOST', DATABASES['default']['HOST']),
    PORT=environ.get('DB_MIGRATION_PORT', DATABASES['default']['PORT']),
)

for override, value in DB_OVERRIDES.items():
    DATABASES['default'][override] = value
