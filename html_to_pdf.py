from __future__ import unicode_literals

__author__ = 'Dzreal'
__date__ = '2018-06-16 20:52'

# coding=utf-8

import os, sys, re, time
import requests, codecs
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pdfkit
import platform

requests.packages.urllib3.disable_warnings()

system = platform.system()
print(sys.getdefaultencoding())

str_encode = 'gbk' if system is 'Windows' else 'utf-8'
print(str_encode)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body style="border:0; margin:0;">
    {content}
</body>
</html>

"""
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'output')):
    os.mkdir(os.path.join(os.path.dirname(__file__), 'output'))

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'htmls')):
    os.mkdir(os.path.join(os.path.dirname(__file__), 'htmls'))


def parse_url(url, name, target='body'):
    '''
    解析url并生成新的html文件
    :param url: 抓取页面的url
    :param name: 生成目标html的文件名
    :param target: 抓取的目标DOM
    :return:返回 '文件路径/文件名' str
    '''

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        target_content = soup.find_all(target)
        h_list = str(target_content)
        html = h_list[1:-1]
        html = html_template.format(content=html)
        html = html.encode("utf-8")

        with open('{}/{}'.format(os.path.join(os.path.dirname(__file__), 'htmls'), name), 'wb') as f:
            f.write(html)
        return '{}/{}'.format(os.path.join(os.path.dirname(__file__), 'htmls'), name)
    except Exception as e:
        print(e)


def save_pdf(htmls, file_name):
    '''
    生成pdf文档
    :param htmls:
    :param file_name:
    :return:
    '''
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    file_name = '{}/{}'.format(os.path.join(os.path.dirname(__file__), 'output'), file_name)
    path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # wkhtmltopdf安装位置
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    pdfkit.from_file(htmls, file_name, options=options, configuration=config)


if __name__ == '__main__':
    start_url = 'https://gitdzreal93.github.io/pages/resume.html'
    name = 'Dzreal_resume.html'
    html = parse_url(start_url, name, 'article')
    pdf_name = '应聘-测试开发工程师-黄大臻-17777130735.pdf'

    try:
        save_pdf(html, pdf_name)
    except Exception as e:
        print(e)
