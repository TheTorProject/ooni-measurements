import os
import pytest

import flask

# Setup logging before doing anything with the Flask app
# See README.adoc

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(relativeCreated)6d %(levelname).1s %(filename)s:%(lineno)s %(message)s",
)

from measurements.app import create_app


def pytest_collection_modifyitems(items):
    for item in items:
        module_dir = os.path.dirname(item.location[0])
        if module_dir.endswith("functional"):
            item.add_marker(pytest.mark.functional)
        elif module_dir.endswith("unit"):
            item.add_marker(pytest.mark.unit)


@pytest.fixture
def app():
    app = create_app(testmode=True)
    app.debug = True
    assert app.logger.handlers == []
    return app


@pytest.yield_fixture
def client(app):
    """
    Overriding the `client` fixture from pytest_flask to fix this bug:
    https://github.com/pytest-dev/pytest-flask/issues/42
    """
    with app.test_client() as client:
        yield client

    while True:
        top = flask._request_ctx_stack.top
        if top is not None and top.preserved:
            top.pop()
        else:
            break
