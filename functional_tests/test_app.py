""" This file contains a Selenium test """
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time


class TestApp(StaticLiveServerTestCase):
    """Test correct register form submission"""

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_register_form_submission_with_button(self):
        self.driver.get(str(self.live_server_url) + '/users/register')
        username_input = self.driver.find_element_by_id('id_username')
        email_input = self.driver.find_element_by_id('id_email')
        password1_input = self.driver.find_element_by_id('id_password1')
        password2_input = self.driver.find_element_by_id('id_password2')
        submission_button = self.driver.find_element_by_class_name(
            'btn-primary')

        username_input.send_keys('john')
        email_input.send_keys('john@gmail.com')
        password1_input.send_keys('123johnny123')
        password2_input.send_keys('123johnny123')
        submission_button.click()
        time.sleep(2)
        redirection_url = self.driver.current_url
        self.assertEquals(self.live_server_url + '/', redirection_url,
                          'Bienvenu! Votre compte a été créé avec succès! '
                          'Vous êtes maintenant connecté')