import flet as ft

import scr.func
import scr.BD.bd_user
import scr.navigation_apps.navigations
import scr.constants as const

def map(page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.controls.clear()

    page.appbar = ft.AppBar(
        title=ft.Text("Карта"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50
    )
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(src=const.tasks_line_icon),
                        ft.Text("Здесь пока что ничего нет", size=40),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Text("оно вообще не нужно но мб и будет", size=5)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
