import pytest
from kollekt import db


@pytest.fixture(scope='module')
def app(request):
    from kollekt import create_app
    return create_app()


@pytest.fixture(autouse=True)
def app_context(app):
    """Creates a flask app context"""
    with app.app_context():
        app.config['WTF_CSRF_ENABLED'] = False
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
    assert b"""<h3 class="text-center" style="font-weight: bold">
          Log in to have a personalized experience
        </h3>""" in response.data


def test_register_new_user(client):
    db.drop_all()
    db.create_all()
    with client:
        response = client.post("/register", data=dict(
            username="admin",
            email='joe@joe.com',
            password="admin",
            confirm_password="admin"), follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'


def test_register_existing_user(client):
    with client:
        response = client.post("/register", data={
            'username': 'admin',
            'email': 'joe@joe.com',
            'password': 'admin',
            'confirm_password': 'admin'
        }, follow_redirects=True)
    assert response.request.path == '/register'


def test_login_existing_user(client):
    response = client.post("/login", data=dict(
        username="admin",
        password="admin", ), follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/'


def test_login_nonexisting_user(client):
    response = client.post('/login', data={
        'username': 'alphabetsoup',
        'password': 'areallystrongpassword'
    }, follow_redirects=True)
    assert response.request.path == '/login'


def test_logged_in_homepage(app, client):
    db.drop_all()
    db.create_all()
    response = client.post("/register", data={
        "username": "admin1",
        "email": "joe1@joe.com",
        "password": "admin",
        "confirm_password": "admin"}, follow_redirects=True)
    # print(response.data).
    assert response.status_code == 200
    # Check that there was one redirect response.
    # assert len(response.history) == 1
    # Check that the second request was to the index page.
    assert response.request.path == "/"


def test_logout(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/"


def test_bad_email_register(client):
    response = client.post("/register", data={
        "username": "test",
        "email": "test",
        "password": "test",
        "confirm_password": "test"}, follow_redirects=True)
    assert response.request.path == '/register'


def test_bad_username_register(client):
    response = client.post("/register", data={
        "username": "a",
        "email": "test",
        "password": "test",
        "confirm_password": "test"}, follow_redirects=True)
    assert response.request.path == '/register'
