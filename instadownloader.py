import os
import sys
import time
import warnings
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Suppress warnings
warnings.simplefilter("ignore")

def clear_terminal():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')  # Clear command prompt on Windows
    else:
        os.system('clear')  # Clear terminal on Unix-based systems

def download_instagram_link():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    profile_directory = os.path.join(script_directory, "edge_profile")

    while True:
        try:
            with open("instagram_link.txt", "r") as file:
                link_to_input = file.read().strip()

            if link_to_input:
                edge_options = webdriver.EdgeOptions()
                edge_options.use_chromium = True
                edge_options.add_argument("--headless")
                edge_options.add_argument("--disable-gpu")
                edge_options.add_argument("--disable-software-rasterizer")
                edge_options.add_argument("--disable-dev-shm-usage")
                edge_options.add_argument("--no-sandbox")
                
                # Adjusting cookie settings to handle third-party cookie blocking
                edge_options.add_argument("--disable-web-security")
                edge_options.add_argument(f"--user-data-dir={profile_directory}")

                # Pass EdgeOptions directly to webdriver.Edge constructor
                driver_path = EdgeChromiumDriverManager().install()
                edge_service = EdgeService(executable_path=driver_path)
                driver = webdriver.Edge(service=edge_service, options=edge_options)

                try:
                    url = "https://savereels.com/download"
                    driver.get(url)

                    link_input_xpath = "/html/body/div[1]/div/div/form/div[1]/div/input"
                    submit_button_xpath = "/html/body/div[1]/div/div/form/div[2]/button"

                    link_input = driver.find_element(By.XPATH, link_input_xpath)
                    link_input.send_keys(link_to_input)

                    submit_button = driver.find_element(By.XPATH, submit_button_xpath)
                    submit_button.click()

                    driver.implicitly_wait(10)

                    link_to_copy_xpath = "/html/body/div/div[1]/div[2]/div/div/a"
                    link_to_copy = driver.find_element(By.XPATH, link_to_copy_xpath).get_attribute("href")

                    with open("elink.txt", "w") as elink_file:
                        elink_file.write(link_to_copy)

                except Exception as inner_error:
                    pass  # Ignore exceptions during processing

                finally:
                    driver.quit()
                    clear_terminal()  # Clear the terminal
                    with open("instagram_link.txt", "w") as file:
                        file.write("")

                    sys.exit()

            time.sleep(5)

        except Exception as outer_error:
            pass  # Ignore exceptions at the outer level

if __name__ == "__main__":
    download_instagram_link()
