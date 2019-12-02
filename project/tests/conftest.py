# project/tests/test_config.py
"""Testing configuration happens here.
"""

import pytest

from project import create_app, db


@pytest.fixture(scope="module")
def test_app():
    """Test-fixture. All testing will happen in 'app'
    """
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_database():
    """Test-fixture for database
    """
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
