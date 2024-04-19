import os
import re
import time
from PIL import Image
from io import BytesIO
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import json
import csv
import io
from tqdm import tqdm

# 设置线程池的大小
MAX_THREADS = 10


def get_url_dict(csv_file_path):
    key_value = {}
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        # 跳过标题行（如果存在）
        next(csv_reader, None)
        # 遍历每一行
        for row in csv_reader:
            # 提取第二列和第三列作为键和值
            key = row[2]
            value = row[1]
            key_value[key] = value
    return key_value


def request_url(title, url):
    text_content = ''
    response = requests.get(url)
    response.encoding = 'utf-8'
    # 检查请求是否成功
    if response.status_code == 200:
        webpage_content = response.content
        # print('ok')
    else:
        print(f"请求失败，状态码：{response.status_code}")

    soup = BeautifulSoup(webpage_content, 'html.parser')
    # target_element = soup.find("a", class_=["wx_tap_link", "js_wx_tap_highlight", "weui-wa-hotarea"], id="js_name")
    # # 文本
    # text_content = soup.get_text(separator=' ', strip=True)
    #
    # 图片
    img_elements = soup.find_all("img")
    i = 0
    for img in img_elements:
        # 优先使用 data-src 属性，如果不存在则使用 src 属性
        img_url = img.get("data-src") or img.get("src")
        # print(img_url)
        if not img_url:
            continue  # 如果没有找到图片 URL，则跳过该元素
        # 获取图片数据
        response = requests.get(img_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        # 保存图片
        temp_title = re.sub(r'[^a-zA-Z0-9\s]', '_', title)
        img.save(os.path.join(r'C:\Users\wuxd-a\PycharmProjects\pythonProject6\reptile\image',
                              f'{temp_title}_{i}.jpg'), "PNG")
        i += 1

    # return text_content


if __name__ == '__main__':

    # csv_file_path = r"C:\Users\wuxd-a\PycharmProjects\pythonProject6\reptile\myword.csv"
    # url_file_path = r'C:\Users\wuxd-a\PycharmProjects\pythonProject6\reptiledata3\fruits4.json'
    # ret_dict = get_url_dict(csv_file_path)  # title：url
    # # pprint(ret_dict)
    # print(type(ret_dict))
    # # 将键值对写入 JSON 文件
    # with open("urls.json", "w", encoding='utf-8') as jsonfile:
    #     json.dump(ret_dict, jsonfile, ensure_ascii=False, indent=4)
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
            # 写入文件
            # with open(os.path.join(r'C:\Users\wuxd-a\PycharmProjects\pythonProject6\reptile\txtdata', f"output_{file_count}.txt"), "a", encoding="utf-8") as f:
            #     f.write(f"##{title}##{text}")
            #     f.write("\n")
            write_count += 1
