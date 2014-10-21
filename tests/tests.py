import os
import time
import unittest
from selenium.webdriver import DesiredCapabilities, Remote, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pages.page_objects import AuthPage, CreatePage, CampaignPage

class TestCase(unittest.TestCase):

    def setUp(self):
        self.campaign_was_created = False

        self.USERNAME = 'tech-testing-ha2-5@bk.ru'
        self.PASSWORD = os.environ.get('TTHA2PASSWORD', 'Pa$$w0rD-5')#'Pa$$w0rD-5'#
        self.DOMAIN = '@bk.ru'

        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.set_domain(self.DOMAIN)
        auth_form.set_login(self.USERNAME)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()


    def tearDown(self):
        if self.campaign_was_created:
            campaign_page = CampaignPage(self.driver)
            campaign_page.open()
            last_campaign = campaign_page.last_campaign
            last_campaign.delete_campaign()
        self.driver.quit()

    def test_base_settings_small_picture(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        image = os.path.abspath("img2.jpg")
        base_settings = create_page.base_settings_small
        base_settings.add_adv("42", "42", "www.42.ru", image)

        banner = create_page.banner_preview_small
        banner_before = banner.get_banner_info()

        add_adv = create_page.add_adv
        add_adv.add_adv()

        self.campaign_was_created = True

        campaign_page = CampaignPage(self.driver)
        last_campaign = campaign_page.last_campaign
        last_campaign.redact_btn_click()

        banner_after = banner.get_banner_info()
        check = banner_before == banner_after
        self.assertTrue(check)


    def test_income_group(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        image = os.path.abspath("img.jpg")
        base_settings = create_page.base_settings
        base_settings.add_adv("www.42.ru", image)

        income_group = create_page.income_group
        income_group.show_income_group_checkboxes()
        income_group.check_low()
        income_group.check_high()

        add_adv = create_page.add_adv
        add_adv.add_adv()

        self.campaign_was_created = True

        campaign_page = CampaignPage(self.driver)
        last_campaign = campaign_page.last_campaign
        last_campaign.redact_btn_click()

        income_group.show_income_group_checkboxes()
        checked = income_group.what_checked()
        check = checked["low"] and checked["high"]

        self.assertTrue(check)


    def test_regions(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        image = os.path.abspath("img.jpg")
        base_settings = create_page.base_settings
        base_settings.add_adv("www.42.ru", image)

        regions = create_page.regions
        regions.check_rus()
        regions.check_another()

        add_adv = create_page.add_adv
        add_adv.add_adv()

        self.campaign_was_created = True

        campaign_page = CampaignPage(self.driver)
        last_campaign = campaign_page.last_campaign
        last_campaign.redact_btn_click()

        checked = regions.where_checked()
        check = checked["another_world"]

        self.assertTrue(check)


    def test_base_settings_big_picture(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        image = os.path.abspath("img.jpg")
        base_settings = create_page.base_settings
        base_settings.add_adv("www.42.ru", image)

        banner = create_page.banner_preview
        banner_before = banner.get_banner_info()

        add_adv = create_page.add_adv
        add_adv.add_adv()

        self.campaign_was_created = True

        campaign_page = CampaignPage(self.driver)
        last_campaign = campaign_page.last_campaign
        last_campaign.redact_btn_click()

        banner_after = banner.get_banner_info()
        check = banner_before == banner_after
        self.assertTrue(check)


    def test_regions_deep(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        image = os.path.abspath("img.jpg")
        base_settings = create_page.base_settings
        base_settings.add_adv("www.42.ru", image)

        regions = create_page.regions
        regions.check_rus()
        regions.check_another()

        add_adv = create_page.add_adv
        add_adv.add_adv()

        self.campaign_was_created = True

        campaign_page = CampaignPage(self.driver)
        last_campaign = campaign_page.last_campaign
        last_campaign.redact_btn_click()

        checked = regions.where_deep_checked()
        self.assertTrue(checked)
