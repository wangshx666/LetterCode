from io import BytesIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import chaojiying

e_username = 'wsxTest'
e_password = '123456wsx'

CJY_USERNAME = '...'  # 账号
CJY_PASSWORD = '...'  # 密码
CJY_SOFT_ID = '...'  # 生成的唯一key
CJY_KIND = 1902  # 验证码类型

url = 'http://bm.e21cn.com/login/user'
browser = webdriver.Chrome()
# 窗口最大化保证坐标正确
browser.maximize_window()
browser.get(url)
wait = WebDriverWait(browser, 10)


def get_code(png):
    cjy = chaojiying.Chaojiying_Client(CJY_USERNAME, CJY_PASSWORD, CJY_SOFT_ID)  # 用户中心>>软件ID 生成一个替换 96001
    im = open(png, 'rb').read()   # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    result = cjy.PostPic(im, CJY_KIND)
    code = result['pic_str']
    return code


def get_position():
    # 显示等待
    img = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="imgCheckCode"]'))
    )
    print(img.location)
    print(img.size)
    size = img.size
    location = img.location
    # 左上角定位
    x1 = location['x'] * 1.25
    y1 = location['y'] * 1.25
    # 右下角定位
    x2 = x1 + size['width']*1.28
    y2 = y1 + size['height']*1.28
    return (x1, y1, x2, y2)


def screen_png():
    # 获取整个窗口的图片
    big_screen = browser.get_screenshot_as_png()
    # 保存  BytesIO -- 读取二进制文件
    img = Image.open(BytesIO(big_screen))
    img.save('a1.png')

    code_img = img.crop(get_position())
    code_img.save('a2.png')

def login(CODE):
    # 用户名
    username= browser.find_element_by_id('username')
    username.send_keys(e_username)
    # 密码
    pwd = browser.find_element_by_id('pwd')
    pwd.send_keys(e_password)
    # 验证码
    code = browser.find_element_by_id('CheckCode')
    code.send_keys(CODE)
    # 点击登录按钮
    btn_login = browser.find_element_by_id('btn_login')
    btn_login.click()


if __name__ == '__main__':
    screen_png()
    # 超级鹰校验
    code = get_code('a2.png')
    print(code)
    # 模拟登陆
    login(code)
