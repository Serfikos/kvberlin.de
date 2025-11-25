import time
import re
import load_django
from parser_app.models import Doctor
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_practices():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    
    service = ChromeService(ChromeDriverManager().install())
    
    print("Initializing Selenium WebDriver...")
    driver = webdriver.Chrome(service=service, options=options)

    search_url = "https://www.kvberlin.de/fuer-patienten/arzt-und-psychotherapeutensuche"
    
    scraped_data = []

    try:
        driver.get(search_url)

        try:
            cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "cc-allow-all")))
            driver.execute_script("arguments[0].click();", cookie_button)
            time.sleep(1)
        except TimeoutException: 
            pass

        aerzte_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Ärzt:innen')]")))
        aerzte_switch_container = aerzte_label.find_element(By.XPATH, "./..")
        driver.execute_script("arguments[0].click();", aerzte_switch_container)
        time.sleep(1)

        search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submitBut")))
        driver.execute_script("arguments[0].click();", search_button)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "arztsuche_results")))
        
        page_num = 1
        while True:
            print(f"\n--- Processing page #{page_num} ---")
            time.sleep(2) 



            results_selector = ".arztsuche_results .docob"
            
            num_items = len(driver.find_elements(By.CSS_SELECTOR, results_selector))
            print(f"Found {num_items} doctors. Starting detailed parsing...")

            for index in range(num_items):
                try:

                    all_items_on_page = driver.find_elements(By.CSS_SELECTOR, results_selector)

                    if index >= len(all_items_on_page):
                        print(f"  > WARN: Element count changed mid-loop. Skipping index {index}.")
                        continue

                    current_item_selenium = all_items_on_page[index]

                    accordions = current_item_selenium.find_elements(By.CLASS_NAME, "p-accordion-header-link")
                    for acc in accordions:
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", acc)
                            time.sleep(0.3)
                            acc.click()
                            time.sleep(0.5) 
                        except (StaleElementReferenceException, TimeoutException): 
                            continue
                        except Exception as e_acc:
                            print(f"    - Minor error clicking accordion: {e_acc}")
                            continue

                    item_html = current_item_selenium.get_attribute('outerHTML')
                    soup = BeautifulSoup(item_html, 'html.parser')

                    title = soup.find('div', class_='fach').text.strip() if soup.find('div', class_='fach') else ""
                    name = soup.find('div', class_='name').text.strip() if soup.find('div', class_='name') else "N/A"
                    
                    street, zip_code, city = "", "", ""
                    street_tag = soup.find('div', class_='streetaddress')
                    if street_tag:
                        street = street_tag.text.strip()
                    
                    plzcity_tag = soup.find('div', class_='plzcity')
                    if plzcity_tag:
                        plzcity_text = plzcity_tag.text.strip()
                        match = re.search(r'(\d{5})\s*(.*)', plzcity_text)
                        if match:
                            zip_code = match.group(1).strip()
                            city = match.group(2).strip()
                        else:
                            city = plzcity_text

                    phone = soup.find('span', class_='tel').text.replace('Tel.:', '').strip() if soup.find('span', class_='tel') else ""
                    fax = soup.find('span', class_='fax').text.replace('Fax:', '').strip() if soup.find('span', class_='fax') else ""
                    email_tag = soup.find('div', class_='email')
                    email = email_tag.find('a').text.strip() if email_tag and email_tag.find('a') else ""

                    website_tag = soup.find('div', class_='web')
                    website = website_tag.find('a')['href'] if website_tag and website_tag.find('a') else ""

                    specializations_list = []
                    languages_list = []
                    accordion_tabs = soup.find_all('div', class_='p-accordion-tab')
                    for tab in accordion_tabs:
                        header_tag = tab.find('span', class_='p-accordion-header-text')
                        content_tag = tab.find('div', class_='p-accordion-content')
                        if header_tag and content_tag:
                            header_text = header_tag.text.strip().lower()
                            content_text = content_tag.get_text(separator='|', strip=True)
                            if not content_text:
                                continue

                            if 'fremdsprachen' in header_text:
                                languages_list = [lang.strip() for lang in content_text.split('|') if lang.strip()]
                            elif 'bezeichnungen' in header_text or 'psychotherapie' in header_text or 'barrierefreiheit' in header_text:
                                details = [d.strip() for d in content_text.split('|') if d.strip()]
                                specializations_list.extend(details)

                    opening_hours_json = {}
                    table = soup.find('table', class_='sz_table')
                    if table:
                        for row in table.find_all('tr'):
                            day_tag = row.find('td', class_='day')
                            if day_tag:
                                day = day_tag.text.strip()
                                schedule_entries = []
                                hours_table = row.find('table', class_='hourstable')
                                if hours_table:
                                    for hours_row in hours_table.find_all('tr'):
                                        hours_col = hours_row.find('td', class_='hours')
                                        comments_col = hours_row.find('td', class_='comments')
                                        entry = ""
                                        if hours_col: entry += hours_col.text.strip()
                                        if comments_col and comments_col.text.strip(): entry += f" ({comments_col.text.strip()})"
                                        if entry: schedule_entries.append(entry.strip())
                                if schedule_entries:
                                    opening_hours_json[day] = "; ".join(schedule_entries)

                    unique_id_str = f"{name}{street}{zip_code}"
                    
                    scraped_data.append({
                        "id": hash(unique_id_str), 
                        "title": title,
                        "name": name, 
                        "street": street, 
                        "zip_code": zip_code,
                        "city": city,
                        "phone": phone, 
                        "fax": fax, 
                        "email": email, 
                        "website": website,
                        "languages": languages_list,
                        "specializations": specializations_list,
                        "opening_hours": opening_hours_json,
                    })
                    print(f"  > Scraped: {name}")

                except Exception as e:
                    print(f"  > ERROR processing a card. Skipping. Error: {type(e).__name__} - {e}")
                    continue

            try:
                next_page_button_element = driver.find_element(By.CSS_SELECTOR, "button.p-paginator-next:not(.p-disabled)")
                driver.execute_script("arguments[0].scrollIntoView();", next_page_button_element)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", next_page_button_element)
                page_num += 1
     
                WebDriverWait(driver, 10).until(EC.staleness_of(all_items_on_page[0]))
            except Exception:
                print("This was the last page.")
                break
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()
        print("Selenium browser closed.")
    return scraped_data

def save_scraped_data_to_db(data):
    if not data:
        print("No data to save.")
        return
    print(f"\nSaving {len(data)} doctors to the database...")
    created_count = 0
    updated_count = 0
    for item in data:
        obj, created = Doctor.objects.update_or_create(
            kv_id=item['id'],
            defaults={
                'title': item.get('title'),
                'name': item.get('name'),
                'street': item.get('street'),
                'zip_code': item.get('zip_code'),
                'city': item.get('city'),
                'phone': item.get('phone'),
                'fax': item.get('fax'),
                'email': item.get('email'),
                'website': item.get('website'),
                'languages': item.get('languages'),
                'specializations': item.get('specializations'),
                'opening_hours': item.get('opening_hours'),
            }
        )
        if created:
            created_count += 1
        else:
            updated_count += 1
    print(f"Done. Created: {created_count}, Updated: {updated_count}. Total records processed: {len(data)}")


if __name__ == "__main__":
    results = scrape_practices()
    if results:
        save_scraped_data_to_db(results)