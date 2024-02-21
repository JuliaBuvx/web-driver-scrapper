import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import scrape_offices


class TestOfficeScraping(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("https://www.onlyoffice.com")

    def test_contact_page_url(self):
        try:
            contacts_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Contacts"))
            )
            contacts_link.click()
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be("https://www.onlyoffice.com/contacts.aspx")
            )
            self.assertEqual(self.driver.current_url, "https://www.onlyoffice.com/contacts.aspx")
        except Exception as e:
            self.fail(f"Error: {e}")

    def test_scrape_offices(self):

        offices_data = scrape_offices(self.driver)
        self.assertTrue(len(offices_data) > 0, "List should not be empty")

    def test_address_format(self):
        offices_data = scrape_offices(self.driver)
        for _, _, full_address in offices_data:
            self.assertNotIn(",,", full_address, "Extra commas are presented")

    def test_missing_data_handling(self):
        offices_data = scrape_offices(self.driver)
        for office_data in offices_data:
            self.assertNotIn('Not Found', office_data, "Not Found data exists")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
