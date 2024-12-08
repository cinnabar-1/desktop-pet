import os
import traceback

from selenium import webdriver
from selenium.common import NoSuchElementException, JavascriptException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import datetime

import time


class GoogleDriver:
    def __init__(self):
        self.chrome_options = None
        self.actions = None
        self.browser_wait = None
        self.browser = None
        self.service = None

    def start_browser(self, url, driver="E:\\lib\\chromedriver-win64\\chromedriver.exe"):
        # 链接一个已经打开的浏览器，可能可以避免别人知道你用了selenium
        # 有个问题，如果浏览器不是程序打开的，运行程序时浏览器可能不是最上面的窗口，需要把浏览器放到最上面不然会有问题。
        # 这里出现过程序启动浏览器连接不上的情况，后来又好了，原因未知--->还是需要传入一个driver，抄代码时网上的代码都不正确
        self.browser = self.connect_to_browser(True, driver)
        self.browser_wait = WebDriverWait(self.browser, 10)
        self.browser.get(url)
        self.actions = ActionChains(self.browser)
        print(self.browser.current_url)

    def connect_to_browser(self, connect, driver=None) -> WebDriver:
        if connect:
            # 链接一个已经打开的浏览器，可能可以避免别人知道你用了selenium
            # 有个问题，如果浏览器不是程序打开的，运行程序时浏览器可能不是最上面的窗口，需要把浏览器放到最上面不然会有问题。
            # 这里出现过程序启动浏览器连接不上的情况，后来又好了，原因未知--->还是需要传入一个driver，抄代码时网上的代码都不正确
            start_browser()
            self.service = Service(driver)
            self.chrome_options = Options()
            self.chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)
        else:
            # 直接使用webdriver
            self.service = Service(driver)
            self.browser = webdriver.Chrome(service=self.service)
        return self.browser

    def delay_find(self, by, value, call):
        message = by + " " + value + " not find"
        usable = self.browser_wait.until(lambda driver: driver.find_element(by, value).is_enabled(),
                                         message)
        # 元素可见
        usable = self.browser_wait.until(EC.presence_of_element_located((by, value)), message) and usable

        if usable:
            return self.try_find_element(call, by, value)
        else:
            raise Exception(message)

    def delay_click(self, by, value, call):
        message = by + " " + value + " not find"
        usable = self.browser_wait.until(lambda driver: driver.find_element(by, value).is_enabled(),
                                         message)
        # 元素可点击
        usable = self.browser_wait.until(EC.element_to_be_clickable((by, value)),
                                         message)
        # 元素可见
        usable = self.browser_wait.until(EC.presence_of_element_located((by, value)), message) and usable

        if usable:
            return self.try_find_element(call, by, value)
        else:
            raise Exception(message)

    def try_find_element(self, call, by, value, retry_times=3):
        result = None
        for i in range(retry_times):
            try:
                result = call(by, value)
                break
            except (StaleElementReferenceException, ElementNotInteractableException) as e:
                print(e)
                traceback.print_exc()
        return result

    def taobao_flash(self, flash_time):
        # 修改提交按钮，让提交按钮可点击
        change_commit_button = lambda element, class_attribute: {
            self.browser.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, 'class',
                                        class_attribute)
        }
        cart_url = "https://cart.taobao.com/"
        print(self.browser.current_url)
        print("flash time is: " + flash_time)
        committed_order = False
        # 全选购物车
        cart_operator_list_id = "cart-operation-fixed"
        cart_operator_list = self.delay_find(By.ID, "cart-operation-fixed",
                                             lambda x, y: self.browser.find_element(x, y))
        cart_operator_list = self.browser.find_element(By.ID, "cart-operation-fixed")
        select_all = cart_operator_list.find_elements(By.XPATH, "./*")[0]
        print(select_all.text)
        select_all.click()
        # 结算 / 提交订单
        settle_class = 'btn--QDjHtErD'
        try:
            # 点击结算按钮
            # self.delay_find(By.CLASS_NAME, settle_class,
            #                 lambda x, y: self.browser.find_element(x, y)).click()
            self.browser.find_element(By.CLASS_NAME, settle_class).click()
        except BaseException as e:
            print(e)
            print("结算按钮不可点击")
        commit_list_class = "btnBox--p9CumEtE"
        # full xpath 不太准确
        commit_xpath = '//*[@id="submitOrder"]/div/div[2]/div'
        # 获取提交订单按钮
        commit_e = self.delay_find(By.XPATH, commit_xpath, lambda by, value: self.browser.find_element(by, value))
        # 直接修改提交订单按钮
        change_commit_button(commit_e, settle_class)
        # 循环判断时间
        while not committed_order:
            cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if flash_time < cur_time:
                # 尝试三次
                for i in range(1, 3):
                    try:
                        print(f"start try commit order {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
                        # 点击提交
                        commit_e.click()
                        print(f"commit success {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
                        committed_order = True
                        break
                    except BaseException as e:
                        print(e)
                        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                        print('try commit order')
            # print(cur_time)
            # time.sleep(0.001)  # 1ms循环
        time.sleep(100)

    def close_browser(self):
        self.browser.close()


chrome_path = str()

driver = str()


def home_conf():
    global chrome_path, driver
    chrome_path = '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe "'
    driver = "E:\\lib\\chromedriver-win64\\chromedriver.exe"


def company_conf():
    global chrome_path, driver
    chrome_path = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'
    driver = "D:\\lib\\chromedriver-win64\\chromedriver.exe"


def start_browser():
    # chrome_path = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'
    cmd = chrome_path + '--remote-debugging-port=9222 ' + '--user-data-dir="C:\\selenium\\ChromeProfile"'
    subprocess.Popen(cmd)


if __name__ == '__main__':
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # flash_time = input(f"请输入抢购时间，格式如 {cur_time} :\n")
    home_conf()
    # company_conf()
    # flash_time = '2024-11-01 20:00:00.00000'
    flash_day = datetime.datetime.now().strftime('%Y-%m-%d')
    flash_clock = ' 20:00:00.00000'
    flash_time = flash_day + flash_clock
    # translate_on_google()
    browser = GoogleDriver()
    try:
        # 第一次进淘宝登录页，后续可以直接进购物车。如果还进登录页，可能会进不去
        browser.start_browser("https://cart.taobao.com/",
                              driver)
        browser.taobao_flash(flash_time)
        browser.close_browser()
    finally:
        browser.close_browser()
