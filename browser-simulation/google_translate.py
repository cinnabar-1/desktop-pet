# utf-8
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
from selenium.webdriver.support import expected_conditions
import subprocess
import datetime

import time

chrome_path = str()

driver = str()


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
        usable = self.browser_wait.until(expected_conditions.presence_of_element_located((by, value)),
                                         message) and usable

        if usable:
            return self.try_find_element(call, by, value)
        else:
            raise Exception(message)

    def delay_click(self, by, value, call):
        message = by + " " + value + " not find"
        usable = self.browser_wait.until(lambda driver: driver.find_element(by, value).is_enabled(),
                                         message)
        # 元素可点击
        usable = self.browser_wait.until(expected_conditions.element_to_be_clickable((by, value)),
                                         message)
        # 元素可见
        usable = self.browser_wait.until(expected_conditions.presence_of_element_located((by, value)),
                                         message) and usable

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
            input_element.send_keys(i)
        # ActionChains操作当前聚焦（点击）的元素
        # for character in world:  # 在 world 是一个字符串的情况下
        #     print(character)
        #     self.actions.send_keys(character).perform()
        #     time.sleep(0.1)  # 增加适当延时以确保下游处理完成

        # 必须，不然send key 会有问题，sleep久一点，等google翻译将当前的翻译结束，不然可能读取到之前的结果
        time.sleep(1)
        # find_element 0
        # 直接的词义
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

        # 整个字典元素（子元素为各种不同的词义）
        dict_all = self.delay_find(By.CLASS_NAME, dict_class,
                                   lambda by, value: self.browser.find_element("class name", dict_class))
        dict_children = dict_all.find_elements(By.XPATH, "./*")
        print("words translate: %s" % translate_text)
        translate_r = translate_r + translate_text + "<br>"
        for dict_child in dict_children:
            # 词性
            speech_elements = dict_child.find_elements("class name", part_of_speech_class)
            # 序号
            order_elements = dict_child.find_elements("class name", order_class)
            # 词义整个大元素
            means_elements = dict_child.find_elements("class name", means_class)
            if len(speech_elements) != 0:
                text = speech_elements[0].text
                print("speech: %s" % text)
                translate_r = translate_r + text + "<br>"
            if len(order_elements) != 0:
                text = order_elements[0].text + ":"
                print("order: %s" % text)
                translate_r = translate_r + text
            if len(means_elements) != 0:
                means_children = means_elements[0].find_elements(By.XPATH, "./*")
                # 词义-英文解释
                if len(means_children) > 0:
                    text = means_children[0].text
                    translate_r = translate_r + text
                    print("means: %s" % text)
                # 词义-例句
                if len(means_children) > 1:
                    text = means_children[1].text
                    translate_r = translate_r + "<br>example: <br>" + text
                    print("example: %s" % text)
                # 词义-字面量
                if len(means_children) > 2:
                    text = means_children[2].text
                    translate_r = translate_r + text
                    print("words: %s" % text)
                # 词义-近义词
                if len(means_children) > 3:
                    synonyms_children = means_children[3]
                    synonyms_children_li = synonyms_children.find_elements(By.TAG_NAME, 'li')
                    for e in synonyms_children_li:
                        translate_r += e.text + ','
                        print("relate : %s" % e.text)
                    # text = means_children[3].text
                    # translate_r = translate_r + text

                text = means_elements[0].text
                print("means: %s" % text)
                translate_r = translate_r + "<br>"
        return translate_r

    def taobao_flash(self, flash_time):
        # 修改提交按钮，让提交按钮可点击
        change_commit_button = lambda element, class_attribute: {
            self.browser.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, 'class',
                                        class_attribute)
        }
        cart_url = "https://cart.taobao.com/"
        # time.sleep(10)
        # document.querySelector("ul[role='listbox']").childNodes[1]
        # if not self.browser.current_url.__contains__(cart_url):
        #     # 左侧跳转栏
        #     list_box = self.delay_find(By.CSS_SELECTOR, "ul[role='listbox']",
        #                                lambda x, y: self.browser.find_element(x, y))
        #     my_cart = list_box.find_elements(By.XPATH, "./*")[1]
        #     my_cart = my_cart.find_elements(By.TAG_NAME, "a")[0]
        #     cart_url = my_cart.get_attribute('href')
        #     print("cart url %s" % cart_url)
        #     cart_url = cart_url.split('?')[0]
        #     if my_cart.text != "我的购物车":
        #         print("cart not find. system exit")
        #         sys.exit(1)
        #     print("go to cart")
        #     my_cart.click()
        #     # 处理页面跳转
        #     all_handles = self.browser.window_handles
        #     for handle in all_handles:
        #         self.browser.switch_to.window(handle)
        #         if self.browser.current_url.__contains__(cart_url):
        #             print("now is chart")
        #             break
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
                        # commit_e.click()
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
    words = txt_parser()
    # words = ["culminating"]
    print(words)
    r = '''#separator:tab
#html:true'''
    browser = GoogleDriver()
    browser.start_browser("https://translate.google.com/", driver)
    try:
        for word in words:
            r = r + '\n' + browser.google_translate(word).replace('\n', "<br>")
            print("=================================")
    except BaseException as e:
        print(e)
        traceback.print_exc()
        time.sleep(10)
        exit(1)
    finally:
        browser.close_browser()
    append_file(r)


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
    # 执行的时候窗口必须在上面，不然会有异常
    # when you execute this program this browser's window must on the top otherwise there will be some exception
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(cur_time)
    # home_conf()
    company_conf()
    translate_on_google()
