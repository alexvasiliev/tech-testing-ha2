import urlparse
from tests.pages.components import AuthForm, TopMenu, BaseSettings, BaseSettingsSmall, IncomeGroup, AddAdv, Where,\
    BannerPreview, BannerPreviewSmall, LastCampaign


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class CampaignPage(Page):
    PATH = '/ads/campaigns/'

    @property
    def last_campaign(self):
        return LastCampaign(self.driver)


class CreatePage(Page):
    PATH = '/ads/create'

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def base_settings(self):
        return BaseSettings(self.driver)

    @property
    def base_settings_small(self):
        return BaseSettingsSmall(self.driver)

    @property
    def income_group(self):
        return IncomeGroup(self.driver)

    @property
    def add_adv(self):
        return AddAdv(self.driver)

    @property
    def banner_preview(self):
        return BannerPreview(self.driver)

    @property
    def banner_preview_small(self):
        return BannerPreviewSmall(self.driver)

    @property
    def regions(self):
        return Where(self.driver)
