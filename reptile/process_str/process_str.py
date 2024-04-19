import os

file_count = 1
import time

def remove_content(text):
    start_index = text.find("##", text.find("##") + 2) + 2
    # print(start_index)
    end_index = text.find("引领项目管理发展。") + 9
    # print(end_index)
    if start_index < 0 or end_index < 0:
        return text  # 未找到匹配内容，返回原字符串
    return text[:start_index] + '\n' + text[end_index:]


def process_file(file_path):
    temp_list = []
    # i = 0
    with open(file_path, "r+", encoding="utf-8") as f:  # 使用 "r+" 模式，既可读取也可写入
        while True:
            line = f.readline()
            if line != '\n':
                # i += 1
                result = remove_content(line).rstrip()
                # print(result.rstrip())
                temp_list.append(result)
                if not line:  # 如果读取到文件末尾，则退出循环
                    break
        # print(i)
    return temp_list


if __name__ == "__main__":
    i = 0
    folder_path = r"C:\Users\wuxd-a\PycharmProjects\pythonProject6\reptile\process_str\final_txtdata"
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            re_list = process_file(file_path)
            # print(re)
            # print(len(re))
            with open(os.path.join(r'C:\Users\wuxd-a\PycharmProjects\pythonProject6\reptile\process_str\ceshi\fin', f"content_{i}"), 'a', encoding='utf-8') as f:
                for item in re_list:
                    f.write(str(item) + "\n")
            i += 1
            time.sleep(1)

        print(i)
