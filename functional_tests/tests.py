from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
max_wait=10
class NewVisitorTest(LiveServerTestCase):
  
  def setUp(self):
    self.browser=webdriver.Chrome()
    
  def tearDown(self):
    self.browser.quit()
  def wait_for_row_in_list_table(self,row_text):
    start_time=time.time()
    while True:
      try:
        table=self.browser.find_element(By.ID,'id_list_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertIn(row_text,[row.text for row in rows])
        return
      except (AssertionError,WebDriverException) as e:
        if time.time()-start_time>max_wait:
          raise e
        time.sleep(0.5)
  def check_for_row_in_list_table(self,row_text):
    table=self.browser.find_element(By.ID,'id_list_table')
    rows=table.find_elements(By.TAG_NAME,'tr')
    self.assertIn(row_text,[row.text for row in rows])
  def test_can_start_a_list_and_retrieve_it_later(self):
    # 张三听说有一个在线待办事项的应用
    # 他去看了这个应用的首页
    self.browser.get(self.live_server_url)
    # 他注意到网页的标题和头部都包含“To-Do"这个词
    self.assertIn('To-Do',self.browser.title)
    header_text=self.browser.find_element(By.TAG_NAME,'h1').text
    self.assertIn('To-Do',header_text)
 
    # 应用有一个输入待办事项的文本输入框
    inputbox=self.browser.find_element(By.ID,'id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),'Enter a to-do item'
    )
    
    # 他在文本输入框中输入了“Buy flowers'
    inputbox.send_keys('Buy flowers')
    # 他按了回车键键后，页面更新了
    # 待办事项表格中显示了“1:Buy flowers"
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)
    self.check_for_row_in_list_table('1:Buy flowers')
    # 页面中又显示了一个文本输入框，可以输入其他待办事项
    # 他输入了“gift to girlfriend"
    inputbox=self.browser.find_element(By.ID,'id_new_item')
    inputbox.send_keys('gift to girlfriend')
    inputbox.send_keys(Keys.ENTER)

    # 页面再次更新，她的清单中显示了这两个待办事项
    self.check_for_row_in_list_table('1:Buy flowers')
    self.check_for_row_in_list_table('2:gift to girlfriend')
     
     # 他满意的离开了
def test_multiple_users_can_start_lists_at_different_urls(self):
    # 张三新建了一个待办事项
    self.browser.get(self.live_server_url)
    inputbox=self.browser.find_element(By.ID,'id_new_item')
    inputbox.send_keys('Buy flowers')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1:Buy flowers')
    # 他注意到清单有一个唯一的URL
    zhangsan_list_url=self.browser.current_url
    self.assertRegex(zhangsan_list_url,'/lists/.+')
    # 现在一个叫李四的新用户访问了网站
    ## 我们使用一个新的浏览器会话
    ## 确保张三的信息不会从cookie中泄露出来
    self.browser.quit()
    self.browser=webdriver.Chrome()
    # 李四访问首页
    # 页面中看不到张三的清单
    self.browser.get(self.live_server_url)
    page_text=self.browser.find_element(By.TAG_NAME,'body').text
    self.assertNotIn('Buy flowers',page_text)
    self.assertNotIn('gift to girlfriend',page_text)

    # 李四新建了一个待办事项
    inputbox=self.browser.find_element(By.ID,'id_new_item')
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1:Buy milk')
    # 李四获得了他的唯一URL
    lisi_list_url=self.browser.current_url
    self.assertRegex(lisi_list_url,'/lists/.+')
    self.assertNotEqual(lisi_list_url,zhangsan_list_url)
    # 这个URL上没有张三的清单
    page_text=self.browser.find_element(By.TAG_NAME,'body').text
    self.assertNotIn('Buy flowers',page_text)
    self.assertIn('Buy milk',page_text)
    # 李四很满意，他离开了
    # 张三想知道这个网站是否会记住她的清单
    #他看到网站为他生成了一个唯一的UR L
    self.fail('Finish the test!')
    # 他访问那个URL，发现他的待办事项列表还在
    # 他满意的离开了
