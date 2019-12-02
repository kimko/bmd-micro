# project/config_custom.py
"""Manage additional application configuration
"""


class BaseConfig:
    """Base configuration"""

    LOGGER = {
        "version": 1,
        "formatters": {
            "default": {"format": "[%(asctime)s] in %(module)s: %(message)s"}
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    pass


class TestingConfig(BaseConfig):
    """Testing configuration"""

    pass


class ProductionConfig(BaseConfig):
    """Production configuration"""

    pass
