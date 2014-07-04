import logging
import os
import uuid

from pywik import Pywik

log = logging.getLogger(__name__)


class BaseTest(object):
    c = Pywik(os.environ['PYWIK_API_URL'], os.environ['PYWIK_TOKEN_AUTH'])

    @classmethod
    def random_string(cls):
        return uuid.uuid4().get_hex()[0:16]


class TestUsersManager(BaseTest):
    @classmethod
    def setup(cls):
        cls.manager = cls.c.user_manager
        cls.user_login = 'testuser-{}'.format(cls.random_string())
        log.debug(cls.manager.add_user(cls.user_login, 'password', '{}@example.com'.format(cls.user_login)))

    @classmethod
    def teardown_class(cls):
        log.debug(cls.manager.delete_user(cls.user_login))

    def test_empty(self):
        # Need an empty tst to force setup/teardown to run once.
        pass
