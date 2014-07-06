import hashlib
import os
import logging
import uuid

import pytest

from pywik import Pywik

logging.basicConfig(level=logging.DEBUG)


def random_string():
    return uuid.uuid4().get_hex()[0:16]


@pytest.fixture(scope='session')
def client():
    return Pywik(os.environ['PYWIK_API_URL'], os.environ['PYWIK_TOKEN_AUTH'])


@pytest.yield_fixture(scope='session')
def user(client):
    user_login = 'testuser-{}'.format(random_string())
    print client.users_manager.add_user(user_login, 'password', '{}@example.com'.format(user_login))
    yield user_login
    print client.users_manager.delete_user(user_login)


@pytest.yield_fixture(scope='session')
def site(client):
    site_name = 'testsite-{}'.format(random_string())
    site_id = client.sites_manager.add_site(site_name, ['http://example.com', 'http://blah.com'])
    yield site_id
    print client.sites_manager.delete_site(site_id)


class TestUsersManager(object):
    def test_set_access(self, client, user, site):
        # Need an empty test to force setup/teardown to run once.
        print self.users_manager.set_user_access(user, 'view', [site])

    def test_get_token_auth(self, user):
        hashed_password = hashlib.md5('password').hexdigest()
        print self.users_manager.get_token_auth(user, hashed_password)


class TestSitesManager(object):
    def test_empty(self, site):
        pass
