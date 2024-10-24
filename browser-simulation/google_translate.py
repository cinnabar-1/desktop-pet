import os
import sys
import traceback

from selenium import webdriver
from selenium.common import NoSuchElementException, JavascriptException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess

import time


class GoogleDriver:
    def __init__(self):
        self.chrome_options = None
        self.actions = None
        self.browser_wait = None
        self.browser = None
        self.service = None

    def start_browser(self, url, driver="E:\\lib\\chromedriver-win64\\chromedriver.exe"):
        self.service = Service(driver)
        # self.browser = webdriver.Chrome(service=self.service)
        # 链接一个已经打开的浏览器，可能可以避免别人知道你用了selenium
        # 有个问题，如果浏览器不是程序打开的，运行程序时浏览器可能不是最上面的窗口，需要把浏览器放到最上面不然会有问题。
        # 这里出现过程序启动浏览器连接不上的情况，后来又好了，原因未知--->还是需要传入一个driver，抄代码时网上的代码都不正确
        #
        start_browser()
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)
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

    def google_translate(self, world):
        translate_r = world
        translate_r += "	"
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
        # 等待输入框可用
        input_element = self.delay_click(By.CLASS_NAME, input_class,
                                         lambda by, value: self.browser.find_element(By.CLASS_NAME, input_class))
        # 点击一下
        input_element.click()
        # 先清除一下输入框，直接send是在输入框追加
        input_element.clear()
        # 直接send是在输入框追加，一个一个写，一次写多个可能导致不完整
        for i in world:
            input_element.send_keys(
                i)
        # ActionChains操作当前聚焦（点击）的元素
        # for character in world:  # 在 world 是一个字符串的情况下
        #     print(character)
        #     self.actions.send_keys(character).perform()
        #     time.sleep(0.1)  # 增加适当延时以确保下游处理完成
        # 必须，不然send key 会有问题，sleep久一点，等google翻译将当前的翻译结束，不然可能读取到之前的结果
        time.sleep(1)
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
        except (NoSuchElementException, JavascriptException) as e:
            print(e)
            traceback.print_exc()

        dict_all = self.delay_find(By.CLASS_NAME, dict_class,
                                   lambda by, value: self.browser.find_element("class name", dict_class))
        # part_of_speech = self.browser.find_element("class name", part_of_speech_class)
        # world_dict = self.browser.find_element("class name", means_class)
        dict_children = dict_all.find_elements(By.XPATH, "./*")
        print(translate_text)
        translate_r = translate_r + translate_text + "<br>"
        for dict_child in dict_children:
            speech_elements = dict_child.find_elements("class name", part_of_speech_class)
            order_elements = dict_child.find_elements("class name", order_class)
            means_elements = dict_child.find_elements("class name", means_class)
            if len(order_elements) != 0:
                text = order_elements[0].text + ":" + means_elements[0].text
                print(text)
                translate_r = translate_r + text + "<br>"
            elif len(speech_elements) != 0:
                text = speech_elements[0].text
                print()
                print(text)
                translate_r = translate_r + text + "<br>"
        return translate_r

    def taobao_flash(self):
        # self.browser.get()
        buy_button_id = ""

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


def append_file(line, file_name="demo.txt"):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, "a", encoding='utf-8') as f:
        f.write(line)


def translate_on_google():
    # words = txt_parser()
    words = ["culminating"]
    print(words)
    r = '''#separator:tab
#html:true'''
    browser = GoogleDriver()
    browser.start_browser("https://translate.google.com/")
    try:
        for word in words:
            r = r + '\n' + browser.google_translate(word).replace('\n', "<br>")
            print("=================================")
    except Exception as e:
        print(e)
        traceback.print_exc()
        time.sleep(10)
        exit(1)
    finally:
        browser.close_browser()
    append_file(r)


def start_browser():
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
    chrome_path = '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe "'
    cmd = chrome_path + '--remote-debugging-port=9222 ' + '--user-data-dir="C:\\selenium\\ChromeProfile"'
    subprocess.Popen(cmd)


if __name__ == '__main__':
    # translate_on_google()
    browser = GoogleDriver()
    browser.start_browser("https://login.taobao.com/member/login.jhtml")
    time.sleep(10)
    # document.querySelector("ul[role='listbox']").childNodes[1]
    browser.browser.find_element(By.CSS_SELECTOR, "ul[role='listbox']").click()
    browser.close_browser()
