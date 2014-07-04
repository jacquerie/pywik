import requests


class PywikError(Exception):
    pass


class Pywik(object):
    def __init__(self, api_url, token_auth):
        self.api_url = api_url
        self.session = requests.session()
        self.session.params['module'] = 'API'
        self.session.params['token_auth'] = token_auth
        self.session.params['format'] = 'json'

    def get_user_manager(self):
        return UserManager(self.session, self.api_url)


def _check_error(response):
    if response.ok:
        return response.json()
    else:
        raise PywikError(response.text)


class UserManager(object):
    def __init__(self, session, url):
        self.session = session
        self.url = url

    def add_user(self, user_login, password, email, alias=''):
        response = self.session.get(self.url, params={
            'method': 'UsersManager.addUser',
            'userLogin': user_login,
            'password': password,
            'email': email,
            'alias': alias
        })

        return _check_error(response)

    def delete_user(self, user_login):
        return _check_error(self.session.get(self.url, params={
            'method': 'UsersManager.deleteUser',
            'userLogin': user_login
        }))
