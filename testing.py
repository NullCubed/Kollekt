import pytest

@pytest.fixture(scope='module')
def app(request):
    from kollekt import create_app
    return create_app()


@pytest.fixture(autouse=True)
def app_context(app):
    """Creates a flask app context"""
    with app.app_context():
        yield app


@pytest.fixture
def client(app_context):
    return app_context.test_client(use_cookies=True)


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_login(client):
    response = client.get("/login")
    assert b'<h5 class="text-center">Dont have an account? Register now</h5>' in response.data




def test_logged_out_homepage(client):

    response = client.get("/")
    assert b"Kollekt" in response.data
