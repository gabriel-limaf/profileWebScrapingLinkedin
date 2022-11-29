from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import csv
from selenium.webdriver.common.by import By

# Login
print('- Logando no Linkedin')
driver = webdriver.Chrome()
sleep(2)
url = 'https://www.linkedin.com/'
driver.get(url)
sleep(2)
credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
sleep(2)
email_field = driver.find_element(By.ID, 'session_key')
email_field.send_keys(username)
sleep(3)
password_field = driver.find_element(By.ID, "session_password")
password_field.send_keys(password)
sleep(2)
signin_field = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/button')
signin_field.click()
sleep(3)
print('- Logou no Linkedin')

# Pesquisar cargo
print('- Pesquisando....')
search = 'https://www.linkedin.com/search/results/people/?keywords=compensation&origin=SWITCH_SEARCH_VERTICAL&sid=4Wx'
driver.get(search)

# Coletar perfis


def geturl():
    page_source = BeautifulSoup(driver.page_source)
    profiles = page_source.find_all('a', class_='app-aware-link')
    all_profile_URL = []
    for profile in profiles:
        profile_URL = profile.get('href')
        if "https://www.linkedin.com/in/" in profile_URL:
            if profile_URL not in all_profile_URL:
                all_profile_URL.append(profile_URL)
    return all_profile_URL


input_page = int(input('How many pages you want to scrape: '))
URLs_all_page = []
for page in range(input_page):
    URLs_one_page = geturl()
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(3)
    next_button = driver.find_element(By.CLASS_NAME, "artdeco-pagination__button--next")
    driver.execute_script("arguments[0].click();", next_button)
    URLs_all_page = URLs_all_page + URLs_one_page
    sleep(2)

# Coletar dados do perfil
with open('output.csv', 'w',  newline='', encoding='utf-8') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'URL', 'Company']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        driver.get(linkedin_URL)
        print('- Accessing profile: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find('div', {'class': 'mt2 relative'})  # teste
        try:
            name = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
            print('--- Nome do perfil: ', name)
            title = info_div.find('div', class_='text-body-medium break-words').get_text().strip()
            print('--- Título do perfil: ', title)
            location = info_div.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip()
            print('--- Localização do perfil: ', location)
            company = info_div.find('span', class_='pv-text-details__right-panel-item-text hoverable-link-text break-words text-body-small t-black').get_text().strip()
            print('--- Empresa do perfil: ', company)
            writer.writerow({headers[0]: name, headers[1]: location, headers[2]: title, headers[3]: linkedin_URL, headers[4]: company})
            print('\n')
        except:
            pass
print('Finalizado!')
