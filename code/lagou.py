from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from fake_useragent import UserAgent
from chaojiying import Chaojiying_Client
import time
import requests

ua = UserAgent()


class LaGouselenium():
    def __init__(self):
        
        #无头浏览器部分     将最后一行代码的注释部分放到实例化selenium的括号中
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu') # chrome_options=chrome_options
        self.chrome = webdriver.Chrome()
        # 隐式等待三秒
        self.chrome.implicitly_wait(3)

    def ImgGetCode(self, imgPath, img_type):  #打码平台解码
        chaojiying = Chaojiying_Client('打码平台账号', '密码', '解码类型')  # 用户中心>>软件ID 生成一个替换 96001
        im = open(imgPath, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        return (chaojiying.PostPic(im, img_type))['pic_str']

    def login(self):  #自动登入部分
        loginUrl = 'https://passport.lagou.com/login/login.html?signature=DACE64F6C94A21DB5C1966DD6CFC79DB&service=https%253A%252F%252Feasy.lagou.com%252Fdashboard%252Findex.htm%253Ffrom%253Dc_index&action=login&serviceId=account&ts=1584729132631'
        self.chrome.get(loginUrl)
        # 账号 密码 登录
        self.chrome.find_element_by_xpath(
            '//form[@class="active"]/div[@data-propertyname="username"]/input').send_keys('公司账号')
        time.sleep(1)
        self.chrome.find_element_by_xpath(
            '//form[@class="active"]/div[@data-propertyname="password"]/input').send_keys('密码')
        time.sleep(1)
        self.chrome.find_element_by_xpath('//form[@class="active"]/div[@data-propertyname="submit"]/input').click()
        time.sleep(1)

        '''
        这部分是应急状况，如果抓取不到图片链接，就使用这一部分，屏幕截图，取出图片。
        self.chrome.save_screenshot('main.png')
        code_img_ele = self.chrome.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/div')
        location = code_img_ele.location  
        size = code_img_ele.size  
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))
        i = Image.open('main.png') 
        frame = i.crop(rangle)  
        frame.save('code.png')
        imgs = Image.open('code.png')
        Img = imgs.convert('L')
        Img.save('code2.png')

        '''
        code_img_ele = self.chrome.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/div/div[2]') #获取验证吗图片的坐标
        img_page = self.chrome.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div[6]/div/div/div[2]/div[1]/div[1]/div[1]/img')  #获取图片地址
        url = img_page.get_attribute('src')
        img_data = requests.get(url).content
        with open('./code2.png', 'wb') as fp:
            fp.write(img_data)   #图片保存

        result = self.ImgGetCode('./code2.png', 9004)  #打印解码结果
        print(result)  # x1,y1|x2,y2|x3,y3

        # x1,y1|x2,y2|x3,y3 ==>[[x1,y1],[x2,y2],[x3,y3]]
        #对打码结果进行坐标优化，使得selenium识别
        all_list = []  # [[x1,y1],[x2,y2],[x3,y3]]
        if '|' in result:
            list_1 = result.split('|')
            count_1 = len(list_1)
            for i in range(count_1):
                xy_list = []
                x = int(list_1[i].split(',')[0])
                y = int(list_1[i].split(',')[1])
                xy_list.append(x)
                xy_list.append(y)
                all_list.append(xy_list)
        else:
            x = int(result.split(',')[0])
            y = int(result.split(',')[1])
            xy_list = []
            xy_list.append(x)
            xy_list.append(y)
            all_list.append(xy_list)
        for l in all_list:
            x = l[0]
            y = l[1]
            ActionChains(self.chrome).move_to_element_with_offset(code_img_ele, x, y).click().perform()  #鼠标连点优化好的坐标
        time.sleep(1)
        self.chrome.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/div/div[3]/a/div').click()  #登录
        time.sleep(2)
        # c = input('如果出现验证码 手动验证后 回车, 否则直接回车')

    def Automatical(self):  #发笔试题过程
        self.chrome.find_element_by_xpath('//*[@id="new-top-header"]/header/div/div[1]/nav/ul/li[5]/a').click()
        self.chrome.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div[2]/div[2]/div/ul/li[2]/div/span[1]').click()
        self.chrome.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/label/input').click()
        self.chrome.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div[2]/div[3]/div[1]/div/div/div/div[3]/div/div[1]/div/span').click()
        self.chrome.find_element_by_xpath(
            '/html/body/div[5]/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div[1]/form/div[7]/div/button[2]').click()
        print('笔试邀请完成')
        time.sleep(5)
        self.chrome.quit()  #退出


if __name__ == '__main__':
    starlg = LaGouselenium()
    starlg.login()
    starlg.Automatical()