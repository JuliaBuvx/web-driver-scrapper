from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import csv

def setup_geckodriver():
    driver_path = GeckoDriverManager().install()
    return driver_path

def scrape_offices(driver):

    try:
        contacts_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Contacts"))
        )
        contacts_link.click()
    except Exception as e:
        print(f"Error navigating to Contacts: {e}")
        return []

    WebDriverWait(driver, 10).until(
        EC.url_to_be("https://www.onlyoffice.com/contacts.aspx")
    )

    offices_data = []
    offices = driver.find_elements(By.CSS_SELECTOR, ".companydata[itemscope]")

    for office in offices:

        country_elements = office.find_elements(By.CSS_SELECTOR, "[itemprop='addressLocality']")
        country = country_elements[0].text if country_elements else ''

        name_elements = office.find_elements(By.CSS_SELECTOR, "span:nth-of-type(2)")
        name = name_elements[0].text if name_elements else 'Not Found'

        street_address_elements = office.find_elements(By.CSS_SELECTOR, "[itemprop='streetAddress']")
        street_address = street_address_elements[0].text if street_address_elements else ''
        address_country_elements = office.find_elements(By.CSS_SELECTOR, "[itemprop='addressCountry']")
        address_country = address_country_elements[0].text if address_country_elements else ''
        postal_code_elements = office.find_elements(By.CSS_SELECTOR, "[itemprop='postalCode']")
        postal_code = postal_code_elements[0].text if postal_code_elements else ''
        telephone_elements = office.find_elements(By.CSS_SELECTOR, "[itemprop='telephone']")
        telephone = telephone_elements[0].text if telephone_elements else ''

        address_parts = [street_address, address_country, postal_code, telephone]
        full_address = ', '.join(filter(None, address_parts))

        offices_data.append([country, name, full_address])

    return offices_data


def save_to_csv(offices_data, filename):

    if not filename.lower().endswith('.csv'):
        raise ValueError("Invalid file format. Please provide a valid CSV file.")

    parent_directory = Path(filename).parent
    if not parent_directory.exists():
        raise FileNotFoundError(f"Directory '{parent_directory}' does not exist.")

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Country', 'CompanyName', 'FullAddress'])
        writer.writerows(offices_data)


def main():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    try:
        driver.get("https://www.onlyoffice.com")
        offices_data = scrape_offices(driver)
        csv_file_path = input("Please enter the path to save the CSV file: ")
        save_to_csv(offices_data, csv_file_path)

        print(f"Data saved to {csv_file_path}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()