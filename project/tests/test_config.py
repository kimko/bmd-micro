# project/tests/test_config.py


def test_development_config(test_app):
    test_app.config.from_object("project.config.DevelopmentConfig")
    assert not test_app.config["TESTING"]


def test_testing_config(test_app):
    test_app.config.from_object("project.config.TestingConfig")
    assert test_app.config["TESTING"]
    assert not test_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
