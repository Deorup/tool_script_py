from pathlib import Path
import pandas as pd
import json
from translate_file_type import FileConverter
import csv

"""
这段代码是递归遍历文件夹下的所有某类型的文件
对每个文件进行处理
"""


def process_file(r_folder_path):
    for file_path in r_folder_path.rglob("*"):
        file_path = Path(file_path)
        extension = file_path.suffix.lower()  # 获取文件扩展名

        if extension == ".csv":
            # 追加写入csv文件
            # target_path = r''
            # append_csv(file_path, target_path)
            # ... 处理 DataFrame ...
            print(f"CSV 文件 {file_path} 处理完成。")

        elif extension == ".docx":
            #  转换示例
            # fileconverter = FileConverter(file_path)
            # fileconverter.word_to_txt()

            # ... 处理 DataFrame ...
            print(f"DOCX 文件 {file_path} 处理完成。")
        elif extension == ".xlsx":
            df = pd.read_excel(file_path)
            # ... 处理 DataFrame ...
            print(f"XLSX 文件 {file_path} 处理完成。")

        elif extension == ".json":
            # ... 处理 JSON 数据 ...
            # 对json追加写一般采用先写入list，再整体写入
            existing_data = []
            # with open(file_path, "r") as f:
            #     existing_data = json.load(f)
            #     new_data = process_content(existing_data)
            # existing_data.append(new_data)  # 将新数据添加到列表
            #
            # with open(file_path, "w", encoding='utf-8') as f:
            #     json.dump(existing_data, f, indent=4)  # 使用 indent 参数格式化输出
            # print(f"JSON 文件 {file_path} 处理完成。")

        elif extension == ".txt":
            with open(file_path, "r", encoding='utf-8') as f:
                text = f.read()
                print(text)
            # ... 处理文本内容 ...
            print(f"TXT 文件 {file_path} 处理完成。")

        else:
            print(f"不支持的文件类型: {file_path}")


"""
这段代码是合并csv文件
"""
global_header_written = False


def append_csv(source_file, destination_file):
    with (open(source_file, 'r', encoding='utf-8') as sf,
          open(destination_file, 'a', encoding='utf-8', newline='') as df):
        global global_header_written
        reader = csv.reader(sf)
        writer = csv.writer(df)

        header = next(reader)  # 读取源文件的标题行

        if not global_header_written and df.tell() == 0:  # 如果目标文件为空，则写入标题
            writer.writerow(header)
            global_header_written = True

        # 跳过源文件的第一行数据（假设其为标题行）
        next(reader, None)

        # 将源文件的其余数据写入目标文件
        for row in reader:
            writer.writerow(row)


if __name__ == "__main__":
    # 替换为你的文件夹路径
    root_folder_path = r''
    root_folder_path = Path(root_folder_path)
    process_file(root_folder_path)
