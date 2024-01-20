import pytest
from app.models import User, Status

@pytest.fixture(scope='module')
def user_fixture():
    user = User(username='testuser')
    user.set_password('testpassword')
    return user

@pytest.fixture(scope='module')
def status_fixture(user_fixture):
    status = Status(content='Test status', author=user_fixture)
    return status

class TestUserModel:

    def test_create_user(self, user_fixture):
        assert user_fixture.username == 'testuser'
        assert user_fixture.check_password('testpassword')

    def test_retrieve_user(self, user_fixture):
        retrieved_user = User.query.filter_by(username='testuser').first()
        assert retrieved_user is not None
        assert retrieved_user.username == 'testuser'

    def test_update_user(self, user_fixture):
        user_fixture.username = 'updateduser'
        assert user_fixture.username == 'updateduser'

    def test_delete_user(self, user_fixture):
        User.query.filter_by(username='testuser').delete()
        retrieved_user = User.query.filter_by(username='testuser').first()
        assert retrieved_user is None


class TestStatusModel:

    def test_create_status(self, status_fixture):
        assert status_fixture.content == 'Test status'

    def test_retrieve_status(self, status_fixture):
        retrieved_status = Status.query.filter_by(content='Test status').first()
        assert retrieved_status is not None
        assert retrieved_status.content == 'Test status'

    def test_update_status(self, status_fixture):
        status_fixture.content = 'Updated status'
        assert status_fixture.content == 'Updated status'

    def test_delete_status(self, status_fixture):
        Status.query.filter_by(content='Test status').delete()
        retrieved_status = Status.query.filter_by(content='Test status').first()
        assert retrieved_status is None

def test_helper_function():
    # Add any additional test cases for helper methods in the models, if applicable
    pass