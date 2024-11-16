import pywebio
from pywebio.input import input_group
from pywebio.output import put_markdown, put_button, toast, put_row, put_text, put_column, put_html, popup, use_scope
from pywebio.pin import put_actions, put_input, put_select

data = [
    {"流水号": "GCSQ2024-08-15-0016", "申请日期": "2023/05/21", "用气人": "张三", "用气性质": "生活用气",
     "经办人": "张三", "提交时间": "2023/05/21",
     "业务进程": {"提交申请": 1, "客户预约": 1, "上门通气": 1, "通气验收": 1}},
    {"流水号": "GCSQ2024-08-15-0017", "申请日期": "2023/05/22", "用气人": "李四", "用气性质": "商业用气",
     "经办人": "李四", "提交时间": "2023/05/22",
     "业务进程": {"提交申请": 2, "客户预约": 1, "上门通气": 1, "通气验收": 1}},
]


def show_details(index):
    """显示详细信息"""
    item = data[index]
    details = f"""
    流水号: {item['流水号']}<br>
    申请日期: {item['申请日期']}<br>
    用气人: {item['用气人']}<br>
    用气性质: {item['用气性质']}<br>
    经办人: {item['经办人']}<br>
    提交时间: {item['提交时间']}<br>
    业务进程: {item['业务进程']}
    """
    toast(details, duration=0, position='right')


def update_status(index, process, status):
    """更新业务进程状态"""
    item = data[index]
    item["业务进程"][process] = status
    display_table(data)
    toast(f"{process}状态已更新为完成！")


def display_table(data_arg):
    with use_scope("table", clear=True):
        """显示数据表格"""
        headers = ['序号', "流水号", "申请日期", "用气人", "用气性质", "经办人", "提交时间", "业务进程", "操作"]

        # 构建表头
        header_row = put_row([put_text(header) for header in headers])

        # 构建数据行
        rows = [header_row]
        for i, item in enumerate(data_arg):
            row = [put_text(i + 1)]  # 添加序号
            for key in headers[1:-2]:
                row.append(put_text(item[key]))
            # 处理业务进程，生成带有颜色的HTML
            business_progress = []
            for process, status in item["业务进程"].items():
                color = {0: 'red', 1: 'gray', 2: 'green'}[status]
                business_progress.append(
                    f'<span class="tag" style="background-color:{color}; color:white; padding:2px 6px; margin-right:5px;">{process}</span>')
            row.append(put_html("".join(business_progress)))
            # 添加操作按钮
            buttons = [put_button("详情", onclick=lambda index=i: show_details(index))]
            if item["业务进程"]["提交申请"] == 1:
                buttons.append(put_button("提交", onclick=lambda index=i: update_status(index, "提交申请", 2)))
            elif item["业务进程"]["客户预约"] < 2 and item["业务进程"]["客户预约"] == 1:
                buttons.append(put_button("预约", onclick=lambda index=i: update_status(index, "客户预约", 2)))
            elif item["业务进程"]["上门通气"] < 2:
                buttons.append(put_button("通气", onclick=lambda index=i: update_status(index, "上门通气", 2)))
            elif item["业务进程"]["通气验收"] < 2 and item["业务进程"]["通气验收"] == 1:
                buttons.append(put_button("验收", onclick=lambda index=i: show_acceptance_popup(index)))
            elif item["业务进程"]["通气验收"] < 2 and item["业务进程"]["通气验收"] == 0:
                buttons.append(put_button("整改", onclick=lambda index=i: show_acceptance_popup(index)))

            row.append(put_row(buttons))
            rows.append(row)
        put_column([put_row(row) for row in rows])


def show_acceptance_popup(index):
    """显示验收弹窗"""

    def on_accept(result):
        status = 2 if result == '成功' else 0
        update_status(index, "通气验收", status)

    popup("验收选择", [
        put_button("成功", onclick=lambda: on_accept('成功')),
        put_button("失败", onclick=lambda: on_accept('失败'))
    ])


def add_application_form():
    """添加新的用气申请表单"""

    def submit_form(fields):
        application = {
            "流水号": fields["id"],
            "申请日期": fields["report_date"],
            "用气人": fields["use_person"],
            "用气性质": fields["nature"],
            "经办人": fields["do_person"],
            "提交时间": fields["summit_date"],
            "业务进程": {
                "提交申请": fields["summit_status"],
                "客户预约": fields["user_appoint_status"],
                "上门通气": fields["user_use_status"],
                "通气验收": fields["user_sure_status"]
            }
        }
        data.append(application)  # 将新数据添加到列表中
        display_table(data)  # 更新表格显示
        toast("申请已成功添加！")
        popup.close()

    popup("新增用气申请",
          put_column(
              [
                  put_input(label="请输入天然气报装申请流水号", name="id", type="text"),
                  put_input(label="请选择申请日期", name="report_date", type="date"),
                  put_input(label="请输入用气人", name="use_person", type="text"),
                  put_select(label="请选择用气性质", name="nature", options=["生活用气", "商业用气", "单位用气"]),
                  put_input(label="请输入经办人", name="do_person", type="text"),
                  put_input(label="请选择提交时间", name="summit_date", type="time"),
                  put_actions(label="提交申请状态", name="summit_status", buttons=[
                      {'label': '未开始', 'value': 0},
                      {'label': '进行中', 'value': 1},
                      {'label': '已完成', 'value': 2}
                  ]),
                  put_actions(label="客户预约状态", name="user_appoint_status", buttons=[
                      {'label': '未开始', 'value': 0},
                      {'label': '进行中', 'value': 1},
                      {'label': '已完成', 'value': 2}
                  ]),
                  put_actions(label="上门通气状态", name="user_use_status", buttons=[
                      {'label': '未开始', 'value': 0},
                      {'label': '进行中', 'value': 1},
                      {'label': '已完成', 'value': 2}
                  ]),
                  put_actions(label="通气验收状态", name="user_sure_status", buttons=[
                      {'label': '未开始', 'value': 0},
                      {'label': '进行中', 'value': 1},
                      {'label': '已完成', 'value': 2}
                  ]),
                  put_button("提交", onclick=lambda: submit_form(input_group.fields))
              ]))


def app():
    put_markdown("# 用气申请")
    put_button("添加用气申请", onclick=lambda: add_application_form())
    display_table(data)


if __name__ == '__main__':
    pywebio.start_server(app, port=8088)
