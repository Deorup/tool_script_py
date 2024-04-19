import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import json
from tqdm import tqdm


def download_image(img_url, title, i):
    if not img_url:
        return  # 如果没有找到图片 URL，则跳过该元素
    # 获取图片数据
    response = requests.get(img_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    # 保存图片
    temp_title = re.sub(r"[^a-zA-Z0-9_\u4e00-\u9fa5\-\(\)\s]", "-", title)
    img.save(os.path.join(r'C:\Users\wuxd-a\PycharmProjects\pythonProject6\reptile\image',
                          f'{temp_title}_{i}.jpg'), "PNG")


def request_url(title, url):
    text_content = ''
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        webpage_content = response.content
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return

    soup = BeautifulSoup(webpage_content, 'html.parser')
    img_elements = soup.find_all("img")

    with ThreadPoolExecutor() as executor:
        for i, img in enumerate(img_elements):
            img_url = img.get("data-src") or img.get("src")
            executor.submit(download_image, img_url, title, i)

    return text_content  # 如果需要返回文本内容，可以在这里返回


if __name__ == '__main__':
    with open("urls.json", 'r', encoding='utf-8') as jsonfile:
        url_dict = json.load(jsonfile)
        # i = 0
        write_count = 1
        file_count = 0
        for title, url in tqdm(url_dict.items(), total=len(url_dict)):
            # text = request_url(title=title, url=url)
            request_url(title=title, url=url)
            if write_count >= 100:
                file_count += 1
                write_count = 0
                print(f'第{file_count}个文件')
