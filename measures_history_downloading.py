from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd

stations_df = pd.read_csv('stations_info.csv')
history_url = 'https://aqicn.org/historical/#city:'


def get_history(curr_url):
    current_directory = os.getcwd()
    download_folder = os.path.join(current_directory, "measures_history")

    options = webdriver.FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_folder)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")

    driver = webdriver.Firefox(options=options)
    driver.get(curr_url)

    # Wait for the page to load and for the download button to become clickable
    wait = WebDriverWait(driver, 60)
    try:
        btn1 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div[5]/div[2]/div/center[1]/span[2]/div")))
        btn1.click()

        btn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div[5]/div[2]/div/center[1]/span[2]/div/center/div")))
        btn2.click()

        files_before = set(os.listdir(download_folder))

        # This will block until a new file appears in the download directory or timeout after 120 seconds
        WebDriverWait(driver, 120, 1).until(
            lambda driver: files_before != set(os.listdir(download_folder))
        )

        files_after = set(os.listdir(download_folder))
        new_files = files_after - files_before
        return next(iter(new_files), None)
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()


for index, row in stations_df.iterrows():
    print(f'Pobieranie historii dla stacji: {index + 1}')
    try:
        history_file = get_history(f"{history_url}{row['station_url']}")
        print(f'\t{history_file}')
        stations_df.loc[index, 'history_file'] = str(history_file)
        time.sleep(5)
    except Exception as e:
        print(f'\tNie udało się pobrać danych: {e}')
stations_df.to_csv('collected_data/stations_info_history.csv', index=False)
