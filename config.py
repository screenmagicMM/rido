import logging
import logging.config
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'rido.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}

g_logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)
