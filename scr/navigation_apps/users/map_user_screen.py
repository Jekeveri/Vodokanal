import flet as ft

import scr.func
import scr.navigation_apps.navigations


def map(page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.controls.clear()

    page.appbar = ft.AppBar(
        title=ft.Text("Обратная связь"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.ProgressRing(scale=2, color=ft.colors.BLACK45),
                                ft.Text("Здесь пока что ничего нет", size=20)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=50
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
