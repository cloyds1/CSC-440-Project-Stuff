import pytest
from UserDBInstance import UserDBInstance

#User object tests
#==============================================================================#
@pytest.fixture
def user():
    yield UserDBInstance.User("cloyds1")

def test_user(user):
    new_user1 = UserDBInstance.User("cloyds1")
    new_user2 = UserDBInstance.User("Username")

    assert user == new_user1
    assert not user == new_user2

#Database object tests
#==============================================================================#
@pytest.fixture
def db():
    yield UserDBInstance(db_path="users.db", auto_commits="True")

def test_add(db, user):
    db.add(user)
    assert db.get(user).identifier == "cloyds1"
    
def test_get(db, user):
    assert db.get(user).identifier == "cloyds1"
    
def test_edit(db, user):
    user.password = "hello world"
    db.edit(user)
    assert db.get(user).password == "hello world"

def test_delete(db, user):
    db.delete(user)
    assert not db.exists(UserDBInstance.User("cloyds1"))

def test_exists(db, user):
    db.add(user)
    assert db.exists(user)

    db.delete(UserDBInstance.User("cloyds1"))
    assert not db.exists(user)

    
