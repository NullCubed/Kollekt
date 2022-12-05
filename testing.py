import pytest
from kollekt import db
from flask_login import current_user


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


def test_login_page(client):
    response = client.get("/login")
    assert b'<h5 class="text-center">Dont have an account? Register now</h5>' in response.data

def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b'<legend class="border-bottom mb-4 text-center">Sign Up</legend>' in response.data


def test_logged_out_homepage(client):
    response = client.get("/")
    assert b"""<h3 class="text-center" style="font-weight: bold">
          Log in to have a personalized experience
        </h3>""" in response.data


def test_logged_in_homepage(app, client):
    db.drop_all()
    db.create_all()
    response = client.post("/register", data={
        "username": "admin1",
        "email": "joe1@joe.com",
        "password": "goodpassword",
        "confirm_password": "goodpassword"}, follow_redirects=True)
    # print(response.data).
    assert response.request.path == "/"
    login = client.post("/login", data={
        "username": "admin1",
        "password": "goodpassword"}, follow_redirects=True)
    print(str(login.data))
    assert b"""<h4 class="text-center border-bottom pb-2">
            Top Communities / Recent Posts

          </h4>""" in login.data
    # Check that there was one redirect response.
    # assert len(response.history) == 1
    # Check that the second request was to the index page.



def test_register_new_user(client):
    db.drop_all()
    db.create_all()
    with client:
        response = client.post("/register", data=dict(
            username="admin",
            email='joe@joe.com',
            password="goodpassword",
            confirm_password="goodpassword"), follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'


def test_register_existing_user(client):
    with client:
        response = client.post("/register", data={
            'username': 'admin',
            'email': 'joe@joe.com',
            'password': 'goodpassword',
            'confirm_password': 'goodpassword'
        }, follow_redirects=True)
    assert response.request.path == '/register'


def test_login_existing_user(client):
    response = client.post("/login", data=dict(
        username="admin",
        password="goodpassword", ), follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/'




def test_login_nonexisting_user(client):
    response = client.post('/login', data={
        'username': 'alphabetsoup',
        'password': 'goodpassword'
    }, follow_redirects=True)
    assert response.request.path == '/login'




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
        "email": "test@test.com",
        "password": "goodpassword",
        "confirm_password": "goodpassword"}, follow_redirects=True)
    assert response.request.path == '/register'


def test_long_password_register(client):
    response = client.post("/register", data={
        "username": "goodusername",
        "email": "test@test.com",
        "password": "thispasswordiswaytoolong",
        "confirm_password": "thispasswordiswaytoolong"}, follow_redirects=True)
    assert response.request.path == '/register'


def test_long_password_confirm(client):
    response = client.post("/register", data={
        "username": "goodusername",
        "email": "test@test.com",
        "password": "goodpassword",
        "confirm_password": "goodpassword22"}, follow_redirects=True)
    assert response.request.path == '/register'


def test_insane_input(client):
    response = client.post("/register", data={
        "username": "goodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusername",
        "email": "goodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusernamegoodusername@test.com",
        "password": "goodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpassword",
        "confirm_password": "goodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpasswordgoodpassword"}, follow_redirects=True)
    assert response.request.path == '/register'

def test_create_collection(client):
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    resposne = client.post ("/login", data={"username": "Admin", "password": "testing"})

    response = client.post("/collections/create/1", data={"name": "test", "desc": "test"}, follow_redirects=True)
    assert response.request.path == "/"
    response = client.get("/collections/view/3")
    assert b"""test""" in response.data


def test_community_tab(client):
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    resposne = client.post ("/login", data={"username": "Admin", "password": "testing"})
    response = client.get("/")
    print(response.data)
    assert b"""
                Watches""" in response.data

def test_good_email_update(client):
    response = client.post("/settings", data={
        "username": "tested",
        "email": "test2@gmail.com",
        "bio": "test",
        "profile_picture": "lion"}, follow_redirects=True)
    assert response.request.path == '/settings'

def test_update_existing_user(client):
    with client:
        response = client.post("/settings", data={
        "username": "tested",
        "email": "test2@gmail.com",
        "bio": "test"}, follow_redirects=True)
    assert response.request.path == '/settings'

def test_bad_email_update(client):
    response = client.post("/settings", data={
        "username": "test2",
        "email": "test",
        "bio": "test"}, follow_redirects=True)
    assert response.request.path == '/settings'

def test_blank_email_update(client):
    response = client.post("/settings", data={
        "username": "test3",
        "email": "   @    .   ",
        "bio": "test"}, follow_redirects=True)
    assert response.request.path == '/settings'

def test_update_long_username(client):
    with client:
        response = client.post("/settings", data={
        "username": "testtesttesttesttesttesttesttesttesttest",
        "email": "test2@gmail.com",
        "bio": "test"}, follow_redirects=True)
    assert response.request.path == '/settings'



def test_update_good_user(client):
    db.drop_all()
    db.create_all()
    with client:
        response = client.post("/settings", data=dict(
            username="tester",
            email='testing@test.com',
            bio="my bio"), follow_redirects=True)
        response2 = client.get("/settings")
        
        assert response.data == response2.data


def test_create_item(client):
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    resposne = client.post("/login", data={"username": "Admin", "password": "testing"})
    response = client.post("/addItem/1", data={
        "text": "test text", "photo": "3c8db28eeebc196d17988ec05c3cf059.jpg", "name": "name"}, follow_redirects=True)
    assert response.request.path == '/item'

def test_upload_item_image(client):
    #Test #6, checks for status code of 200, then checks for image in html
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    response = client.post("/login", data={"username": "Admin", "password": "testing"})
    response = client.post("/addItem/1", data={
        "text": "test text", "photo": "bantest.jpg", "name": "901239012309120931390"}, follow_redirects=True)
    assert response.status_code == 200
    assert b'bantest.jpg!' in response.data

def test_upload_item(client):
    #Test #3, checks for status code of 200, then checks for flashed message
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    response = client.post("/login", data={"username": "Admin", "password": "testing"})
    response = client.post("/addItem/1", data={
        "text": "test text", "photo": "bantest.jpg", "name": "901239012309120931390"}, follow_redirects=True)
    print(response.status_code)
    assert response.status_code == 200
    assert b'IMAGE UPLOADED!' in response.data

def test_communites_in_profile(client):
    # 73 tests to ensure the user can see their communities/collections from their
    # profile page
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    response = client.get('/userProfile')
    assert b'Shoes' in response.data

def test_items_on_profile_page(client):
    # 47 tests to see if new items are showing on profile page
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    response = client.post("/login", data={"username": "Admin", "password": "testing"})
    response = client.post("/addItem/1", data={
        "text": "test text", "photo": "bantest.jpg", "name": "901239012309120931390"}, follow_redirects=True)
    response = client.post('/userProfile')
    assert b'901239012309120931390' in response.data

def test_items_in_collections(client):
    # 46 tests to see if items are showing up in the correct collection
    db.drop_all()
    db.create_all()
    response = client.get("/fillDB")
    response = client.post("/login", data={"username": "Admin", "password": "testing"})
    response = client.post("/addItem/2", data={
        "text": "test text", "photo": "bantest.jpg", "name": "901239012309120931390"}, follow_redirects=True)
    response = client.post('/collections/view/2')
    assert b'901239012309120931390' in response.data