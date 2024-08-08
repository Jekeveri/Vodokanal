import flet as ft

import scr.BD.bd_user
import scr.func
import scr.navigation_apps.navigations


def authentication(page):
    page.clean()
    page.controls.clear()
    screen_width = page.window_width
    screen_height = page.window_height

    page.title = "Авторизация"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    login = ft.TextField(label="Логин", width=screen_width * 0.2)
    password = ft.TextField(label="Пароль", width=screen_width * 0.2)

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
                        ft.ElevatedButton(text="Вход", on_click=on_click, width=screen_width * 0.1)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=400,
                )
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()
