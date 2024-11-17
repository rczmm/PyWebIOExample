import os

import frontmatter
from pywebio import start_server
from pywebio.output import *


def nav():
    # 导航栏
    put_html('''
        <nav style="background-color: #333; color: white; padding: 10px;">
            <div style="max-width: 1200px; margin: auto; display: flex; align-items: center;">
                <img src="https://example.com/logo.png" alt="Podcast Logo" style="width: 50px; height: 50px; margin-right: 20px;">
                <h1 style="margin: 0;">播客标题</h1>
                <div style="flex-grow: 1;"></div>
                <a href="#all" style="color: white; text-decoration: none; margin-right: 20px;">全部</a>
                <a href="#category" style="color: white; text-decoration: none; margin-right: 20px;">分类</a>
                <a href="#share" style="color: white; text-decoration: none;">分享</a>
            </div>
        </nav>
    ''')


def read_markdown_file() -> list:
    """

    :rtype: list
    """
    files = [f for f in os.listdir('post') if f.endswith('.md')]
    podcast_list = []
    for file in files:
        with open(os.path.join('post', file), 'r', encoding='utf-8') as f:
            content = f.read()
            md_content = frontmatter.Frontmatter.read(content)
            post_meta = md_content.get('attributes')
            post_body = md_content.get('body')
            podcast = {
                'title': post_meta['title'],
                'description': post_meta['desc'],
                'date': post_meta['date'],
                'body': post_body,
            }
            podcast_list.append(podcast)
    return podcast_list


def show_details(body_arg):
    toast('点击了查看全部播客按钮', duration=3)
    clear()
    nav()
    put_markdown(body_arg)


def podcast_page(podcast_list_arg):
    nav()

    # 页面主体内容
    put_markdown('## 欢迎来到我们的播客平台！')
    put_text('在这里，你可以发现各种类型的播客内容...')

    for podcast in podcast_list_arg:
        put_markdown(f"""
        ### {podcast['title']}
        - **日期**: {podcast['date']}
        - **描述**: {podcast['description']}
        ---
        """)
        put_button(label='查看全文', onclick=lambda: show_details(podcast['body']),
                   color='info', outline=True)


def index():
    podcast_list = read_markdown_file()
    podcast_page(podcast_list)


if __name__ == '__main__':
    start_server(index, port=8080, debug=True)
