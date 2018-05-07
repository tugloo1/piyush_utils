import re
from retry import retry
from selenium.webdriver import Chrome
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException


exceptions = (ElementNotVisibleException, NoSuchElementException)


class ChromeDriver(Chrome):
    def __init__(self):
        super(ChromeDriver, self).__init__()

    @retry(exceptions, delay=3, tries=3)
    def find_element_by_css_selector(self, css_selector):
        return super(ChromeDriver, self).find_element_by_css_selector(css_selector)

    @retry(exceptions, tries=3, delay=3)
    def find_element_by_id(self, element_id: str):
        return super(ChromeDriver, self).find_element_by_id(element_id)

    def write_to_text_field_by_id(self, text_field_id: str, text_field_input: str):
        element = self.find_element_by_id(text_field_id)
        element.send_keys(text_field_input)

    def click_on_button_with_text(self, button_text: str):
        elements = self.find_elements_by_tag_name('button')
        for e in elements:
            element_text = e.text
            if element_text == button_text:
                e.click()
                return
        raise NoSuchElementException('Could not find element with text ' + button_text)

    @retry(exceptions, tries=3, delay=3)
    def click_on_element_by_link_text(self, link_text: str):
        elements = self.find_elements_by_link_text(link_text)
        if elements.__len__() == 0:
            raise NoSuchElementException
        elements[0].click()

    @retry(exceptions, delay=3, tries=3)
    def find_elements_by_class_name(self, class_name: str):
        elements = super(ChromeDriver, self).find_elements_by_class_name(class_name)
        if elements.__len__() == 0:
            raise NoSuchElementException
        return elements

    @retry(exceptions, delay=3, tries=3)
    def find_element_by_class_name(self, class_name: str):
        return self.find_elements_by_class_name(class_name)[0]

    @retry(exceptions, delay=3, tries=3)
    def get_element_by_css_selectors_text(self, css_selector: str, css_regex_search: str):
        elements = self.find_elements_by_css_selector(css_selector)
        for element in elements:
            if re.match(css_regex_search, element.text):
                return element
        raise NoSuchElementException
