import flet as ft

import scr.BD.bd_admin.select_server
import scr.exit
import scr.func
import scr.constants as const


def admin_main(page):
    page.clean()
    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.START
    screen_width = page.window_width
    screen_height = page.window_height

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
    column_content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True,)
    res = scr.BD.bd_admin.select_server.select_address_to_choice()
    filtered_results = [
        result for result in res
    ]

    if res:
        for record in filtered_results:
            address_id, city, district, street, dom, apartment, entrance = record
            row = ft.Row(
                [
                    ft.Checkbox(),
                    ft.Text(f"р.{district} ул.{street} д.{dom} кв.{apartment}", size=17)
                ]
            )
            column_content.controls.append(row)
    column_content.controls.append(
        ft.Container(
            content=ft.Text("Назначить"),
            padding=ft.padding.only(top=20, bottom=20),
            margin=5,
            border_radius=15,
            bgcolor=const.tasks_completed_text_color,
            ink=True,
            shadow=ft.BoxShadow(
                offset=ft.Offset(0, 7),
                blur_radius=10,
                color=ft.colors.BLACK38
            ),
            alignment=ft.alignment.center,
        )
    )
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
