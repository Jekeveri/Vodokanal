import datetime
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.bd_server_user
import scr.toggle_user_sessions
import scr.func
import scr.navigation_apps.users.doing_work.chose_meters


def sealing(page, id_task, meter_id, where):
    screen_width = page.width
    screen_height = page.height

    result_meters = scr.BD.bd_users.local.select_bd.select_meters_data_new_for_one(id_task, meter_id)
    if result_meters:
        for result in result_meters:
            id_meters, meter_number, instalation_day, meter_type, id_address, marka, seal_number, \
                date_next_verification, location, status_filling, meter_remark, type_protection = result
    result_info_meters = f"Счетчик: {marka} \nДата установки: {instalation_day} \nТип: {meter_type}"

    if type_protection is True:
        seal_type = "роторную"
    else:
        seal_type = "антимагнитную пломбу"

    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    marka_checkbox = ft.Ref[ft.Checkbox]()
    serial_number_checkbox = ft.Ref[ft.Checkbox]()
    installation_checkbox = ft.Ref[ft.Checkbox]()
    star_checkbox = ft.Ref[ft.Checkbox]()

    dict_checkboxes["marka"] = False
    dict_checkboxes["serial_number"] = False
    dict_checkboxes["installation"] = False
    dict_checkboxes["star"] = False

    content_question = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="marka": on_checkbox_change(e.control, name),
                                            ref=marka_checkbox),
                                ft.Text("Марка счетчика совпадает с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{marka}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                on_click=lambda e, name="marka": toggle_checkbox(e, marka_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="serial_number": on_checkbox_change(e.control, name),
                                    ref=serial_number_checkbox),
                                ft.Text("Заводской номер счетчика"),
                            ]),
                            ft.Row([
                                ft.Text("совпадает с "),
                                ft.Text(f"{meter_number}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                on_click=lambda e, name="serial_number": toggle_checkbox(e, serial_number_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="installation": on_checkbox_change(e.control, name),
                                    ref=installation_checkbox),
                                ft.Text("Прибор учета устрановлен"),
                            ]),
                            ft.Row([
                                ft.Text("по протоколу?"),
                            ]),
                        ]
                    ),
                on_click=lambda e, name="seal": toggle_checkbox(e, installation_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="star": on_checkbox_change(e.control, name),
                                            ref=star_checkbox),
                                ft.Text("Сигнальная звезочка"),
                            ]),
                            ft.Row([
                                ft.Text("вращается равномерно? "),
                            ]),
                        ]
                    ),
                on_click=lambda e, name="seal": toggle_checkbox(e, star_checkbox.current, name)
            )
        ]
    )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        if not chect_list:
            page.close(check_meters_data)
        for chect in chect_list:
            if chect == "marka":
                message_string += "Включите в акт несоответствие Марки счетчика\n"
            elif chect == "serial_number":
                message_string += "Включите в акт несоответствие Заводского номера\n"
            elif chect == "installation":
                message_string += "Включите в акт информацию о неправильной установки прибора учета\n"
            elif chect == "star":
                message_string += "Включите в акт информацию о некоректной работе звездочки\n"
        page.close(check_meters_data)
        page.open(alert)
        page.open(seal_al)
        scr.func.show_alert_yn(page, message_string)

    def button_no(e):
        page.close(check_meters_data)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    check_meters_data = ft.AlertDialog(
        modal=True,
        content=content_question,
        title=ft.Text("Проверте работоспособность счетчика"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Ввод прибора учета",
                                      on_click=button_yes,
                                      bgcolor=ft.colors.BLUE_200,
                                      width=screen_width*0.30
                                      ),
                    ft.ElevatedButton("Назад",
                                      on_click=button_no,
                                      bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    def close(e):
        page.close(seal_al)
        page.open(alert)

    def not_installed(e):
        page.close(seal_al)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    seal_al = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Установите {seal_type} пломбу"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Установлена", on_click=close, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=not_installed, bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    title = ft.Column(
        [
            ft.Text(result_info_meters, size=17),
        ]
    )

    seal_number_new = ft.TextField(label="Номер пломбы", )
    type_seal = ft.TextField(label="Тип пломбы", value=seal_type, multiline=True, min_lines=1,
                             max_lines=3)
    remark = ft.TextField(label="Примечание", value=meter_remark, multiline=True, min_lines=1,
                          max_lines=3)

    content = ft.Column(
        [
            seal_number_new,
            type_seal,
            remark
        ]
    )

    def on_click_save(e):
        if seal_number_new.value is None:
            seal_number_new.error_text = "Введите номер пломбы"
        else:
            scr.BD.bd_users.local.update_bd.update_seal(seal_number_new.value, meter_id, id_task, remark.value)
        page.close(alert)

    def on_click_back(e):
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    alert = ft.AlertDialog(
        modal=True,
        title=title,
        content=content,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_save),
                    ft.ElevatedButton("Назад", on_click=on_click_back)
                ]
            )
        ]
    )
    page.open(check_meters_data)

    page.update()
