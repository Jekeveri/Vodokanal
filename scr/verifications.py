import flet as ft

import scr.BD.bd_server
import scr.func
import scr.navigation_apps.navigations


def authentication(page):
    page.clean()
    page.navigation_bar = None
    page.appbar = None
    page.controls.clear()
    screen_width = page.width
    screen_height = page.height

    page.title = "Авторизация"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    login = ft.TextField(label="Логин", )
    password = ft.TextField(label="Пароль", )

    def on_click(e):
        if login.value != "" and password.value != "":
            scr.BD.bd_server.check_user_credentials(login.value, password.value, page)
        else:
            scr.func.show_snack_bar(page, "Неправильный логин или пароль.")

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        login,
                        password,
                        ft.ElevatedButton(text="Вход", on_click=on_click,)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=400,
                )
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()
