import datetime
import flet as ft
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.local.delete_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.bd_server_user
import scr.toggle_user_sessions
import scr.func
import scr.constants as const
import scr.navigation_apps.users.doing_work.chose_meters

statuses = []
sorting = "Дата"
search_history_list = []  # длина будет--------------------------максимум 10


def recall_main(page):
    main(page)


def main(page):
    page.update()
    page.controls.clear()
    screen_width = page.width
    screen_height = page.height
    page.vertical_alignment = ft.MainAxisAlignment.START
    global statuses, sorting, search_history_list

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

        result = scr.BD.bd_users.local.select_bd.select_user_data()
        if result:
            for record in result:
                user_id, login_user, password_user, privileges, first_name, last_name = record
                scr.BD.bd_users.bd_server_user.select_task_data_for_update(user_id)
        update_results()
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Будущие задачи"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50,
        actions=[
            ft.IconButton(icon=ft.icons.AUTORENEW, on_click=on_click_update)
        ]
    )
    page.update()

    completed_icon = ft.Icon(ft.icons.TASK_ALT, color=ft.colors.WHITE)
    failed_icon = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE)
    pending_icon = ft.Icon(ft.icons.HOURGLASS_EMPTY, color=ft.colors.WHITE)
    unloaded_icon = ft.Icon(ft.icons.BUILD, color=ft.colors.WHITE)

    def filtration(e, color, text):
        global statuses
        if text not in statuses:
            if color == ft.colors.WHITE:
                statuses.append(text)
                if text == 'выполнен':
                    completed_icon.color = ft.colors.BLACK
                    completed_tasks_container.shadow.color = const.tasks_completed_text_color
                    update_results(filter_statuses=statuses)
                elif text == 'просрочен':
                    failed_icon.color = ft.colors.BLACK
                    failed_tasks_container.shadow.color = const.tasks_failed_text_color
                    update_results(filter_statuses=statuses)
                elif text == 'невыполнен':
                    pending_icon.color = ft.colors.BLACK
                    pending_tasks_container.shadow.color = ft.colors.BLACK54
                    update_results(filter_statuses=statuses)
                elif text == 'в_исполнении':
                    unloaded_icon.color = ft.colors.BLACK
                    unloaded_tasks_container.shadow.color = const.tasks_unloaded_text_color
                    update_results(filter_statuses=statuses)
        else:
            if color != ft.colors.WHITE:
                statuses.remove(text)
                if text == 'выполнен':
                    completed_icon.color = ft.colors.WHITE
                    completed_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)
                elif text == 'просрочен':
                    failed_icon.color = ft.colors.WHITE
                    failed_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)
                elif text == 'невыполнен':
                    pending_icon.color = ft.colors.WHITE
                    pending_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)
                elif text == 'в_исполнении':
                    unloaded_icon.color = ft.colors.WHITE
                    unloaded_tasks_container.shadow.color = ft.colors.BLACK38
                    update_results(filter_statuses=statuses)

    completed_tasks_container = ft.Container(
        content=ft.Row([completed_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=5, bottom=5),
        margin=ft.margin.only(left=5, right=5),
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
        on_click=lambda e: filtration(e, completed_icon.color, 'выполнен')
    )
    failed_tasks_container = ft.Container(
        content=ft.Row([failed_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=5, bottom=5),
        margin=ft.margin.only(left=5, right=5),
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
        on_click=lambda e: filtration(e, failed_icon.color, 'просрочен')
    )
    pending_tasks_container = ft.Container(
        content=ft.Row([pending_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=5, bottom=5),
        margin=ft.margin.only(left=5, right=5),
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
        on_click=lambda e: filtration(e, pending_icon.color, 'невыполнен')
    )
    unloaded_tasks_container = ft.Container(
        content=ft.Row([unloaded_icon], alignment=ft.MainAxisAlignment.CENTER, ),
        padding=ft.padding.only(top=5, bottom=5),
        margin=ft.margin.only(left=5, right=5),
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
        on_click=lambda e: filtration(e, unloaded_icon.color, 'в_исполнении')
    )

    def handle_tap(e):
        search_task.open_view()

    def handle_change(e):
        # вывод в консоль при каждом изменении вводимой строки, тут будет обновление заданий и отправка запроса
        # Логика обработки изменения текста (фильтрация, обновление списка и т.д.)
        if search_task.value != '':
            search_task.close_view(e.control.value)
        update_search_results(e.control.value)
        update_results(statuses)

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
        search_task.close_view(query)
        update_results(statuses)

    def close_anchor(e):
        # Логика обработки выбора элемента из истории
        search_task.value = e.control.data
        update_search_results("")
        update_results(statuses)
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
        value="",
        controls=create_search_list(),  # Изначально отображаем пустой список или последние результаты
        col=3,
    )

    def update_results(filter_statuses=None):
        search_value = search_task.value
        results = scr.BD.bd_users.local.select_bd.select_future_tasks_data_new(sorting, search_value)

        if filter_statuses:
            filtered_results = [result for result in results if result[10] in filter_statuses]
        else:
            filtered_results = [result for result in results]

        column.controls.clear()

        # Словарь для хранения задач по датам и улицам
        tasks_by_date = {}

        panel_list = ft.ExpansionPanelList(
            elevation=25,
            expanded_header_padding=3
        )

        for result in filtered_results:
            id_task, person_name, district, street, dom, apartment, phone_number, \
                personal_account, date, remark, status, purpose, registered_residing, \
                status_address, standarts, area, saldo = result

            # Проверяем, существует ли уже ключ для этой даты, если нет - создаем
            if date not in tasks_by_date:
                tasks_by_date[date] = {}

            # Проверяем, существует ли уже ключ для этой улицы внутри даты, если нет - создаем
            if street not in tasks_by_date[date]:
                tasks_by_date[date][street] = []

            if status == 'выполнен':
                color = const.tasks_completed_color
            elif status == 'в_исполнении':
                color = const.tasks_unloaded_color
            else:
                color = const.tasks_pending_color

            result_info = f"ул.{street} д.{dom} кв.{apartment}"
            row = ft.Column(
                [
                    ft.Text(result_info, size=17, color=const.tasks_text_color),
                    ft.Text(f"{phone_number}")
                ]
            )

            def viewing(e, id_task):
                def on_click(e):
                    page.close(view)

                results_address_data = scr.BD.bd_users.local.select_bd.select_tasks_data_for_one(id_task)
                filtered_results = [
                    result_address_data for result_address_data in results_address_data
                ]

                for result in filtered_results:
                    id_task, person_name, street, dom, apartment, phone_number, \
                        personal_account, date, remark, status, purpose, registered_residing, \
                        status_address, standarts, area, saldo, type_address = result
                result_info_address = f"Адрес: ул.{street} д.{dom} кв.{apartment}"
                result_info_person = f"ФИО владельца: {person_name}"
                view = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(result_info_address),
                    content=ft.Column(
                        [
                            ft.Text(f"Лицевой счет: {personal_account}"),
                            ft.Text(f"{result_info_person}"),
                            ft.Text(f"Номер телефона: {phone_number}"),
                            ft.Text(f"Тип адресса: {type_address}"),
                            ft.Text(f"Дата выполнения: {date}"),
                            ft.Text(f"Тип задания: {purpose}"),
                            ft.Text(f"Количество прописанных: {registered_residing}"),
                            ft.Text(f"Нормативы: {standarts}"),
                            ft.Text(f"Площадь: {area}"),
                        ]
                    ),
                    actions=[
                        ft.Row(
                            [
                                ft.ElevatedButton("Назад", on_click=on_click, bgcolor=ft.colors.RED_200)
                            ], alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                )
                page.open(view)

            def reschedule_to_another_date(e, task_id, date):

                def check():
                    try:
                        # Попробуем преобразовать введенный текст в дату
                        datetime.datetime.strptime(new_date.value, '%Y-%m-%d')  # Формат даты: ГГГГ-ММ-ДД
                        result_text = True
                    except ValueError:
                        result_text = False
                    return result_text

                def on_click(e):
                    if check():
                        scr.BD.bd_users.local.update_bd.update_date(task_id, new_date.value)
                        recall_main(page)
                        page.close(change_date)
                    else:
                        new_date.error_text = "Введите правильный формат даты \nГГГГ-ММ-ДД"
                    page.update()

                def close(e):
                    page.close(change_date)

                new_date = ft.TextField(label="Новая дата", value=date)
                change_date = ft.AlertDialog(
                    title=ft.Text("Перенести задание на другой день"),
                    content=ft.Column(
                        [
                            ft.Text(f"Старая дата: {date}"),
                            new_date
                        ]
                    ),
                    actions=[
                        ft.Row(
                            [
                                ft.ElevatedButton("Подтвердить",
                                                  on_click=on_click,
                                                  bgcolor=ft.colors.BLUE_200,
                                                  width=screen_width * 0.30),
                                ft.ElevatedButton("Назад",
                                                  on_click=close,
                                                  bgcolor=ft.colors.BLUE_200,
                                                  width=screen_width * 0.30)
                            ], alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )

                page.open(change_date)
                page.update()

            # Используем замыкание для передачи правильного id_task + выбор действия
            def create_on_click(id_task, date):
                def show(e):
                    page.open(
                        ft.AlertDialog(
                            title=ft.Text("Вы хотите просмотреть данные или выполнить задание?"),
                            actions=[
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Просмотреть",
                                                          on_click=lambda e: viewing(e, id_task),
                                                          bgcolor=ft.colors.BLUE_200,
                                                          width=screen_width * 0.30),
                                        ft.ElevatedButton("Выполнить",
                                                          on_click=on_click,
                                                          bgcolor=ft.colors.BLUE_200,
                                                          width=screen_width * 0.30)
                                    ], alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Row(),
                                ft.Row(
                                    [
                                        ft.ElevatedButton("Перенос задания",
                                                          on_click=lambda e: reschedule_to_another_date(e, id_task,
                                                                                                        date),
                                                          bgcolor=ft.colors.BLUE_200),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ]
                        )
                    )

                def on_click(e):
                    scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where="fff")

                return show

            on_click_container = create_on_click(id_task, date)

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
                alignment=ft.alignment.bottom_left,
                on_click=on_click_container
            )

            # Добавляем контейнер с задачей в соответствующий список по улице
            tasks_by_date[date][street].append(task_container)

        # Создаем раскрывающиеся панели по датам
        for date, streets in tasks_by_date.items():
            street_panel_list = ft.ExpansionPanelList(
                elevation=10,
                expanded_header_padding=3
            )

            # Создаем раскрывающиеся панели по улицам для каждой даты
            for street, tasks in streets.items():
                street_panel = ft.ExpansionPanel(
                    header=ft.Text(f"{street}"),
                    content=ft.Column(tasks, scroll=ft.ScrollMode.AUTO),  # Добавляем список задач в панель
                    expanded=True,
                    can_tap_header=True
                )
                street_panel_list.controls.append(street_panel)

            # Добавляем панель с улицами в панель по дате
            date_panel = ft.ExpansionPanel(
                header=ft.Text(f"{date}"),
                content=street_panel_list,  # Добавляем список улиц в панель по дате
                expanded=True,
                can_tap_header=True
            )
            panel_list.controls.append(date_panel)

        column.controls.append(panel_list)

        page.update()

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def on_click_upload(e):
        scr.BD.bd_users.bd_server_user.upload_data_to_server(page)

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
                                ft.dropdown.Option("Дата"),
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
        ft.Container(
            content=ft.Column([ft.Divider(thickness=4, color=ft.colors.WHITE)]),

        )
    )

    page.add(column)

    page.vertical_alignment = ft.MainAxisAlignment.END
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(text="Отгрузить все данные", on_click=on_click_upload, icon="BACKUP_ROUNDED", ),
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()
