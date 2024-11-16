import pywebio
from pywebio.output import put_html
from pyecharts import options as opts
from pyecharts.charts import Tree

data = [
    {
        "children": [
            {"name": "龙"},
            {
                "children": [
                    {"children": [
                        {"name": "小猫"}
                    ], "name": "大猫"},
                    {"name": "黑猫"}
                ],
                "name": "猫",
            },
            {
                "children": [
                    {"children": [
                        {"name": "小狗"}, {"name": "黑狗"}
                    ], "name": "白狗"},
                    {"name": "大狗"},
                ],
                "name": "狗",
            },
        ],
        "name": "动物",
    }
]

c = (
    Tree()
    .add("", data)
    .set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例"))
)

c.width = "100%"


def display_tree():
    put_html(c.render_notebook())


if __name__ == '__main__':
    pywebio.start_server(display_tree, port=8088)
