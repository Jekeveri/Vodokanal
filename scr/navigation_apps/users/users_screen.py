import os
import datetime

import flet as ft

import scr.exit
import scr.BD.bd_user


def update_data(page, id_task):
    def on_click_time_task(e):
        today = datetime.datetime.now().strftime("%H:%M:%S")
        if remark.value != "" and reading_value.value != "":
            scr.BD.bd_user.update_local_tasks(str(today), id_task, reading_value.value, remark.value)

    def on_click_back(e):
        user_main(page)

    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    reading_value = ft.TextField(label="Показания счетчика", width=300)
    remark = ft.TextField(label="Поддробная информация", width=300, )
    photo_picker = ft.ElevatedButton("Добавить фотографию")
    button_save = ft.ElevatedButton("ХУЙ", on_click=on_click_time_task, disabled=False)
    button_back = ft.ElevatedButton("Back", on_click=on_click_back, disabled=False)
    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        reading_value,
                        remark,
                        photo_picker,
                        button_save,
                        button_back
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER

                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


def user_main(page):
    page.clean()
    page.controls.clear()
    page.title = "Пользователь"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def handle_change(e):
        if e.control.selected_index == 1:
            scr.BD.bd_user.delete_data_db()
            page.close(end_drawer)
            scr.exit.exit_account(page)
        else:
            page.add(
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("была нажата кнопка 2")
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            width=400,
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER
                )
            )

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
        results = scr.BD.bd_user.select_task_data()
        filtered_results = [
            result for result in results
        ]
        column.controls.clear()
        for result in filtered_results:
            id_task, street, dom, apartment = result
            result_info = f"Адрес: {street} Дом {dom} Квартира {apartment}"
            # Используем замыкание для передачи правильного apartment
            def create_on_click(id_task):
                def on_click(e):
                    update_data(page, id_task)
                return on_click

            on_click = create_on_click(id_task)

            row = ft.Row(
                [
                    ft.Container(
                        content=ft.Text(result_info),
                        padding=10,
                        margin=5,
                        border_radius=5,
                        width=580,
                        bgcolor=ft.colors.BLUE_400,
                        on_click=on_click
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            column.controls.append(row)
        page.update()

    column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

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
    update_results()
    page.add(column)
    page.update()
