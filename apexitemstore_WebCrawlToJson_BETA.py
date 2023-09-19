# 1.爬取apexitemstore中<h3>Limited-Time</h3>下的内容
# 2.转存至JSON文件
# 3.在JS中调用JSON

import requests
from bs4 import BeautifulSoup
import re
from github import Github
import json

# 发送HTTP请求并获取网页内容
url = 'https://apexitemstore.com/'
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 查找 <h3>Limited-Time</h3> 标签
h3_tags = soup.find('h3', string='Limited-Time')

recolor_id_list = []
recolor_id_dict = {}

for p_tag in h3_tags.find_next_siblings('p', limit=1):#遍历<h3>Limited-Time</h3>下属第一个p标签
    a_tag = p_tag.find_all(name='a')#找出目标p标签下第一个a标签
    for link in a_tag:#遍历目标a标签中的链接
        href = link.get('href')
        href_str =re.search(r'/(?P<content>[^/]+)/$', href)
        if href_str:
            desired_content = href_str.group('content')
            recolor_id = desired_content.replace('-',' ')
            recolor_id = recolor_id.title()  # 大写首字母
            recolor_id_list.append(recolor_id)

recolor_id = recolor_id_list
recolor_dict = {index: value for index, value in enumerate(recolor_id)}
# print(recolor_dict)
"""
<-----以上爬虫apexitem网页指定内容并格式化为字典代码已成功--->
"""


# GitHub账号信息
token = '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'
repository_name = 'for_heybox_apex'
file_name = 'apex_legends-recolor_dict.json'
# 将Python对象转换为JSON
json_data = json.dumps(recolor_dict, indent=4)
# 创建GitHub实例
g = Github(token)
# 获取指定仓库
repo = g.get_user().get_repo(repository_name)

# 检查文件是否存在
file_exists = False
contents = repo.get_contents("")
for content_file in contents:
    if content_file.path == file_name:
        file_exists = True
        break

if file_exists:
    # 更新文件内容
    file = repo.get_contents(file_name)
    updated_data = {f"skin_id_{key}": value for key, value in json.loads(json_data).items()}
    updated_json_data = json.dumps(updated_data, indent=4)
    repo.update_file(file.path, "Update file", updated_json_data, file.sha)
else:
    # 创建新文件
    new_data = {f"new_id_{key}": value for key, value in json.loads(json_data).items()}
    new_json_data = json.dumps(new_data, indent=4)
    repo.create_file(file_name, "Create file", new_json_data)

print("JSON已成功写入GitHub托管库！")

