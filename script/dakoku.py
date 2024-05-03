import os
import time
import click
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

class TimeStamper:
    def __init__(self, user="", pw=""):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--profile-directory=Default')
        self.driver = webdriver.Chrome(options=options)
        self.driver.delete_all_cookies()
        self.user = user
        self.pw = pw
        self.company_code = "Bcg237"

    def request(self):
        self.driver.get("https://cl.i-abs.co.jp/CX_s-clocking")
        time.sleep(1)

    def input_account_info(self):
        print("Entering account info")
        company_code = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-login/div/div/div/div/main/div/div/table/tr[1]/td/input"
        )
        company_code.clear()
        company_code.send_keys(self.company_code)

        employee_code = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-login/div/div/div/div/main/div/div/table/tr[2]/td/input"
        )
        employee_code.clear()
        employee_code.send_keys(self.user)

        password = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-login/div/div/div/div/main/div/div/table/tr[3]/td/input"
        )
        password.clear()
        password.send_keys(self.pw)

    def login(self):
        self.input_account_info()
        login_button = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-login/div/div/div/div/main/div/div/table/tr[4]/td/input"
        )
        login_button.click()
        time.sleep(1)

    def dakoku(self, mode: str) -> None:
        dakoku_button = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-menu/main/section/ul/li[1]/a"
        )
        dakoku_button.click()
        time.sleep(1)

        if mode not in ["work_start", "work_end", "rest_start", "rest_end"]:
            raise ValueError(f"Parameter: {mode} is not valid.")

        # shigoto_start
        elif mode == "work_start":
            each_mode_button = self.driver.find_element(
                by=By.XPATH,
                value="/html/body/app-root/div/section/div/xsw-0000/div/main/section/div/div/label[1]"
            )
            each_mode_button.click()
            time.sleep(1)

        # shigoto_end
        elif mode == "work_end":
            each_mode_button = self.driver.find_element(
                by=By.XPATH,
                value="/html/body/app-root/div/section/div/xsw-0000/div/main/section/div/div/label[2]"
            )
            each_mode_button.click()
            time.sleep(1)

        # kyukei_start
        elif mode == "rest_start":
            each_mode_button = self.driver.find_element(
                by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-0000/div/main/section/div/div/label[3]"
            )
            each_mode_button.click()
            time.sleep(1)

        # kyukei_end
        elif mode == "rest_end":
            each_mode_button = self.driver.find_element(
                by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-0000/div/main/section/div/div/label[4]"
            )
            each_mode_button.click()
            time.sleep(1)

        enter_button = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-0000/div/main/section/div/a"
        )
        enter_button.click()
        time.sleep(1)

        yes_button = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/app-root/div/section/div/xsw-xswengrave/div/div/div[3]/button[1]"
        )
        yes_button.click()


@click.command()
@click.option("--mode", type=str, required=True)
@click.option("--test", is_flag=True, show_default=True, default=False, required=False)
def main(mode: str, test: bool):
    import chromedriver_binary

    if test:
        print("Test mode")
        pass
    else:
        slp_time = int(random.uniform(1, 1000))
        print("Sleeping for {} seconds".format(slp_time))
        time.sleep(int(slp_time))

    # A bit hacky way of path management in local vs. dev
    if os.path.exists('data.csv'):
        df_data = pd.read_csv('data.csv', dtype=str)
    else:
        df_data = pd.read_csv('/home/ubuntu/script/data.csv', dtype=str)

    list_data = list(zip(df_data['user'].values, df_data['pw'].values))
    print("Data: ", list_data)

    for (user, pw) in list_data:
        print('Initializing')
        timestamper = TimeStamper(user=user, pw=pw)
        print('Going to dakoku page')
        timestamper.request()
        print('Logging in')
        timestamper.login()
        print('Registering dakoku')
        print('Mode: {}'.format(mode))
        timestamper.dakoku(mode=mode)
        timestamper.driver.delete_all_cookies()
        timestamper.driver.quit()
        print('Done')

if __name__ == '__main__':
    main()