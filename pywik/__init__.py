import requests
import urllib


class PywikError(Exception):
    pass


class Pywik(object):
    def __init__(self, api_url, token_auth):
        self.api_url = api_url
        self.session = requests.session()
        self.token_auth = token_auth
        self.session.params.update(self.default_params())

    def default_params(self):
        return {
            'module': 'API',
            'token_auth': self.token_auth,
            'format': 'json'
        }

    @property
    def users_manager(self):
        return UsersManager(self, self.api_url)

    @property
    def sites_manager(self):
        return SitesManager(self, self.api_url)


def _check_error(response):
    if response.ok:
        msg = response.json()
        if msg.get('result') == 'error':
            raise PywikError(msg)
        return msg
    else:
        raise PywikError(response.text)


def make_array(prefix, lst):
    """Make an array that Piwik will understand

    make_array('urls', ['abc', 'def']) => &urls[0]=abc&urls[1]=def

    :param prefix: name of the array to create
    :param lst: list of entries
    """
    ret = ''
    for idx, value in enumerate(lst):
        ret += '&{0}[{1}]={2}'.format(prefix, idx, urllib.quote(value))
    return ret


class Base(object):
    def __init__(self, client, url):
        self.client = client
        self.session = client.session
        self.url = url


class UsersManager(Base):
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
        :param site_ids: list of site ids
        """
        return _check_error(self.session.post(self.url, params={
            'method': 'UsersManager.setUserAccess',
            'userLogin': user_login,
            'access': access,
            'idSites': ','.join((str(x) for x in site_ids))
        }))

    def get_token_auth(self, user_login, md5_password):
        return _check_error(self.session.get(self.url, params={
            'method': 'UsersManager.getTokenAuth',
            'userLogin': user_login,
            'md5Password': md5_password
        }))['value']


class SitesManager(Base):
    def add_site(self, site_name, urls, ecommerce='', site_search='', search_keyword_parameters='',
                 search_category_parameters='', excluded_ips='', excluded_query_parameters='',
                 timezone='', currency='', group='', start_date='', excluded_user_agents='',
                 keep_url_fragments='', type=''):
        """Add a site
        :return: site id
        """
        params = self.client.default_params()
        params.update({
            'method': 'SitesManager.addSite',
            'siteName': site_name,
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
            'type': type
        })

        if start_date:
            params['startDate'] = start_date

        data = urllib.urlencode(params, True) + make_array('urls', urls)
        return _check_error(self.session.post(self.url, params=data))['value']

    def delete_site(self, site_id):
        return _check_error(self.session.post(self.url, params={
            'method': 'SitesManager.deleteSite',
            'idSite': site_id
        }))

    def get_javascript_tag(self, id_site, piwik_url='', merge_subdomains='', group_page_titles_by_domain='',
                           merge_alias_urls='', visitor_custom_variables='', page_custom_variables='',
                           custom_campaign_name_query_param='', custom_campaign_keyword_param='',
                           do_not_track=''):
        return _check_error(self.session.get(self.url, params={
            'method': 'SitesManager.getJavascriptTag',
            'idSite': id_site,
            'piwikUrl': piwik_url,
            'mergeSubdomains': merge_subdomains,
            'groupPageTitlesByDomain': group_page_titles_by_domain,
            'mergeAliasUrls': merge_alias_urls,
            'visitorCustomVariables': visitor_custom_variables,
            'pageCustomVariables': page_custom_variables,
            'customCampaignNameQueryParam': custom_campaign_name_query_param,
            'customCampaignKeywordParam': custom_campaign_keyword_param,
            'doNotTrack': do_not_track
        }))['value']

