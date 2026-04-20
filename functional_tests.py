from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import os

# 屏蔽Chrome日志
os.environ['WDM_LOG_LEVEL'] = '0'
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--log-level=3')

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 张三听说有一个在线待办事项应用
        # 他打开了首页
        self.browser.get('http://localhost:8000')

        # 他注意到网页标题和头部都包含"To-Do"
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # 应用有一个输入待办事项的文本框
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 他在文本框中输入"Buy flowers"
        inputbox.send_keys('Buy flowers')

        # 按下回车键，页面更新
        inputbox.send_keys(Keys.ENTER)

        # 页面显示了他输入的待办事项
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Buy flowers', [row.text for row in rows])

        # 他又输入了第二个待办事项
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(verbosity=2)