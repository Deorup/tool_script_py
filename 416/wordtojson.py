import docx
import re
import os
import json
import cn2an
from pprint import pprint


class WordToJson:
    def __init__(self):
        pass

    def word_to_txt(self, src_filepath, dst_filepath=os.getcwd(), flag=False):
        if not os.path.exists(src_filepath):
            raise FileNotFoundError(f"File not found: {src_filepath}")

        #  打开word文档，追加写入txt (为空才写)
        folder_path = os.path.join(dst_filepath, "data")
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        txt_file_path = os.path.join(folder_path, "建筑施工安全事故案例分析.txt")
        with (open(txt_file_path, "a", encoding="utf-8") as f):
            file_size = os.path.getsize(txt_file_path)
            if file_size != 0 and flag is False:
                print("txt file not empty,如")
                return txt_file_path
            document = docx.Document(src_filepath)
            for paragraph in document.paragraphs:
                paragraph_text = paragraph.text.strip()
                # skip 目录
                if (paragraph_text.startswith("案例") and paragraph_text[-1].isdigit()
                        or paragraph_text.startswith(("第", "目录"))):
                    continue
                # 写入txt
                f.write(paragraph_text)
        f.close()

        return txt_file_path

    def split_by_markers(self, text, markers):
        # 使用 re.escape() 函数对每个标记进行转义，确保特殊字符被正确解析。
        pattern = f"|".join(re.escape(marker) for marker in markers)
        # print(pattern)
        return re.split(pattern, text)

    def string_to_json(self, one_case_str):
        dict = {
            'id': '',
            'title': '',
            'info':
                {
                    'introduction': '',
                    'cause': {
                        'direct_cause': '',
                        'indirect_cause': ''
                    },
                    'lessons': '',
                    'expert_reviews': '',
                }
        }
        # print(one_case_str[1])
        for i in range(len(one_case_str)):
            # id 和 title
            if i == 0:
                parts = one_case_str[i].split("：")
                tem_str = re.sub(r'[案例]+', '', parts[0]).replace("^", "十")
                dict['id'] = cn2an.cn2an(tem_str)
                dict['title'] = parts[1]
            else:
                # 'introduction
                if one_case_str[i].startswith("事故简介"):
                    # 取出后面的内容
                    pattern = r'事故简介(.*)'
                    match = re.search(pattern, one_case_str[i])
                    dict['info']['introduction'] = match.group(1)

                elif one_case_str[i].startswith(("原因分析", "事故原因")):
                    parts = one_case_str[i].split("间接原因")
                    pattern = r'直接原因(.*)'  # 使用正则表达式匹配"直接原因"之后的内容
                    match = re.search(pattern, parts[0])
                    direct_str = ''
                    result = match.group(1)
                    # 处理字符串末多余字符
                    for j, char in enumerate(reversed(result)):
                        if char == "。":
                            direct_str = result[:-j - 1]
                            break
                    dict['info']['cause']['direct_cause'] = direct_str + '。'
                    dict['info']['cause']['indirect_cause'] = parts[1]

                # lessons
                elif one_case_str[i].startswith("事故教训"):
                    pattern = r'事故教训(.*)'
                    match = re.search(pattern, one_case_str[i])
                    dict['info']['lessons'] = re.sub(r"[^\u4e00-\u9fff]", '', match.group(1)) + '。'

                # expert_reviews
                elif one_case_str[i].startswith("专家点评"):
                    pattern = r'专家点评(.*)'
                    match = re.search(pattern, one_case_str[i])
                    dict['info']['expert_reviews'] = match.group(1) + '。'
                else:
                    pass
        return dict

    def txt_to_json(self, txt_file_path):
        # 打开txt文档
        with open(txt_file_path, 'r', encoding='utf-8') as src_file:
            all_text = ""
            for line in src_file:
                all_text += line

            # 将string 分割成单个案例
            case_list = re.split(r'。案例', all_text)
            # i = 0 # 测试用
            # 每次处理一个案例内容
            temp_list = []
            for item in case_list:
                item = re.sub(r'\s+', '', item)  # 删除空格
                markers = ["一、", "二、", "三、", "四、", "五、", "六、", "七、", "八、"]  # 分割一个案例下的副标题
                split_text = self.split_by_markers(item, markers)  # return一个字符串列表
                dict_data = self.string_to_json(split_text)
                # i = i + 1 # 测试用
                # print(i) # 测试用
                # 追加写入到一个列表中
                temp_list.append(dict_data)

            # 写入json文件
            with open(os.path.join(os.path.dirname(os.path.abspath(txt_file_path)), '建筑施工安全事故案例分析11.json'), mode='w',
                      encoding='utf-8') as f:  # 将列表里储存的字典一次性写入.json
                print("写入json")
                json.dump(temp_list, f, indent=4, ensure_ascii=False)
            f.close()
        src_file.close()


if __name__ == "__main__":
    src_path = r"D:\GITcode\DEPP\word to json\建筑施工安全事故案例分析.docx"  # doc文档所在路径
    final_json_path = r""  # 最终生成路径,默认为当前路径
    wordtojson = WordToJson()
    # 对于多个同类型json文件,应该循环先写入一个txt中,在一次写入json
    # false处理单个文件，true处理多个文件
    txt_file_path = wordtojson.word_to_txt(src_path, flag=True)
    wordtojson.txt_to_json(txt_file_path)
    # print(txt_file_path)
