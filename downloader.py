import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import sys
import warnings
from webdriver_manager.chrome import ChromeDriverManager

warnings.simplefilter("ignore")

def download_facebook_link():
    while True:
        try:
            with open("facebook_link.txt", "r") as file:
                link_to_input = file.read().strip()

            if link_to_input:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--disable-software-rasterizer")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")

                # Pass ChromeOptions directly to webdriver.Chrome constructor
                driver_path = ChromeDriverManager().install()
                chrome_service = ChromeService(executable_path=driver_path)
                driver = webdriver.Chrome(service=chrome_service, options=chrome_options)



                try:
                    url = "https://snapsave.app/facebook-reels-download"
                    driver.get(url)

                    link_input_xpath = "/html/body/main/div[1]/section[2]/form/div[1]/input"
                    submit_button_xpath = "/html/body/main/div[1]/section[2]/form/div[2]/button"

                    link_input = driver.find_element(By.XPATH, link_input_xpath)
                    link_input.send_keys(link_to_input)

                    submit_button = driver.find_element(By.XPATH, submit_button_xpath)
                    submit_button.click()

                    driver.implicitly_wait(10)

                    link_to_copy_xpath = "/html/body/main/div[1]/section/div/div[1]/div[2]/div/table/tbody/tr[1]/td[3]/a"
                    link_to_copy = driver.find_element(By.XPATH, link_to_copy_xpath).get_attribute("href")

                    with open("elink.txt", "w") as elink_file:
                        elink_file.write(link_to_copy)

                except Exception as inner_error:
                    print(f"An error occurred during processing: {inner_error}")

                finally:
                    driver.quit()
                    with open("facebook_link.txt", "w") as file:
                        file.write("")

                    sys.exit()

            time.sleep(5)

        except Exception as outer_error:
            print(f"An error occurred: {outer_error}")
            time.sleep(5)

if __name__ == "__main__":
    download_facebook_link()
