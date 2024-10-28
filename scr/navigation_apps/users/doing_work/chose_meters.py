import datetime
import flet as ft
import scr.BD.bd_users.update_bd
import scr.BD.bd_users.delete_bd
import scr.BD.bd_users.insert_bd
import scr.BD.bd_users.select_bd
import scr.BD.bd_server
import scr.toggle_user_sessions
import scr.func
import scr.constants as const
import scr.navigation_apps.users.pages.main_users_screen
import scr.navigation_apps.users.pages.future_user_screen
import scr.navigation_apps.users.doing_work.update_data_meters
import scr.navigation_apps.users.doing_work.sealing_meter


def call_show_meters_data(page, id_task, where):
    show_meters_data(page, id_task, where)


def show_meters_data(page, id_task, where):
    screen_width = page.width
    screen_height = page.height
    page.controls.clear()
    results_meters_data = scr.BD.bd_users.select_bd.select_meters_data_new(id_task)
    results_address_data = scr.BD.bd_users.select_bd.select_tasks_data_for_one(id_task)

    filtered_results = [
        result_address_data for result_address_data in results_address_data
    ]

    for result in filtered_results:
        id_task, person_name, street, dom, apartment, phone_number, \
            personal_account, date, remark, status, purpose, registered_residing, \
            status_address, standarts, area, saldo, type_address = result
    result_info_address = f"Адрес: ул.{street} д.{dom} кв.{apartment}"
    result_info_person = f"ФИО владельца: {person_name}"

    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    fio_checkbox = ft.Ref[ft.Checkbox]()
    residing_checkbox = ft.Ref[ft.Checkbox]()
    standarts_checkbox = ft.Ref[ft.Checkbox]()
    area_checkbox = ft.Ref[ft.Checkbox]()

    if type_address == "МКД":
        dict_checkboxes["FIO"] = False
        dict_checkboxes["registered_residing"] = False
        dict_checkboxes["standarts"] = False

        content = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="FIO": on_checkbox_change(e.control, name),
                                            ref=fio_checkbox),
                                ft.Text("ФИО совпадает с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{person_name}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ])
                        ]
                    ),
                    on_click=lambda e, name="FIO": toggle_checkbox(e, fio_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="registered_residing": on_checkbox_change(e.control, name),
                                    ref=residing_checkbox),
                                ft.Text("Количество прописанных "),
                            ]),
                            ft.Row([
                                ft.Text("/проживающих совпадает с "),
                                ft.Text(f"{registered_residing}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="registered_residing": toggle_checkbox(e, residing_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="standarts": on_checkbox_change(e.control, name),
                                            ref=standarts_checkbox),
                                ft.Text("Нормативы совпадают с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{standarts}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="standarts": toggle_checkbox(e, standarts_checkbox.current, name)
                )
            ]
        )
    elif type_address == "ЧС":
        dict_checkboxes["FIO"] = False
        dict_checkboxes["registered_residing"] = False
        dict_checkboxes["standarts"] = False
        dict_checkboxes["area"] = False
        content = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="FIO": on_checkbox_change(e.control, name),
                                            ref=fio_checkbox),
                                ft.Text("ФИО совпадает с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{person_name}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ])
                        ]
                    ),
                    on_click=lambda e, name="FIO": toggle_checkbox(e, fio_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(
                                    on_change=lambda e, name="registered_residing": on_checkbox_change(e.control, name),
                                    ref=residing_checkbox),
                                ft.Text("Количество прописанных "),
                            ]),
                            ft.Row([
                                ft.Text("/проживающих совпадает с "),
                                ft.Text(f"{registered_residing}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="registered_residing": toggle_checkbox(e, residing_checkbox.current, name)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="standarts": on_checkbox_change(e.control, name),
                                            ref=standarts_checkbox),
                                ft.Text("Нормативы совпадают с "),
                            ]),
                            ft.Row([
                                ft.Text(f"{standarts}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),
                    on_click=lambda e, name="standarts": toggle_checkbox(e, standarts_checkbox.current, name)
                ),
                ft.Container(
                    content=
                    ft.Column(
                        [
                            ft.Row([
                                ft.Checkbox(on_change=lambda e, name="area": on_checkbox_change(e.control, name),
                                            ref=area_checkbox),
                                ft.Text("Площадь без построек "),

                            ]),
                            ft.Row([
                                ft.Text("совпадает с "),
                                ft.Text(f"{area}", weight=ft.FontWeight.BOLD),
                                ft.Text("?")
                            ]),
                        ]
                    ),

                    on_click=lambda e, name="area": toggle_checkbox(e, area_checkbox.current, name)
                ),
            ]
        )
    else:
        dict_checkboxes["FIO"] = False
        content = ft.Column(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Checkbox(on_change=lambda e, name="FIO": on_checkbox_change(e.control, name),
                                    ref=fio_checkbox),
                        ft.Text("ФИО совпадает с "),
                        ft.Text(f"{person_name}", weight=ft.FontWeight.BOLD),
                        ft.Text("?")
                    ]),
                    on_click=lambda e, name="FIO": toggle_checkbox(e, fio_checkbox.current, name)
                )
            ]
        )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        if not chect_list:
            page.close(check_address_data)
        else:
            for chect in chect_list:
                if chect == "FIO":
                    message_string += "Включите в акт пердписание о несоответствии ФИО\n"
                elif chect == "registered_residing":
                    message_string += "Включите в акт несоответствие количества прописанных\n"
                elif chect == "standarts":
                    message_string += "Включите в акт несоответствие с нормативами\n"
                elif chect == "area" and type_address == "ЧС":
                    message_string += "Включите в акт несоответствие площади\n"
            scr.func.show_alert_yn(page, message_string)
            page.close(check_address_data)

    def button_no(e):
        page.close(check_address_data)
        if where == "task":
            scr.navigation_apps.users.pages.main_users_screen.user_main(page)
        else:
            scr.navigation_apps.users.pages.future_user_screen.main(page)

    check_address_data = ft.AlertDialog(
        modal=True,
        content=content,
        title=ft.Text("Уточните Данные"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Да", on_click=button_yes, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=button_no, bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        inset_padding=screen_width*0.10
    )
    page.open(check_address_data)

    def on_click_back(e):
        if where == "task":
            scr.navigation_apps.users.pages.main_users_screen.user_main(page)
        else:
            scr.navigation_apps.users.pages.future_user_screen.main(page)

    def on_click_save(e):
        scr.BD.bd_users.update_bd.update_dop_data_address(
            remark_textfield.value, registered_residing_textfield.value, standarts_textfield.value,
            area_textfield.value, id_address, id_task)
        call_show_meters_data(page, id_task, where)
        page.update()

    button_back = ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
    button_save = ft.ElevatedButton("Сохранить", on_click=on_click_save, bgcolor=ft.colors.BLUE_200, visible=False)
    filtered_results_meters = [result for result in results_meters_data]
    column = ft.Column(scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    color = ft.colors.GREY
    column.controls.clear()

    def on_change_dop_data(e):
        button_save.visible = True
        page.update()

    for result in filtered_results_meters:
        id_meters, meter_number, instalation_day, meter_type, id_address, marka, seal_number, \
            date_next_verification, location, status_filling, meter_remark, type_protection = result

        if status_filling == 'выполнен':
            color = const.tasks_completed_color
        elif status_filling == 'в_исполнении':
            color = const.tasks_unloaded_color
        else:
            color = const.tasks_pending_color

        result_info_meters = f"Марка: {marka}\nЗаводской номер: {meter_number}\nТип: {meter_type}"

        row_to_container = ft.Column(
            [
                ft.Text(result_info_meters, size=17, ),
            ],
        )

        # Используем замыкание для передачи правильного apartment
        def create_on_click(id_task, id_meters):
            def on_click(e):
                if purpose == "Контрольный съем показаний":
                    scr.navigation_apps.users.doing_work.update_data_meters.update_data(page, id_meters, id_task, where)
                elif purpose == "Повторная опломбировка":
                    scr.navigation_apps.users.doing_work.sealing_meter.sealing(page, id_task, id_meters, where)

            return on_click

        on_click_container = create_on_click(id_task, id_meters)

        container = ft.Container(
            content=row_to_container,
            padding=ft.padding.only(top=20, left=50, right=50, bottom=20),
            margin=5,
            border_radius=15,
            bgcolor=color,
            ink=True,
            shadow=ft.BoxShadow(
                offset=ft.Offset(0, 7),
                blur_radius=10,
                color=ft.colors.BLACK38
            ),
            alignment=ft.alignment.center,
            on_click=on_click_container
        )
        column.controls.append(container)

    remark_textfield = ft.TextField(label="Примечание", value=remark, on_change=on_change_dop_data)
    registered_residing_textfield = ft.TextField(label="Прописанно", value=registered_residing,
                                                 on_change=on_change_dop_data)
    for i in const.norma_water_supply:
        if i == standarts:
            standarts = i
    standarts_textfield = ft.Dropdown(
        on_change=on_change_dop_data,
        label="Нормативы",
        value=standarts,
        options=[
            ft.dropdown.Option(value) for value in const.norma_water_supply
        ],
    )
    content_standarts = ft.Column()
    standarts_setting = ft.AlertDialog(
        title=ft.Text("Определение нормативов"),
        content=content_standarts,
    )
    area_textfield = ft.TextField(label="Площадь", value=area, on_change=on_change_dop_data)
    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    remark_textfield,
                    registered_residing_textfield,
                    standarts_textfield,
                    area_textfield

                ]
            )
        ]
    )
    panels = [
        ft.ExpansionPanel(
            header=ft.Row(
                [
                    ft.Text("Редактирование данных адреса")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
            can_tap_header=True,
            content=dop_buttons_redact,
            expanded=False,
            aspect_ratio=100,
            bgcolor=ft.colors.BLUE_100,
        ),
    ]
    panel_list = ft.ExpansionPanelList(
        elevation=25,
        controls=panels,
        expanded_header_padding=3
    )
    container = ft.Container(
        content=panel_list,
        width=screen_width * 0.9,
        border_radius=15,
    )
    column.controls.append(container)
    content_dialog = column
    title = ft.Column(
        [
            ft.Text(result_info_address, size=17, ),
            ft.Text(result_info_person, size=17, ),
            ft.Text(f"Номер телефона владельца {phone_number}", size=17, ),
            ft.Text(f"Примечание по адрессу: {remark}", size=17, ),
        ]
    )
    row_button = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    row_button.controls.append(button_save)
    row_button.controls.append(button_back)

    page.add(
        ft.Column(
            [
                title,
                content_dialog,
                row_button
            ],
            scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()
