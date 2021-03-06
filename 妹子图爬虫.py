# 获取第一页的html之后解析出第一页主图片的地址、图库的标题、总页数，然后创建存放图片的文件夹，使用循环下载图片并保存到文件夹中
from bs4 import BeautifulSoup
import requests as r
import os
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

def update_header(referer):
    headers['Referer'] = '{}'.format(referer)

def dic_path(s):
    # windows文件夹命名不能有符号
    sn = ""
    for i in s:
        if i in ['?', '！', '&']:
            continue
        else:
            sn += i
    return sn

url = input('请输入第一页的网址：')
# 获取第一页的数据
res = r.get(url=url, headers=headers)
page_text = res.text
soup = BeautifulSoup(page_text, 'lxml')
# 获取总页数
pagenumber_moban = r'<span>\d\d</span>'
Pattern = re.compile(pagenumber_moban)
match = re.search(Pattern, str(soup))
if match:
    pagenumbers = int(match.group()[6:8])
else:
    pagenumber_moban = r'<span>\d\d\d</span>'
    Pattern = re.compile(pagenumber_moban)
    match = re.search(Pattern, str(soup))
    pagenumbers = int(match.group()[6:9])
print("共有{}张图片".format(pagenumbers))
# 创建文件夹，下载第一页的主图片并保存到文件夹中
page1 = str(soup.find('img', class_='blur'))
l = page1.split('"')
kwd = os.getcwd()
s_d = dic_path(l[1])
os.mkdir(kwd + '\\' + s_d)
image_url = l[7]
img_path = kwd + '\\' + s_d + '\\' + '1.jpg'
update_header(url)
img_data = r.get(url=image_url, headers=headers).content
print('正在下载第1张图片......')
with open(img_path, 'wb') as fp:
    fp.write(img_data)
print('第1张图片下载完成!')
# 下载其余的图片
for p in range(2, pagenumbers + 1):
    url_later = url + '/' + str(p)
    res = r.get(url=url_later, headers=headers)
    page_text = res.text
    update_header(url_later)
    soup = BeautifulSoup(page_text, 'lxml')
    page1 = str(soup.find('img', class_='blur'))
    l = page1.split('"')
    image_url = l[7]
    img_path = kwd + '\\' + s_d + '\\' + str(p) + '.jpg'
    print("正在下载第{}张图片......".format(p))
    img_data = r.get(url=image_url, headers=headers).content
    with open(img_path, 'wb') as fp:
        fp.write(img_data)
    print("第{}张图片下载完成!".format(p))
print("全部{}张图片下载完成！".format(pagenumbers))
