import datetime

import flet as ft

import scr.BD.bd_user
import scr.BD.bd_server
import scr.exit


def show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number):
    screen_width = page.window.width
    screen_height = page.window.height
    results = scr.BD.bd_user.select_meters_data_new(id_task)

    def on_click_back(e):
        page.close(dlg_modal)
        user_main(page)
    button_back = ft.ElevatedButton("Back", on_click=on_click_back, width=screen_width * 0.2)
    filtered_results = [
        result for result in results
    ]
    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    color = ft.colors.GREY
    column.controls.clear()
    for result in filtered_results:
        id_meters, meter_number, instalation_day, meter_type, status, status_filling = result

        if status_filling == 'выполнен':
            color = ft.colors.GREEN
        elif status_filling == 'в_исполнении':
            color = ft.colors.YELLOW
        else:
            color = ft.colors.GREY
        result_info_meters = f"Счетчик: {meter_number} Дата установки: {instalation_day} Тип: {meter_type}"
        row_to_container = ft.Column(
            [
                ft.Text(f"Номер: {id_meters}", size=17, width=screen_width * 0.2),
                ft.Text(result_info_meters, size=17, width=screen_width * 0.2),
            ],
        )

        # Используем замыкание для передачи правильного apartment
        def create_on_click(id_task, id_meters, result_info_meters, result_tasks_info, phone_number):
            def on_click(e):
                update_data(page, id_meters, result_info_meters, id_task, result_info_address, result_tasks_info, phone_number)

            return on_click

        on_click_container = create_on_click(id_task, id_meters, result_info_meters, result_tasks_info, phone_number)

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
    content_dialog = column
    title = ft.Column(
        [
            ft.Text(result_tasks_info, size=17, width=screen_width * 0.2),
            ft.Text(result_info_address, size=17, width=screen_width * 0.2),
            ft.Text(f"{phone_number}", size=17,)
        ]
    )
    row_button = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    row_button.controls.append(button_back)

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=title,
        content=content_dialog,
        content_padding=20,
        actions=[
            row_button
        ],
        actions_alignment=ft.MainAxisAlignment.END,

    )
    page.open(dlg_modal)
    page.update()


def update_data(page, meter_id, result_info_meters, id_task, result_info_address, result_tasks_info, phone_number):
    screen_width = page.window.width
    screen_height = page.window_height

    def on_click_upload(e):
        pass

    def on_click_time_task(e):
        today = datetime.datetime.now().strftime("%H:%M:%S")
        if remark.value != "" and reading_value.value != "":
            scr.BD.bd_user.update_local_tasks(str(today), id_task, reading_value.value, remark.value, meter_id)

    def on_click_back(e):
        show_meters_data(page, id_task, result_info_address, result_tasks_info, phone_number)

    reading_value = ft.TextField(label="Показания счетчика", width=screen_width * 0.2)
    remark = ft.TextField(label="Поддробная информация", width=screen_width * 0.2)
    photo_picker = ft.ElevatedButton("Добавить фотографию", width=screen_width * 0.2)
    button_save = ft.ElevatedButton("Сохранить", on_click=on_click_time_task)
    button_save_upload = ft.ElevatedButton("Сохранить и отправить", on_click=on_click_upload, width=screen_width * 0.11)
    button_back = ft.ElevatedButton("Back", on_click=on_click_back)

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    column.controls.clear()
    column.controls.append(reading_value)
    column.controls.append(remark)
    column.controls.append(photo_picker)

    title = ft.Column(
        [
            ft.Text(f"Номер: {meter_id}", size=17, width=screen_width * 0.2),
            ft.Text(result_info_meters, size=17, width=screen_width * 0.2),
        ]
    )
    row_button = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    row_button.controls.append(button_save)
    row_button.controls.append(button_back)
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=title,
        content=column,
        actions=[
            row_button
        ],
    )
    page.open(dlg_modal)
    page.update()


def user_main(page):
    page.update()
    page.controls.clear()
    screen_width = page.window_width
    screen_height = page.window_height
    page.title = "Пользователь"
    page.vertical_alignment = ft.MainAxisAlignment.START

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
        color = ft.colors.GREY
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
                    ft.Text(result_info, size=17, width=screen_width * 0.2),
                    ft.Text(f"Цель задания: {purpose}", size=17, width=screen_width * 0.2),
                ],
            )

            # Используем замыкание для передачи правильного apartment
            def create_on_click(id_task, result_info, result_tasks_info, phone_number):
                def on_click(e):
                    show_meters_data(page, id_task, result_info, result_tasks_info, phone_number)

                return on_click

            on_click_container = create_on_click(id_task,result_info, result_tasks_info, phone_number)

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
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.FloatingActionButton(icon=ft.icons.MENU, bgcolor=ft.colors.GREY_50, scale=0.6,
                                                        on_click=lambda e: page.open(end_drawer))
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            width=400,
                        )
                    ], alignment=ft.MainAxisAlignment.START,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
    )

    def on_click_upload(e):
        scr.BD.bd_server.upload_data_to_server()

    update_results()
    page.add(column)
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(text="Отгрузить все данные", on_click=on_click_upload, width=screen_width * 0.2)
            ], alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.update()
