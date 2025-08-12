import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


class WebScraper:
    def __init__(self, base_url):
        """
        初始化爬虫
        :param base_url: 网站的基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        # 添加请求头，模拟浏览器访问
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def login(self, login_url, username, password, additional_data=None):
        """
        执行登录操作
        :param login_url: 登录页面的URL
        :param username: 用户名
        :param password: 密码
        :param additional_data: 其他需要提交的登录数据
        :return: 登录是否成功
        """
        # 获取登录页面以提取可能需要的隐藏字段（如CSRF token）
        login_page = self.session.get(login_url)
        
        if login_page.status_code != 200:
            return False
            
        soup = BeautifulSoup(login_page.content, 'html.parser')
        
        # 查找可能需要提交的隐藏字段
        hidden_inputs = soup.find_all("input", type="hidden")
        
        # 尝试查找用户名和密码输入框的实际字段名
        username_input = soup.find("input", {"type": "text"}) or soup.find("input", {"type": "email"}) or soup.find("input", {"name": True})
        password_input = soup.find("input", {"type": "password"})
        
        login_data = {}
        
        # 设置用户名和密码字段
        if username_input:
            username_field = username_input.get('name', 'username')
            login_data[username_field] = username
        else:
            login_data['username'] = username
            
        if password_input:
            password_field = password_input.get('name', 'password')
            login_data[password_field] = password
        else:
            login_data['password'] = password
        
        # 添加隐藏字段到登录数据中
        for hidden_input in hidden_inputs:
            name = hidden_input.get('name')
            value = hidden_input.get('value', '')
            if name:
                login_data[name] = value
                
        # 添加额外的登录数据
        if additional_data:
            login_data.update(additional_data)
            
        # 提交登录表单
        response = self.session.post(login_url, data=login_data)
        
        # 检查登录是否成功
        return response.status_code == 200
    
    def scrape_news_content(self, target_url, max_items=5):
        """
        从指定URL提取<div class="news_content">中的内容
        :param target_url: 目标页面URL
        :param max_items: 最大新闻条目数，默认为5条
        :return: 提取到的内容列表
        """
        # 访问目标页面
        response = self.session.get(target_url)
        
        if response.status_code != 200:
            return []
            
        # 解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找所有class为news_content的div元素，限制数量
        news_divs = soup.find_all('div', class_='news_content')[:max_items]

        # 提取内容
        contents = []
        for div in news_divs:
            contents.append({
                'text': div.get_text(strip=True)
            })
            
        return contents
        
    def save_to_csv(self, origin, contents, filename=None):
        """
        将内容保存到CSV文件
        :param contents: 要保存的内容列表
        :param filename: 文件名，默认为news_content_当前时间.csv
        :return: 保存的文件名
        """
        if not contents:
            return None
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_content_{timestamp}_{origin}.csv"
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for content in contents:
                writer.writerow(content)
                
        return filename


def main():
    # 使用示例
    # 请根据实际情况修改以下URL和凭据
    APPIX = ["sina"]
    BASE_URL = "https://tushare.pro"
    LOGIN_URL = BASE_URL + "/login"

    # 创建爬虫实例
    scraper = WebScraper(BASE_URL)
    
    # 登录
    username = os.getenv("TUSHARE_USERNAME")
    if not username:
        username = input("请输入您的Tushare用户名：")

    password = os.getenv("TUSHARE_PASSWORD")
    if not password:
        password = input("请输入您的Tushare密钥：")
    
    print("正在登录...")

    if scraper.login(LOGIN_URL, username, password):
        print("登录成功")
        for i in APPIX:
            TARGET_URL = BASE_URL + "/news/"+  i
            # 提取数据，限制每站只获取5条新闻
            print(f"正在提取数据{i}")
            contents = scraper.scrape_news_content(TARGET_URL, max_items=5)

            if contents:
                print(f"找到 {len(contents)} 个新闻内容")
                # 保存到CSV文件
                filename = scraper.save_to_csv(i, contents)
                if filename:
                    print(f"内容已保存到 {filename}")
                else:
                    print("保存内容时出错")
            else:
                print("未找到任何新闻内容")
    else:
        print("登录失败")


if __name__ == "__main__":
    main()