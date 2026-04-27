from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    # 修复后的辅助方法：每次都重新找table
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 张三访问首页
        self.browser.get('http://127.0.0.1:8000')

        # 确认标题和头部正确
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Your To-Do list', header_text)

        # 输入第一个待办事项：Buy flowers
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 验证第一个待办事项显示
        self.check_for_row_in_list_table('1: Buy flowers')

        # 输入第二个待办事项：Give a gift to Lisi
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 验证两个待办事项都显示
        self.check_for_row_in_list_table('1: Buy flowers')
        self.check_for_row_in_list_table('2: Give a gift to Lisi')

        # 张三想知道网站是否会记住清单（下节课内容）
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')