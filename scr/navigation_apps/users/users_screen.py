import datetime

import flet as ft

import scr.BD.bd_user
import scr.BD.bd_server
import scr.exit
import scr.func
import scr.constants as const


def show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number, remark, result_address):
    screen_width = page.width
    screen_height = page.height
    page.controls.clear()
    results = scr.BD.bd_user.select_meters_data_new(id_task)

    def on_click_back(e):
        user_main(page)
        user_main(page)

    button_back = ft.ElevatedButton("Back", on_click=on_click_back, bgcolor=ft.colors.RED_200)
    filtered_results = [result for result in results]
    column = ft.Column(scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    color = ft.colors.GREY
    column.controls.clear()

    def on_click_add(e):
        scr.func.show_alert_yn(page, "Заполните новый счетчик", id_task)
        page.update()

    button_add = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=on_click_add,
                                         bgcolor=ft.colors.LIME_300)
    for result in filtered_results:
        id_meters, meter_number, instalation_day, meter_type, id_address, marka, seal_number, \
            date_next_verification, location, saldo, status_filling, meter_remark = result

        if status_filling == 'выполнен':
            color = const.tasks_fulfilled_color
        elif status_filling == 'в_исполнении':
            color = const.tasks_unloaded_color
        else:
            color = const.tasks_pending_color

        result_info_meters = f"Счетчик: {meter_number} Дата установки: {instalation_day} Тип: {meter_type}"

        row_to_container = ft.Column(
            [
                ft.Text(f"Номер: {id_meters}", size=17, ),
                ft.Text(result_info_meters, size=17, ),
            ],
        )

        # Используем замыкание для передачи правильного apartment
        def create_on_click(id_task, id_meters, result_info_meters, result_tasks_info, phone_number, meter_remark,
                            remark, result_address):
            def on_click(e):
                update_data(page, id_meters, result_info_meters, id_task, result_info_address, result_tasks_info,
                            phone_number, meter_remark, remark, result_address)

            return on_click

        on_click_container = create_on_click(id_task, id_meters, result_info_meters, result_tasks_info, phone_number,
                                             meter_remark, remark, result_address)

        row = ft.Row(
            [
                ft.Container(
                    content=row_to_container,
                    padding=10,
                    margin=5,
                    border_radius=15,
                    bgcolor=color,
                    ink=True,
                    on_click=on_click_container
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        column.controls.append(row)
    filtered_results = [
        result for result in result_address
    ]
    for resultt in filtered_results:
        id_task, person_name, street, dom, apartment, phone_number,personal_account, date, remark, status, purpose, registered_residing,status, standarts, area = resultt
    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    ft.TextField(label="Сальдо", value=saldo),
                    ft.TextField(label="Прописанно", value=registered_residing),
                    ft.TextField(label="Нормативы", value=standarts),
                    ft.TextField(label="Площадь", value=area),
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
    column.controls.append(button_add)
    column.controls.append(container)
    content_dialog = column
    title = ft.Column(
        [
            ft.Text(result_tasks_info, size=17, ),
            ft.Text(result_info_address, size=17, ),
            ft.Text(f"{phone_number}", size=17, ),
            ft.Text(f"Примечание по адрессу: {remark}", size=17, ),
        ]
    )
    row_button = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
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


m_value = ""
m_remark = ""


def update_data(page, meter_id, result_info_meters, id_task, result_info_address, result_tasks_info,
                phone_number, meter_remark, task_remark, result_address):
    today = datetime.datetime.now().strftime("%H:%M:%S")
    screen_width = page.width
    screen_height = page.height

    def bottom_sheet_yes(e):
        page.close(bottom_sheet)
        page.close(dlg_modal)
        show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number, task_remark, result_address)

    def bottom_sheet_no(e):
        page.close(bottom_sheet)

    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Вы точно хотите выйти?"),
                    ft.Text("Не сохраненные данные удалятся!"),
                    ft.Row(
                        [
                            ft.ElevatedButton("Да", on_click=bottom_sheet_yes),
                            ft.ElevatedButton("Нет", on_click=bottom_sheet_no)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
            ),
        ),
    )

    def on_click_time_task(e):
        today = datetime.datetime.now().strftime("%H:%M:%S")
        if remark.value != "" and reading_value.value != "":
            global m_remark, m_value
            m_value = reading_value.value
            m_remark = remark.value
            scr.BD.bd_user.update_local_tasks(str(today), id_task, reading_value.value, remark.value, meter_id)
            show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number, task_remark, result_address)
            page.close(dlg_modal)
            page.update()

    def on_click_back(e):
        if reading_value.value != m_value or remark.value != m_remark:
            page.open(bottom_sheet)
        else:
            page.close(dlg_modal)
            show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number, task_remark, result_address)

    results = scr.BD.bd_user.select_meter_reading_new(meter_id)
    filtered_results = [result for result in results]
    for result in filtered_results:
        id_meters, last_reading_date, last_reading_value, new_reading_date, new_reading_value = result

    reading_value = ft.TextField(label="Показания счетчика", value=new_reading_value, )
    remark = ft.TextField(label="Примечания по счетчику", value=meter_remark)

    title = ft.Column(
        [
            ft.Text(f"Номер: {meter_id}", size=17, ),
            ft.Text(result_info_meters, size=17, ),
        ]
    )

    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    ft.ElevatedButton("Марка"),
                    ft.ElevatedButton("Заводской номер"),
                    ft.ElevatedButton("Номер пломбы"),
                    ft.ElevatedButton("Место расположение"),
                    ft.ElevatedButton("Тип услуги"),
                ]
            )
        ]
    )
    panels = [
        ft.ExpansionPanel(
            header=ft.Text("Редактирование данных счётчика"),
            can_tap_header=True,
            content=dop_buttons_redact,
            expanded=False,
            aspect_ratio=100,
            bgcolor=ft.colors.BLUE_100
        ),
    ]
    panel_list = ft.ExpansionPanelList(
        elevation=10,
        controls=panels
    )

    meters_data = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Дата контрольных показаний: {last_reading_date}"),
                ft.Text(f"Контрольные показания: {last_reading_value}"),

                reading_value,
                remark,

                ft.ElevatedButton("Добавить фотографию"),

                ft.Column(
                    [
                        panel_list
                    ], scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ]
        )
    )

    dlg_modal = ft.AlertDialog(
        modal=True,
        content=meters_data,
        title=title,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_time_task, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    page.controls.clear()
    page.open(dlg_modal)
    page.update()


def user_main(page):
    page.update()
    page.controls.clear()
    screen_width = page.width
    screen_height = page.height
    page.title = "Пользователь"
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.appbar = ft.AppBar(
        title=ft.Text("Задачи"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50
    )
    page.update()

    def update_results():
        results = scr.BD.bd_user.select_tasks_data_new()
        filtered_results = [
            result for result in results
        ]
        column.controls.clear()

        for result in filtered_results:
            id_task, person_name, street, dom, apartment, phone_number, \
                personal_account, date, remark, status, purpose, registered_residing, \
                status_address, standarts, area = result
            if status == 'выполнен':
                color = const.tasks_fulfilled_color
            elif status == 'в_исполнении':
                color = const.tasks_unloaded_color
            else:
                color = const.tasks_pending_color
            result_info = f"Улица: {street} Дом {dom} Квартира {apartment}"
            result_tasks_info = f"Лицевой счет: {personal_account} ФИО: {person_name}"
            row = ft.Column(
                [
                    ft.Text(result_info, size=17, color=const.tasks_text_color),
                    ft.Text(f"Цель задания: {purpose}", size=17, color=const.tasks_text_color),
                ],
            )

            # Используем замыкание для передачи правильного apartment
            def create_on_click(id_task, result_info, result_tasks_info, phone_number, remark, results):
                def on_click(e):
                    show_meters_data(page, id_task, result_info, result_tasks_info, phone_number, remark, results)

                return on_click

            on_click_container = create_on_click(id_task, result_info, result_tasks_info, phone_number, remark, results)

            task_container = ft.Container(
                        content=row,
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

            column.controls.append(task_container)

        page.update()

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def on_click_upload(e):
        scr.BD.bd_server.upload_data_to_server()

    update_results()

    page.add(column)

    page.vertical_alignment = ft.MainAxisAlignment.END
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(text="Отгрузить все данные", on_click=on_click_upload, )
            ], alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.update()
