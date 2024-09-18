import flet as ft

import scr.BD.bd_admin.select_server
import scr.BD.bd_admin.update_server
import scr.exit
import scr.func
import scr.constants as const


def admin_main(page):
    page.clean()
    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.START
    screen_width = page.window_width
    screen_height = page.window_height
    # Словарь для хранения состояний чекбоксов
    task_status = {}

    def create_on_click(selected_task, employer_id):

        def on_click(e):
            scr.BD.bd_admin.update_server.set_employer_to_task(selected_task, employer_id)
            page.close(choice_employer_list)
            scr.func.show_snack_bar(page, "Задание назначенно")
            show_results()

        return on_click

    list_employer = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, )
    choice_employer_list = ft.AlertDialog(
        modal=True,
        title=ft.Text("Выбор сотрудника"),
        content=list_employer,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Назад", on_click=lambda e: page.close(choice_employer_list),
                                      bgcolor=ft.colors.RED_200)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    def choice_employer(selected_task):
        list_employer.controls.clear()
        results = scr.BD.bd_admin.select_server.select_employer_to_choice()
        filtered_results = [
            result for result in results
        ]
        if results:
            for record in filtered_results:
                employer_id, name = record
                list_employer.controls.append(ft.Container(content=ft.Text(f"{name}"),
                                                           on_click=create_on_click(selected_task, employer_id)))

        page.open(choice_employer_list)
        page.update()

    # Функция обновления состояния чекбоксов
    def on_checkbox_change(e, task_id):
        task_status[task_id] = e.control.value

    # Функция для обработки назначения заданий
    def assign_tasks(e):
        selected_tasks = [task_id for task_id, is_checked in task_status.items() if is_checked]
        if selected_tasks:
            # Здесь выполняется логика назначения выбранных заданий
            choice_employer(selected_tasks)
            task_status.clear()
        else:
            scr.func.show_snack_bar(page, "Выберите задания")

    home_tabs = ft.Container(
        content=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
                ft.DataColumn(ft.Text("Age"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("54"), on_double_tap=True),
                        ft.DataCell(ft.Text("54")),
                        ft.DataCell(ft.Text("54")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack"), on_double_tap=True),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        ),
    )

    def show_results():
        res = scr.BD.bd_admin.select_server.select_address_to_choice()
        filtered_results = [
            result for result in res
        ]
        column_content.controls.clear()
        if res:
            for record in filtered_results:
                task_id, address_id, city, district, street, dom, apartment, entrance = record
                # Изначально все чекбоксы отключены (False)
                task_status[task_id] = False

                row = ft.Container(
                    content=ft.Row(
                        [
                            ft.Checkbox(value=False,
                                        on_change=lambda e, task_id=task_id: on_checkbox_change(e, task_id),
                                        label=f"р.{district} ул.{street} д.{dom} кв.{apartment}",
                                        label_style=ft.TextStyle(size=17)),
                        ]
                    ),
                )
                column_content.controls.append(row)
            column_content.controls.append(
                ft.Container(
                    content=ft.Text("Назначить"),
                    padding=ft.padding.only(top=20, bottom=20),
                    margin=5,
                    border_radius=15,
                    bgcolor=ft.colors.BLUE,
                    ink=True,
                    shadow=ft.BoxShadow(
                        offset=ft.Offset(0, 7),
                        blur_radius=10,
                        color=ft.colors.BLACK38
                    ),
                    alignment=ft.alignment.center,
                    on_click=assign_tasks  # Обработка назначения
                )
            )
            page.update()
        else:
            column_content.controls.append(ft.Text("Нет свободных заданий", size=26))
            page.update()

    column_content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, )
    show_results()
    tabs_content_2 = ft.Container(
        content=ft.Container(
            content=column_content
        )
    )

    def on_click_exit(e):
        scr.exit.exit_account(page)

    setting_tabs = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.TIME_TO_LEAVE, color=ft.colors.WHITE),
            ft.Text("Выход", style=ft.TextStyle(color=ft.colors.WHITE))
        ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(top=20, left=50, right=50, bottom=20),
        bgcolor=const.tasks_completed_text_color,
        border_radius=ft.border_radius.all(25),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        on_click=on_click_exit,
    )

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        scrollable=True,
        tabs=[
            ft.Tab(
                text="Главная",
                content=home_tabs,
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
                content=tabs_content_2,
            ),
            ft.Tab(
                text="Настройки",
                icon=ft.icons.SETTINGS,
                content=setting_tabs,
            ),
        ],
        expand=1,
    )

    page.add(t)
    page.update()
