import datetime

import flet as ft

import scr.BD.bd_user
import scr.BD.bd_server
import scr.exit
import scr.func


def show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number, remark):
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
        id_meters, meter_number, instalation_day, meter_type, status, status_filling, meter_remark = result

        if status_filling == 'выполнен':
            color = ft.colors.GREEN
        elif status_filling == 'в_исполнении':
            color = ft.colors.YELLOW
        else:
            color = ft.colors.GREY

        result_info_meters = f"Счетчик: {meter_number} Дата установки: {instalation_day} Тип: {meter_type}"

        row_to_container = ft.Column(
            [
                ft.Text(f"Номер: {id_meters}", size=17, ),
                ft.Text(result_info_meters, size=17, ),
            ],
        )

        # Используем замыкание для передачи правильного apartment
        def create_on_click(id_task, id_meters, result_info_meters, result_tasks_info, phone_number, meter_remark,
                            remark):
            def on_click(e):
                update_data(page, id_meters, result_info_meters, id_task, result_info_address, result_tasks_info,
                            phone_number, meter_remark, remark)

            return on_click

        on_click_container = create_on_click(id_task, id_meters, result_info_meters, result_tasks_info, phone_number,
                                             meter_remark, remark)

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
    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    ft.ElevatedButton("Сальдо"),
                    ft.ElevatedButton("Прописанно"),
                    ft.ElevatedButton("Нормативы"),
                    ft.ElevatedButton("Площадь"),
                ]
            )
        ]
    )
    panels = [
        ft.ExpansionPanel(
            header=ft.Text("Редактирование данных адреса"),
            can_tap_header=True,
            content=dop_buttons_redact,
            expanded=False,
            aspect_ratio=100,
            bgcolor=ft.colors.BLUE_100,
        ),
    ]
    panel_list = ft.ExpansionPanelList(
        elevation=10,
        controls=panels,
    )
    container = ft.Container(
        content=panel_list,
        width=screen_width * 0.2,  # Задаем ширину контейнера
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
    # page.open(dlg_modal)
    page.update()


def update_data(page, meter_id, result_info_meters, id_task, result_info_address, result_tasks_info,
                phone_number, meter_remark, task_remark):
    today = datetime.datetime.now().strftime("%H:%M:%S")
    screen_width = page.width
    screen_height = page.height

    def on_click_time_task(e):
        today = datetime.datetime.now().strftime("%H:%M:%S")
        if remark.value != "" and reading_value.value != "":
            scr.BD.bd_user.update_local_tasks(str(today), id_task, reading_value.value, remark.value, meter_id)
            show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number, task_remark)
            page.close(dlg_modal)
            page.update()

    def on_click_back(e):
        page.close(dlg_modal)
        show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number, task_remark)

    results = scr.BD.bd_user.select_meter_reading_new(meter_id)
    filtered_results = [result for result in results]
    for result in filtered_results:
        id_meters, last_reading_date, last_reading_value = result

    reading_value = ft.TextField(label="Показания счетчика", )
    remark = ft.TextField(label="Примечания по счетчику", )

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
        bgcolor=ft.colors.BLUE_GREY_50
    )

    def handle_change(e):
        if e.control.selected_index == 1:
            scr.BD.bd_user.delete_data_db()
            page.close(end_drawer)
            scr.exit.exit_account(page)
        else:
            pass

    end_drawer = ft.NavigationDrawer(
        on_change=handle_change,
        controls=[
            ft.IconButton(icon=ft.icons.ARROW_LEFT, on_click=lambda e: page.close(end_drawer)),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(icon=ft.icons.ADD_TO_HOME_SCREEN_SHARP, label="Главная"),
            ft.NavigationDrawerDestination(icon=ft.icons.EXIT_TO_APP, label="Выход"),
        ],
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
                personal_account, date, remark, status, purpose = result

            if status == 'выполнен':
                color = ft.colors.GREEN
            elif status == 'в_исполнении':
                color = ft.colors.YELLOW
            else:
                color = ft.colors.GREY
            result_info = f"Улица: {street} Дом {dom} Квартира {apartment}"
            result_tasks_info = f"Лицевой счет: {personal_account} ФИО: {person_name}"
            row = ft.Column(
                [
                    ft.Text(result_info, size=17, ),
                    ft.Text(f"Цель задания: {purpose}", size=17, ),
                ],
            )

            # Используем замыкание для передачи правильного apartment
            def create_on_click(id_task, result_info, result_tasks_info, phone_number, remark):
                def on_click(e):
                    show_meters_data(page, id_task, result_info, result_tasks_info, phone_number, remark)

                return on_click

            on_click_container = create_on_click(id_task, result_info, result_tasks_info, phone_number, remark)

            row = ft.Row(
                [
                    ft.Container(
                        content=row,
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
        page.update()

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    icons = ft.Icon(
        name=ft.icons.MENU,
        color=ft.colors.LIME_50
    )

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
