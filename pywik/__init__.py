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

    @property
    def users_manager(self):
        return UsersManagaer(self.session, self.api_url)

    @property
    def sites_manager(self):
        return SitesManager(self.session, self.api_url)


def _check_error(response):
    if response.ok:
        return response.json()
    else:
        raise PywikError(response.text)


class Base(object):
    def __init__(self, session, url):
        self.session = session
        self.url = url


class UsersManagaer(Base):
    def add_user(self, user_login, password, email, alias=''):
        return _check_error(self.session.post(self.url, params={
            'method': 'UsersManager.addUser',
            'userLogin': user_login,
            'password': password,
            'email': email,
            'alias': alias
        }))

    def delete_user(self, user_login):
        return _check_error(self.session.post(self.url, params={
            'method': 'UsersManager.deleteUser',
            'userLogin': user_login
        }))

    def set_user_access(self, user_login, access, site_ids):
        """
        :param access: one of noaccess, view, or admin
        """
        return _check_error(self.session.post(self.url, params={
            'method': 'UsersManager.setUserAccess',
            'userLogin': user_login,
            'access': access,
            'idSites': site_ids
        }))


class SitesManager(Base):
    def add_site(self, site_name, urls, ecommerce='', site_search='', search_keyword_parameters='',
                 search_category_parameters='', excluded_ips='', excluded_query_parameters='',
                 timezone='', currency='', group='', start_date='', excluded_user_agents='',
                 keep_url_fragments='', type=''):
        """Add a site
        :return: site id
        """
        params = {
            'method': 'SitesManager.addSite',
            'siteName': site_name,
            'urls': urls,
            'ecommerce': ecommerce,
            'siteSearch': site_search,
            'searchKeywordParameters': search_keyword_parameters,
            'searchCategoryParameters': search_category_parameters,
            'excludedIps': excluded_ips,
            'excludedQueryParameters': excluded_query_parameters,
            'timezone': timezone,
            'currency': currency,
            'group': group,
            'excludedUserAgents': excluded_user_agents,
            'keepURLFragments': keep_url_fragments,
            'type': type}

        if start_date:
            params['startDate'] = start_date

        return _check_error(self.session.post(self.url, params))['value']

    def delete_site(self, site_id):
        return _check_error(self.session.post(self.url, params={
            'method': 'SitesManager.deleteSite',
            'idSite': site_id
        }))
