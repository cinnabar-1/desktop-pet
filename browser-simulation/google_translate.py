import sys
import traceback

from selenium import webdriver
from selenium.common import NoSuchElementException, JavascriptException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class GoogleDriver:
    def __init__(self):
        self.actions = None
        self.browser_wait = None
        self.browser = None
        self.service = None

    def start_browser(self, url, driver="E:\\lib\\chromedriver-win64\\chromedriver.exe"):
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)
        self.browser_wait = WebDriverWait(self.browser, 10)
        self.browser.get(url)
        self.actions = ActionChains(self.browser)

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
            except StaleElementReferenceException:
                traceback.print_exc()
        return result

    def get_result(self, world):
        print(word)
        # 需要翻译的文字的输入框
        input_class = "er8xn"
        # 直接的词义
        direct_means_class = "ryNqvb"
        # 查字典 之后外层的类 包含了词性和含义。需要用这个判断具体的词性包含了哪些含义
        dict_class = "Dwvecf"
        # 词性类
        part_of_speech_class = "eIKIse"
        # 序号类
        order_class = "RSggmb"
        # 含义类
        means_class = "JAk00"
        # 查字典类
        check_dict_class = "dWI6ed"
        input_element = self.delay_click(By.CLASS_NAME, input_class,
                                         lambda by, value: self.browser.find_element(By.CLASS_NAME, input_class))
        # 点击一下
        input_element.click()
        # 先清除一下输入框，直接send是在输入框追加
        input_element.clear()
        input_element.click()
        # 直接send是在输入框追加，一个一个写，一次写多个可能导致不完整
        for i in world:
            input_element.send_keys(
                i)
        # ActionChains操作当前聚焦（点击）的元素
        # for character in world:  # 在 world 是一个字符串的情况下
        #     print(character)
        #     self.actions.send_keys(character).perform()
        #     time.sleep(0.1)  # 增加适当延时以确保下游处理完成
        # 必须，不然send key 会有问题
        time.sleep(0.5)
        # find_element 0
        translate_text = self.delay_find(By.CLASS_NAME, direct_means_class,
                                         lambda by, value: self.browser.find_element(by, value).text)
        # 查字典
        self.delay_click(By.CLASS_NAME, check_dict_class,
                         lambda by, value: self.browser.find_element(by, value).click())
        try:
            # 显示全部
            self.browser.execute_script(
                'document.getElementsByClassName("VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc LQeN7 VK4HE")[0].click()')
        except NoSuchElementException and JavascriptException:
            print(sys.exception().__traceback__)

        dict_all = self.delay_find(By.CLASS_NAME, dict_class,
                                   lambda by, value: self.browser.find_element("class name", dict_class))
        part_of_speech = self.browser.find_element("class name", part_of_speech_class)
        world_dict = self.browser.find_element("class name", means_class)
        dict_children = dict_all.find_elements(By.XPATH, "./*")
        print(translate_text)
        for dict_child in dict_children:
            speech_elements = dict_child.find_elements("class name", part_of_speech_class)
            order_elements = dict_child.find_elements("class name", order_class)
            means_elements = dict_child.find_elements("class name", means_class)
            if len(order_elements) != 0:
                print(order_elements[0].text, ":", means_elements[0].text)
            elif len(speech_elements) != 0:
                print()
                print(speech_elements[0].text)

    def close_browser(self):
        self.browser.close()


def txt_parser():
    separator = '\t'
    word = list()
    with open("draft-20240903072332.txt") as f:
        line_index = 0
        body_index = 2
        while True:
            line = f.readline()
            if not line:
                break
            if line_index > body_index:
                word.append(line.split(separator)[0])
            line_index += 1
    return word


if __name__ == '__main__':
    words = txt_parser()
    # words = ["browser"]
    print(words)
    browser = GoogleDriver()
    browser.start_browser("https://translate.google.com/", "D:\\lib\\chromedriver-win64\\chromedriver.exe")
    try:
        for word in words:
            browser.get_result(word)
            print("=================================")
    except Exception:
        traceback.print_exc()
        time.sleep(10)
    browser.close_browser()
