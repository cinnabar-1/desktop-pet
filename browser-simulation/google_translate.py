import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import time


class GoogleDriver:
    def __init__(self):
        self.browser_wait = None
        self.browser = None
        self.service = None

    def start_browser(self, url, driver="E:\\lib\\chromedriver-win64\\chromedriver.exe"):
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)
        self.browser_wait = WebDriverWait(self.browser, 10)
        self.browser.get(url)

    def delay_find(self, by, value, call):
        message = by + " " + value + " not find"
        find = self.browser_wait.until(lambda driver: driver.find_element(by, value).is_enabled(),
                                       message)
        if find:
            # 延时一下执行，判断enable之后立即执行还是不行
            time.sleep(1)
            return call(by, value)
        else:
            raise message

    def get_result(self, world):
        # 需要翻译的文字的输入框
        input_class = "er8xn"
        # 先清除一下输入框，直接send是在输入框追加
        self.browser.find_element(By.CLASS_NAME, input_class).clear()
        # 直接send是在输入框追加
        self.browser.find_element(By.CLASS_NAME, input_class).send_keys(
            world)
        # 查字典类
        check_dict = "dWI6ed"
        self.delay_find(By.CLASS_NAME, check_dict,
                        lambda by, value: self.browser.find_element(by, value).click())
        # 查字典 之后外层的类 包含了词性和含义。需要用这个判断具体的词性包含了哪些含义
        dict_class = "Dwvecf"
        # 词性类
        part_of_speech_class = "eIKIse"
        # 序号类
        order_class = "RSggmb"
        # 含义类
        means_class = "JAk00"
        # find_element 0
        translate = self.delay_find(By.CLASS_NAME, "ryNqvb",
                                    lambda by, value: self.browser.find_element(by, value))
        # time.sleep(1)
        try:
            # 展开所有
            self.browser.execute_script(
                'document.getElementsByClassName("VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc LQeN7 VK4HE")[0].click()')
        except Exception:
            print(sys.exception().__traceback__)

        dict_all = self.browser.find_element("class name", dict_class)
        part_of_speech = self.browser.find_element("class name", part_of_speech_class)
        world_dict = self.browser.find_element("class name", means_class)
        dict_children = dict_all.find_elements(By.XPATH, "./*")
        print(translate.text)
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
    # words = txt_parser()
    words = ["browser"]
    print(words)
    browser = GoogleDriver()
    browser.start_browser("https://translate.google.com/", "E:\\lib\\chromedriver-win64\\chromedriver.exe")
    for word in words:
        browser.get_result(word)
        print("=================================")
    browser.close_browser()
