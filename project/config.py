# project/config.py


class BaseConfig:
    """Base configuration"""

    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    pass


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""

    pass


class LoggerConfig:
    from logging.config import dictConfig
    dictConfig({
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    })
