# 获取第一页的html之后解析出第一页主图片的地址、图库的标题、总页数，然后创建存放图片的文件夹，使用循环下载图片并保存到文件夹中
from bs4 import BeautifulSoup
import requests as r
import os
import re
from random import choice

UserAgent = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.111 YaBrowser/21.2.1.107 Yowser/2.5 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"]
headers = {"User-Agent": choice(UserAgent)}


def update_header(referer):
    headers['Referer'] = '{}'.format(referer)


def dic_path(s):
    # windows文件夹命名不能有符号
    sn = ""
    for i in s:
        if i in ['?', '&']:
            continue
        else:
            sn += i
    return sn


def mzitu_pachong_single(url):
    # 获取第一页的数据
    res = r.get(url=url, headers=headers)
    page_text = res.text
    soup = BeautifulSoup(page_text, 'lxml')
    # 获取总页数
    pagenumber_moban = r'<span>\d\d</span>'
    pattern = re.compile(pagenumber_moban)
    match = re.search(pattern, str(soup))
    if match:
        pagenumbers = int(match.group()[6:8])
    else:
        pagenumber_moban = r'<span>\d\d\d</span>'
        pattern = re.compile(pagenumber_moban)
        match = re.search(pattern, str(soup))
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
    print('正在下载第1张图片......')
    img_data = r.get(url=image_url, headers=headers).content
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


if __name__ == '__main__':
    url = input('请输入第一页的网址：')
    mzitu_pachong_single(url)
