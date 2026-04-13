from selenium import webdriver

browser = webdriver.Chrome()

#张三听说有一个在线代办事项应用
#他去看了应用的首页
browser.get('http://localhost:8000')

#他注意到网页里包含“To-Do”这个词
assert 'To-Do' in browser.title

#应用有一个输入待办事项的文本输入框

#他在文本输入框输入“buy flowers”

#他按了回车键后，页面更新
#待办事项表格中显示了“1: Buy flowers"

#页面中有显示了一个文本输入框，可以输入其他待办事项
#他输入了“Send a gift to Lisi“

#页面再次更新，他的清单中显示了这两个待办事项

#长什么想知道这个网站是否会记住他的清单
#他看到网站为他生成了一个唯一的URL

#他访问了那个URL，发现他的待办事项列表还在
#他满意的离开了

browser.quit()