import datetime
import os
import flet as ft
import scr.BD.bd_users.update_bd
import scr.BD.bd_users.insert_bd
import scr.BD.bd_users.select_bd
import scr.BD.bd_server
import scr.exit
import scr.func
import scr.constants as const


def call_show_meters_data(page, id_task):
    show_meters_data(page, id_task)


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
    result_info_person = f"ФИО владельца: {person_name}"
    row_address = ft.Column(
        [
            ft.Text(result_info_address, size=17, color=const.tasks_text_color),
        ],
    )

    def on_click_back(e):
        user_main(page)

    def on_click_save(e):
        scr.BD.bd_users.update_bd.update_dop_data_address(
            remark_textfield.value, registered_residing_textfield.value, standarts_textfield.value,
            area_textfield.value, id_address, id_task)
        call_show_meters_data(page, id_task)
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
            date_next_verification, location, status_filling, meter_remark = result

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


m_value = ""
m_remark = ""
statuses = []
sorting = "Адрес"
search_history_list = []  # длина будет максимум 10


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
            reading_value.error_text = "✱ Введите данные"
            page.update()

    # Обработка нажатия кнопки назад
    def on_click_back(e):
        if reading_value.value != new_reading_value or remark.value != meter_remark:
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
            if new_reading_value is None:
                new_reading_value = ""

    # Поля ввода для показаний и примечаний
    reading_value = ft.TextField(label="Показания счетчика", value=new_reading_value)
    remark = ft.TextField(label="Примечания по счетчику", value=meter_remark, multiline=True, min_lines=1,
                          max_lines=3)

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

    def save_image_to_db(file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)
        scr.BD.bd_users.insert_bd.insert_photo(file_name, file_data, id_task, meter_id)

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                save_image_to_db(file.path)  # Сохраняем изображение в базу данных
                selected_images.append(file.name)
                update_saving_data(meter_id, id_task)
                scr.func.show_snack_bar(page, f"Изображение {file.name} сохранено в базу данных.")
        else:
            scr.func.show_snack_bar(page, "Выбор файла отменен.")

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    selected_images = []
    save_photos = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, )

    def update_saving_data(meter_id, id_task):
        images = scr.BD.bd_users.select_bd.select_photo_data_new(meter_id, id_task)
        if images:
            selected_images.clear()
            for result in images:
                id_photo, value_photo, file_name1, task_id, meter_id = result
                selected_images.append(file_name1)
        save_photos.controls.clear()
        if selected_images:
            for i in selected_images:
                save_photos.controls.append(ft.Text(i))
            page.update()

    update_saving_data(meter_id, id_task)

    def zagr(e):
        pick_files_dialog.pick_files(allow_multiple=True)

    # Основной контент модального окна
    meters_data = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Дата контрольных показаний: {last_reading_date}"),
                ft.Text(f"Контрольные показания: {last_reading_value}"),
                reading_value,
                remark,
                save_photos,
                ft.ElevatedButton("Добавить фотографию", on_click=zagr),
                ft.Column(
                    [
                        panel_list
                    ], scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ], scroll=ft.ScrollMode.AUTO,
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
    global statuses, sorting, search_history_list

    page.appbar = ft.AppBar(
        title=ft.Text("Задачи"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50
    )
    page.update()

    completed_icon = ft.Icon(ft.icons.TASK_ALT, color=ft.colors.WHITE)
    failed_icon = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE)
    pending_icon = ft.Icon(ft.icons.HOURGLASS_EMPTY, color=ft.colors.WHITE)
    unloaded_icon = ft.Icon(ft.icons.BUILD, color=ft.colors.WHITE)

    def filter_completed(e, color):
        global statuses
        if color == ft.colors.WHITE:
            statuses.append('выполнен')
            completed_icon.color = ft.colors.BLACK
            completed_tasks_container.shadow.color = const.tasks_completed_text_color
            update_results(filter_statuses=statuses)
        else:
            statuses.remove('выполнен')
            completed_icon.color = ft.colors.WHITE
            completed_tasks_container.shadow.color = ft.colors.BLACK38
            update_results(filter_statuses=statuses)

    def filter_failed(e, color):
        global statuses
        if color == ft.colors.WHITE:
            statuses.append('просрочен')
            failed_icon.color = ft.colors.BLACK
            failed_tasks_container.shadow.color = const.tasks_failed_text_color
            update_results(filter_statuses=statuses)
        else:
            statuses.remove('просрочен')
            failed_icon.color = ft.colors.WHITE
            failed_tasks_container.shadow.color = ft.colors.BLACK38
            update_results(filter_statuses=statuses)

    def filter_pending(e, color):
        global statuses
        if color == ft.colors.WHITE:
            statuses.append('невыполнен')
            pending_icon.color = ft.colors.BLACK
            pending_tasks_container.shadow.color = ft.colors.BLACK54
            update_results(filter_statuses=statuses)
        else:
            statuses.remove('невыполнен')
            pending_icon.color = ft.colors.WHITE
            pending_tasks_container.shadow.color = ft.colors.BLACK38
            update_results(filter_statuses=statuses)

    def filter_unloaded(e, color):
        global statuses
        if color == ft.colors.WHITE:
            statuses.append('в_исполнении')
            unloaded_icon.color = ft.colors.BLACK
            unloaded_tasks_container.shadow.color = const.tasks_unloaded_text_color
            update_results(filter_statuses=statuses)
        else:
            statuses.remove('в_исполнении')
            unloaded_icon.color = ft.colors.WHITE
            unloaded_tasks_container.shadow.color = ft.colors.BLACK38
            update_results(filter_statuses=statuses)

    completed_tasks_container = ft.Container(
        content=ft.Row([completed_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=20, bottom=20),
        bgcolor=const.tasks_completed_text_color,
        border_radius=ft.border_radius.all(35),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        col=1,
        on_click=lambda e: filter_completed(e, completed_icon.color)
    )
    failed_tasks_container = ft.Container(
        content=ft.Row([failed_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=20, bottom=20),
        bgcolor=const.tasks_failed_text_color,
        border_radius=ft.border_radius.all(35),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        col=1,
        on_click=lambda e: filter_failed(e, failed_icon.color)
    )
    pending_tasks_container = ft.Container(
        content=ft.Row([pending_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=20, bottom=20),
        bgcolor=const.tasks_pending_text_color,
        border_radius=ft.border_radius.all(35),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        col=1,
        on_click=lambda e: filter_pending(e, pending_icon.color)
    )
    unloaded_tasks_container = ft.Container(
        content=ft.Row([unloaded_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=20, bottom=20),
        bgcolor=const.tasks_unloaded_text_color,
        border_radius=ft.border_radius.all(35),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        col=1,
        on_click=lambda e: filter_unloaded(e, unloaded_icon.color)
    )

    def handle_tap(e):
        search_task.open_view()

    def handle_change(e):
        # вывод в консоль при каждом изменении вводимой строки, тут будет обновление заданий и отправка запроса
        # Логика обработки изменения текста (фильтрация, обновление списка и т.д.)
        update_search_results(e.control.value)

    def handle_submit(e):
        # выбор при enter, тут то же будет запрос, но уже с готовым заданием, может быть даже сразу будет открывать
        # плашку
        query = e.control.value.strip()
        if query and query not in search_history_list:
            if len(search_history_list) >= 10:
                del search_history_list[9]
            search_history_list.insert(0, query)
            update_search_history()  # Обновляем историю запросов
        update_search_results("")
        page.update()
        search_task.close_view()

    def close_anchor(e):
        # Логика обработки выбора элемента из истории
        search_task.value = e.control.data
        update_search_results("")
        page.update()
        search_task.close_view()

    def create_search_list():
        return [
            ft.ListTile(
                title=ft.Text(query),
                on_click=close_anchor,
                data=query
            )
            for query in search_history_list
        ]

    def update_search_history():
        # Обновляем элементы управления в SearchBar с новой историей запросов
        search_task.controls = create_search_list()
        page.update()

    def update_search_results(query):
        # Логика обновления отображения в зависимости от запроса
        pass

    search_task = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Поиск задания...",
        view_hint_text="Последние результаты...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=create_search_list(),  # Изначально отображаем пустой список или последние результаты
        col=3
    )

    def update_results(filter_statuses=None):
        results = scr.BD.bd_users.select_bd.select_tasks_data_new(sorting)
        if filter_statuses:
            filtered_results = [result for result in results if result[9] in filter_statuses]
        else:
            filtered_results = [
                result for result in results
            ]

        column.controls.clear()

        for result in filtered_results:
            id_task, person_name, street, dom, apartment, phone_number, \
                personal_account, date, remark, status, purpose, registered_residing, \
                status_address, standarts, area, saldo = result
            if status == 'выполнен':
                color = const.tasks_completed_color
            elif status == 'в_исполнении':
                color = const.tasks_unloaded_color
            else:
                color = const.tasks_pending_color
            result_info = f"Улица: {street} Дом {dom} Квартира {apartment}"
            row = ft.Column(
                [
                    ft.Text(result_info, size=17, color=const.tasks_text_color),
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

    def on_click_update(e):
        statuses.clear()
        unloaded_icon.color = ft.colors.WHITE
        unloaded_tasks_container.shadow.color = ft.colors.BLACK38
        pending_icon.color = ft.colors.WHITE
        pending_tasks_container.shadow.color = ft.colors.BLACK38
        failed_icon.color = ft.colors.WHITE
        failed_tasks_container.shadow.color = ft.colors.BLACK38
        completed_icon.color = ft.colors.WHITE
        completed_tasks_container.shadow.color = ft.colors.BLACK38

        result = scr.BD.bd_users.select_bd.select_user_data()
        if result:
            for record in result:
                user_id, login_user, password_user, privileges, first_name, last_name = record
                scr.BD.bd_server.select_task_data_for_update(user_id)
        update_results()
        page.update()

    update_results()

    def sorting_change(e):
        global sorting
        sorting = e.control.value
        update_results(statuses)

    page.add(
        ft.ResponsiveRow(
            [
                ft.ResponsiveRow(
                    [
                        search_task,
                        ft.Dropdown(
                            on_change=sorting_change,
                            value=sorting,
                            width=100,
                            label="Сортировка",
                            options=[
                                ft.dropdown.Option("Адрес"),
                                ft.dropdown.Option("Статус"),
                            ],
                            col=1
                        )
                    ], columns=4
                ),
                unloaded_tasks_container,
                pending_tasks_container,
                completed_tasks_container,
                failed_tasks_container
            ],
            columns=4,
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(thickness=2, color=ft.colors.BLACK45)
    )

    page.add(column)

    page.vertical_alignment = ft.MainAxisAlignment.END
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(text="Отгрузить все данные", on_click=on_click_upload, ),
                ft.ElevatedButton(text="Обновить", on_click=on_click_update, )
            ], alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.update()
