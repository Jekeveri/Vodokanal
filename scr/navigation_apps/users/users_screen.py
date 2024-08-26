import datetime

import flet as ft

import scr.BD.bd_users.update_bd
import scr.BD.bd_users.insert_bd
import scr.BD.bd_users.select_bd
import scr.BD.bd_server
import scr.exit
import scr.func
import scr.constants as const


def show_meters_data(page, id_task):
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
            status_address, standarts, area, saldo = result
    result_info_address = f"Улица: {street} Дом {dom} Квартира {apartment}"
    row_address = ft.Column(
        [
            ft.Text(result_info_address, size=17, color=const.tasks_text_color),
            ft.Text(f"Цель задания: {purpose}", size=17, color=const.tasks_text_color),
        ],
    )

    def on_click_back(e):
        user_main(page)

    def on_click_save(e):
        scr.BD.bd_users.update_bd.update_dop_data_address(
            remark_textfield.value, registered_residing_textfield.value, standarts_textfield.value,
            area_textfield.value, id_address, id_task)
        user_main(page)
        page.update()

    button_back = ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
    button_save = ft.ElevatedButton("Сохранить", on_click=on_click_save, bgcolor=ft.colors.RED_200, visible=False)
    filtered_results_meters = [result for result in results_meters_data]
    column = ft.Column(scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    color = ft.colors.GREY
    column.controls.clear()

    def on_change_dop_data(e):
        button_save.visible = True
        page.update()

    def on_click_add(e):
        scr.func.show_alert_yn(page, "Заполните новый счетчик", id_task)
        page.update()

    button_add = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=on_click_add,
                                         bgcolor=ft.colors.LIME_300)
    for result in filtered_results_meters:
        id_meters, meter_number, instalation_day, meter_type, id_address, marka, seal_number, \
            date_next_verification, location, status_filling, meter_remark = result

        if status_filling == 'выполнен':
            color = const.tasks_fulfilled_color
        elif status_filling == 'в_исполнении':
            color = const.tasks_unloaded_color
        else:
            color = const.tasks_pending_color

        result_info_meters = f"Счетчик: {marka} Дата установки: {instalation_day} Тип: {meter_type}"

        row_to_container = ft.Column(
            [
                ft.Text(f"Номер: {id_meters}", size=17, ),
                ft.Text(result_info_meters, size=17, ),
            ],
        )

        # Используем замыкание для передачи правильного apartment
        def create_on_click(id_task, id_meters):
            def on_click(e):
                update_data(page, id_meters, id_task)

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
    saldo_text = ft.Text(f"Сальдо: {saldo}", size=17)
    registered_residing_textfield = ft.TextField(label="Прописанно", value=registered_residing,
                                                 on_change=on_change_dop_data)
    standarts_textfield = ft.TextField(label="Нормативы", value=standarts, on_change=on_change_dop_data)
    area_textfield = ft.TextField(label="Площадь", value=area, on_change=on_change_dop_data)
    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    remark_textfield,
                    saldo_text,
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
    column.controls.append(button_add)
    column.controls.append(container)
    content_dialog = column
    title = ft.Column(
        [
            row_address,
            ft.Text(result_info_address, size=17, ),
            ft.Text(f"{phone_number}", size=17, ),
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


m_value = ""
m_remark = ""


def update_data(page, meter_id, id_task):
    screen_width = page.width
    screen_height = page.height

    # Функции для работы с BottomSheet
    def bottom_sheet_yes(e):
        page.close(bottom_sheet)
        page.close(dlg_modal)
        show_meters_data(page, id_task)

    def bottom_sheet_no(e):
        page.close(bottom_sheet)

    # BottomSheet для подтверждения выхода
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

    # Обработка нажатия кнопки сохранения
    def on_click_time_task(e):
        today = datetime.datetime.now().strftime("%H:%M:%S")
        if remark.value and reading_value.value:  # Упростил проверку на пустоту
            global m_remark, m_value
            m_value = reading_value.value
            m_remark = remark.value
            scr.BD.bd_users.update_bd.update_local_tasks(
                str(today), id_task, m_value, m_remark, meter_id)
            show_meters_data(page, id_task)
            page.close(dlg_modal)
            page.update()
        else:
            reading_value.error_text = "Введите данные"
            page.update()

    # Обработка нажатия кнопки назад
    def on_click_back(e):
        if reading_value.value != m_value or remark.value != m_remark:
            page.open(bottom_sheet)
        else:
            page.close(dlg_modal)
            show_meters_data(page, id_task)

    # Инициализация переменных на случай, если данные не будут получены
    marka = "Неизвестно"
    meter_number = "Неизвестно"
    instalation_day = "Неизвестно"
    meter_type = "Неизвестно"
    seal_number = "Неизвестно"
    location = "Неизвестно"
    meter_remark = "Неизвестно"

    # Получение данных счетчика
    results_meters_data = scr.BD.bd_users.select_bd.select_meters_data_new_for_one(id_task, meter_id)
    if results_meters_data:
        for result in results_meters_data:
            id_meters, meter_number, instalation_day, meter_type, id_address, marka, seal_number, \
                date_next_verification, location, status_filling, meter_remark = result

    # Формирование текста с информацией о счетчике
    result_info_meters = f"Счетчик: {marka} Дата установки: {instalation_day} Тип: {meter_type}"

    # Инициализация переменных для показаний
    last_reading_date = "Неизвестно"
    last_reading_value = "Неизвестно"
    new_reading_value = ""

    # Получение данных показаний счетчика
    results = scr.BD.bd_users.select_bd.select_meter_reading_new(meter_id)
    if results:
        for result in results:
            id_meters, last_reading_date, last_reading_value, new_reading_date, new_reading_value = result

    # Поля ввода для показаний и примечаний
    reading_value = ft.TextField(label="Показания счетчика", value=new_reading_value)
    remark = ft.TextField(label="Примечания по счетчику", value=meter_remark, multiline=True, min_lines=1,
                          max_lines=3, )

    # Заголовок
    title = ft.Column(
        [
            ft.Text(f"Номер: {meter_id}", size=17),
            ft.Text(result_info_meters, size=17),
        ]
    )

    # Поля ввода для редактирования данных счетчика
    marka_textfield = ft.TextField(label="Марка", value=marka)
    meter_number_textfield = ft.TextField(label="Заводской номер", value=meter_number)
    seal_number_textfield = ft.TextField(label="Номер пломбы", value=seal_number)
    location_textfield = ft.TextField(label="Место расположения", value=location)
    meter_type_textfield = ft.TextField(label="Тип услуги", value=meter_type)

    # Расширяемый список для редактирования данных счетчика
    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    marka_textfield,
                    meter_number_textfield,
                    seal_number_textfield,
                    location_textfield,
                    meter_type_textfield,
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

    # Основной контент модального окна
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

    # Модальное окно с данными счетчика
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

    # Очищаем и обновляем контент страницы
    page.controls.clear()
    page.open(dlg_modal)
    page.update()


def user_main(page):
    page.update()
    page.controls.clear()
    screen_width = page.width
    screen_height = page.height
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.appbar = ft.AppBar(
        title=ft.Text("Задачи"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50
    )
    page.update()

    def update_results():
        results = scr.BD.bd_users.select_bd.select_tasks_data_new()
        filtered_results = [
            result for result in results
        ]
        column.controls.clear()

        for result in filtered_results:
            id_task, person_name, street, dom, apartment, phone_number, \
                personal_account, date, remark, status, purpose, registered_residing, \
                status_address, standarts, area, saldo = result
            if status == 'выполнен':
                color = const.tasks_fulfilled_color
            elif status == 'в_исполнении':
                color = const.tasks_unloaded_color
            else:
                color = const.tasks_pending_color
            result_info = f"Улица: {street} Дом {dom} Квартира {apartment}"
            row = ft.Column(
                [
                    ft.Text(result_info, size=17, color=const.tasks_text_color),
                    ft.Text(f"Цель задания: {purpose}", size=17, color=const.tasks_text_color),
                ],
            )

            # Используем замыкание для передачи правильного apartment
            def create_on_click(id_task):
                def on_click(e):
                    show_meters_data(page, id_task)

                return on_click

            on_click_container = create_on_click(id_task)

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
