import os
# -*- coding: UTF-8 -*-
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import random, string
import time

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '#id_Login'
    PASSWORD = '#id_Password'
    DOMAIN = '#id_Domain'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        self.driver.find_element_by_css_selector(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_css_selector(self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element_by_css_selector(self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()


class TopMenu(Component):
    EMAIL = '#PH_user-email'

    def get_email(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EMAIL).text
        )


class BaseSettings(Component):
    TARGET = '#product-type-6043'
    URL = 'input[data-name="url"]'
    IMAGE = 'input[data-name="image"]'
    SUBMIT = '.banner-form__save-button'

    def get_url(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.URL)
        )[1]

    def get_image(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.IMAGE)
        )

    def set_advertise(self):
        radio = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.TARGET)
        )
        radio.click()
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('.base-setting__campaign-name__input')
        ).send_keys(randomword(8))

    def submit(self):
        sub = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SUBMIT)
        )
        sub.click()

    def add_adv(self, _url, _image):
        self.set_advertise()
        url = self.get_url()
        image = self.get_image()
        url.send_keys(_url)
        image.send_keys(_image)
        WebDriverWait(self.driver, 30, 0.1).until(
            self.wait_for_image_load
        )
        self.submit()

    def wait_for_image_load(self, d):
        BANNER_PREVIEW = '.banner-preview__img'
        images = self.driver.find_elements_by_css_selector(BANNER_PREVIEW)
        for element in images:
            print "width" + element.value_of_css_property("width")
            if element.value_of_css_property("width") == '320px':
                return element


class BaseSettingsSmall(Component):
    TARGET = '#product-type-6043'
    HEADER = 'input[data-name="title"]'
    TEXT = 'textarea[data-name="text"]'
    URL = 'input[data-name="url"]'
    IMAGE = 'input[data-name="image"]'
    SUBMIT = '.banner-form__save-button'
    CHANGE = '.banner-form__banner-formats__tab'

    def get_header(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.HEADER)
        )

    def get_text(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.TEXT)
        )

    def get_url(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.URL)
        )[1]

    def get_image(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.IMAGE)
        )

    def set_advertise(self):
        radio = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.TARGET)
        )
        radio.click()
        change = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath("//span[@class='banner-form__banner-formats__tab-text'][text() = '120 × 100']")
        )
        change.click()
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('.base-setting__campaign-name__input')
        ).send_keys(randomword(8))


    def submit(self):
        sub = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SUBMIT)
        )
        sub.click()

    def add_adv(self, _header, _text, _url, _image):
        self.set_advertise()
        header = self.get_header()
        text = self.get_text()
        url = self.get_url()
        image = self.get_image()
        header.send_keys(_header)
        text.send_keys(_text)
        url.send_keys(_url)
        image.send_keys(_image)
        WebDriverWait(self.driver, 30, 0.1).until(
            self.wait_for_image_load
        )
        self.submit()


    def wait_for_image_load(self, d):
        BANNER_PREVIEW = '.banner-preview__img'
        images = self.driver.find_elements_by_css_selector(BANNER_PREVIEW)
        for element in images:
            if element.value_of_css_property("width") == '120px':
                return element


class Where(Component):
    CHECKBOXES = '[data-name="regions"] .tree__node__input'
#    CHECKBOXES_RUS = '[data-name="regions"] .tree__node__list'
#    SETTING_VALUE_RUS = '[data-valid-flag="regions"] [data-name="regions"] .tree__node__value'
#    SETTING_VALUE_ANOTHER = '[data-valid-flag="regions"] [data-name="regions"] .tree__node__value'

    def check_rus(self):
        check = self.driver.find_elements_by_css_selector(self.CHECKBOXES)[0]
        check.click()

    def check_another(self):
        check = self.driver.find_elements_by_css_selector(self.CHECKBOXES)[5]
        check.click()

    def where_checked(self):
        check = WebDriverWait(self.driver, 15, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.CHECKBOXES)
        )
        checked = {
            "russia": False,
            "ussr": False,
            "europe": False,
            "asia": False,
            "north_america": False,
            "another_world": False
        }
        if check[0].is_selected():
            checked["russia"] = True
        if check[1].is_selected():
            checked["ussr"] = True
        if check[2].is_selected():
            checked["europe"] = True
        if check[3].is_selected():
            checked["asia"] = True
        if check[4].is_selected():
            checked["north_america"] = True
        if check[5].is_selected():
            checked["another_world"] = True
        return checked

    def where_deep_checked(self):
        #change = WebDriverWait(self.driver, 30, 0.1).until(
        #    lambda d: d.find_element_by_xpath("//span[@class='tree__node__collapse-icon']")#[data-node-id = 'Россия']")
        #)
        change = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('li[id="regions188"] span[data-node-id="Россия"]')#lambda d: d.find_element_by_css_selector('li[class="tree__node tree__node_collapsed has_children"] span[data-node-id="Россия"]')
        )
        change.click()

        check = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('li[class="tree__node tree__node_collapsed"] span[data-node-id="Алтайскийкрай"]')#lambda d: d.find_element_by_id('view9678')#lambda d: d.find_element_by_css_selector('input[id="view9661"]')
        )
        if check.is_selected():
            print "False"
#            return False

        change.click()

        change = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('li[id="regions100009"] span[data-node-id="Остальноймир"]')
        )
        change.click()

        change = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('li[id="regions100007"] span[data-node-id="АвстралияиОкеания"]')
        )

        change.click()

        check = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('li[class="tree__node tree__node_collapsed"] span[data-node-id="Австралия"]')
        )

        if check.is_selected():
            print "true"
#            return True
"""
        check = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_id('view9661')
        )
        if check.is_selected():
            print "1"
        checks = self.driver.find_elements_by_css_selector('tree__node__input')
        for element in checks:
            if element.value_of_css_property("id") == 'view9661':
                if element.is_selected():
                    print "2"

        check = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath("//span[@class='tree__node__input'][id = 'view9661']")
        )

        if check.is_selected():
            print "3"

        return False

        check = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('li[class="tree__node__input"] span[id="view9661"]')
        )
        if check.is_selected():
            return False
        check = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('li[class="tree__node__input"] span[id="view10358"]')
        )
        if check.is_selected():
            return True"""



class IncomeGroup(Component):
    SETTING_VALUE = '[data-valid-flag="income_group"] [data-name="income_group"] .campaign-setting__value'
    CHECKBOXES = '[data-name="income_group"] .campaign-setting__input'
    CHECKBOXES_BLOCK = '[data-name="income_group"] .campaign-setting__list'

    def get_setting_value(self):
        return WebDriverWait(self.driver, 30, 1).until(
            lambda d: d.find_element_by_css_selector(self.SETTING_VALUE)
        )

    def click_on_setting_value(self):
        setting_value = self.get_setting_value()
        setting_value.click()

    def show_income_group_checkboxes(self):
        self.click_on_setting_value()
        wait = WebDriverWait(self.driver, 15, 1)
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.CHECKBOXES_BLOCK))
        )

    def check_high(self):
        check = self.driver.find_elements_by_css_selector(self.CHECKBOXES)[0]
        check.click()

    def check_med(self):
        check = self.driver.find_elements_by_css_selector(self.CHECKBOXES)[1]
        check.click()

    def check_low(self):
        check = self.driver.find_elements_by_css_selector(self.CHECKBOXES)[2]
        check.click()

    def what_checked(self):
        check = WebDriverWait(self.driver, 15, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.CHECKBOXES)
        )
        checked = {
            "high": False,
            "med": False,
            "low": False
        }
        if check[0].is_selected():
            checked["high"] = True
        if check[1].is_selected():
            checked["med"] = True
        if check[2].is_selected():
            checked["low"] = True
        return checked

class BannerPreview(Component):
    PREVIEW = '.added-banner__banner-preview'
    IMAGE = '.banner-preview__img'

    def get_preview_block(self):
        preview = WebDriverWait(self.driver, 30, 0.1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.PREVIEW))
        )
        return preview

    def get_banner_info(self):
        preview = self.get_preview_block()
        wait = WebDriverWait(preview, 15, 0.1)
        image = wait.until(lambda d: d.find_element_by_css_selector(self.IMAGE))
        url = image.value_of_css_property("background-image")

        return {
            "url": url
        }

class BannerPreviewSmall(Component):
    PREVIEW = '.added-banner__banner-preview'
    TEXT = '.banner-preview__text'
    HEADER = '.banner-preview__title'
    IMAGE = '.banner-preview__img'

    def get_preview_block(self):
        preview = WebDriverWait(self.driver, 30, 0.1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.PREVIEW))
        )
        return preview

    def get_banner_info(self):
        preview = self.get_preview_block()
        wait = WebDriverWait(preview, 15, 0.1)
        text = wait.until(lambda d: d.find_element_by_css_selector(self.TEXT).text)
        header = wait.until(lambda d: d.find_element_by_css_selector(self.HEADER).text)
        image = wait.until(lambda d: d.find_element_by_css_selector(self.IMAGE))
        url = image.value_of_css_property("background-image")

        return {
            "text": text,
            "header": header,
            "url": url
        }

class AddAdv(Component):
    SLIDER = '.price-slider__begunok'
    EDIT_BTN = '.control__link_edit'
    ADD_BTN = ".main-button-new"

    def add_adv(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.SLIDER))
        )
        self.driver.find_element_by_css_selector(self.ADD_BTN).click()


class LastCampaign(Component):
    REDACT_BTN = '.control__link_edit'
    DELETE_BTN = '.campaign-row .control__preset_delete'

    def get_redact_btn(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.REDACT_BTN)
        )

    def get_delete_btn(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DELETE_BTN)
        )

    def redact_btn_click(self):
        self.get_redact_btn().click()

    def delete_campaign(self):
        self.get_delete_btn().click()







