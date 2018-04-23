# _*_ coding:utf-8 _*_
import os
import re
from application.config import LOG
# print(os.path.realpath(__file__))
# dir = os.path.split(os.path.realpath(__file__))
# print(os.path.dirname(__file__))
# print(os.pardir)
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(script_dir)
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "../src/application"))
print(src_dir)
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "../src"))
print(main_dir)

def filter_src_file(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__init__") and \
            not file.startswith("common") and not file.startswith("config"):
                file_list.append(file)
    # file_list.append("main.py")
    return file_list

def filter_unittest_file(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
            # if os.path.splitext(file)[1] == '.py' and file.startswith("test_",0,4)
                file_list.append(file)
    return file_list

def src_abs_path():
    src_file_list = filter_src_file(src_dir)
    # src_list.append(os.path.join(main_dir, 'main.py'))
    # file_dic = {}
    file_abs_path = []
    for file in src_file_list:
        # num = [0, 0]
        file_abs_path.append(os.path.abspath(os.path.join(src_dir, file)))
    file_abs_path.append(os.path.join(main_dir, "main.py"))
    # print(file_abs_path)
    return file_abs_path

def unittest_abs_path():
    unittest_file_list = filter_unittest_file(script_dir)
    # src_list.append(os.path.join(main_dir, 'main.py'))
    # file_dic = {}
    file_abs_path = []
    for file in unittest_file_list:
        # num = [0, 0]
        file_abs_path.append(os.path.abspath(os.path.join(script_dir, file)))
    return file_abs_path



def count_class_method():
    file_dic = {}
    num = [0, 0, 0]  #count all class function
    srcfile_abs_path = src_abs_path()
    for path in srcfile_abs_path:
        functn_list = []
        # print(functn_list)
        filename = os.path.split(path)[-1]
        # print(filename)
        with open(path, 'r', encoding='UTF-8') as file_content:
            code_lines = file_content.readlines()
            # print(path)
            for line in code_lines:
                if line.startswith("class"):
                    result = re.findall(r'class.(.*)\(', line)[0]
                    # print(result)
                    num[0] = num[0] + 1
                    # print(num[0])
                elif line.startswith("def"):
                    # print(line)
                    result = re.findall(r'def.(.*)\(', line)[0]

                    functn_list.append(result)
                    # print(result)
                    # file_list.append()
                    num[1] = num[1] + 1
                    # print(num[1])
                elif line.startswith("    def"):
                    result = re.findall(r'\sdef.(.*)\(', line)[0]
                    if isinstance(result,str) and result and not result.startswith("__"):
                        functn_list.append(result)
                        # print(functn_list)

                    num[2] = num[2] + 1
                    # print(num[2])
        file_dic[filename] = functn_list
    return num, file_dic

def count_unittest_function():
    file_dic = {}
    testfile_abs_path = unittest_abs_path()
    print(testfile_abs_path)
    for path in testfile_abs_path:
        functn_list = []
        # print(functn_list)
        filename = os.path.split(path)[-1]
        # print(filename)
        with open(path, 'r', encoding='UTF-8') as file_content:
            code_lines = file_content.readlines()
            # print(path)
            for line in code_lines:
                if line.startswith("    def"):
                    result = re.findall(r'\sdef.(.*)\(', line)[0]
                    result.startswith("setUp") and not result.startswith("tearDown")
                    functn_list.append(result)
        file_dic[filename] = functn_list
    print(file_dic)
    return file_dic



def match_unitest_file():
    # src_num = count_class_method()[0]
    src_file_dic = count_class_method()[1]
    unittest_file_dic =count_unittest_function()
    src_filename_list = src_file_dic.keys()
    unittest_filename_list = filter_unittest_file(script_dir)
    # print(src_filename_list)
    print(src_file_dic)
    for name in src_filename_list:
        name = "test_" + name
        # print(name)
        if name in unittest_filename_list:
            for method_name in src_file_dic[name[5:]]:
                if method_name not in unittest_file_dic[name]:
                    src_file_name = name[5:]
                    # print(src_file_name)
                    # print(method_name)
                    print("src目录下模块%s的%s在单元测试中没有调用"%(src_file_name, method_name))
        else:
            print("src目录下模块%s缺少单元测试用例"%(name[5:]))


    # print(src_num)
    # print(type(src_file_dic))
    # print(src_filename_list)


if __name__ == '__main__':
    # filter_unittest_file(script_dir)
    # print(filter_src_file(src_dir))
    # search_src_name()
    # search_unittest_name()
    # src_abs_path()
    # string = "xxxxxxxxxxxxxxxxxxxxxxxx entry '某某内容' for aaaaaaaaaaaaaaaaaa"
    # result = re.findall(".*entry(.*)for.*", string)
    # for x in result:
    #     print(x)
    # match_unitest_file()
    # match_unitest_file()
    match_unitest_file()

