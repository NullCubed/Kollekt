import pytest
from kollekt import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_login(client):
    response = client.get("/login")
    assert b'<h5 class="text-center">Dont have an account? Register now</h5>' in response.data




def test_logged_out_homepage(client):

    response = client.get("/home")
    assert b"Kollek" in response.data
