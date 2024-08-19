import flet as ft

import scr.exit
import scr.func
import scr.BD.bd_user
import scr.navigation_apps.navigations


def setting(page):
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()

    def on_click_exit(e):
        scr.BD.bd_user.delete_data_db()
        scr.exit.exit_account(page)

    scr.func.show_snack_bar(page, "Setting")
    result = scr.BD.bd_user.select_user_data()

    def on_hover(e):
        e.control.bgcolor = ft.colors.RED_200 if e.data == "true" else ft.colors.BLUE_GREY_100
        e.control.scale = 1.1 if e.data == "true" else 1
        e.control.update()

    bte = ft.Container(
        content=ft.Text("Выход"),
        padding=ft.padding.only(top=20, left=50, right=50, bottom=20),
        bgcolor=ft.colors.BLUE_GREY_100,
        border_radius=ft.border_radius.all(25),
        on_click=on_click_exit,
        on_hover=on_hover,
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True
    )

    button_exit = ft.ElevatedButton("Выход", on_click=on_click_exit, bgcolor=ft.colors.RED_200)
    if result:
        for record in result:
            login_user, password_user, privileges, first_name, last_name = record

    page.add(
        ft.Column(
            [
                ft.Text("Профиль сотрудника"),
                ft.Text(f"Сотрудник: {last_name} {first_name}"),
                ft.Text(f"Логин: {login_user}"),
                ft.Text(f"Пароль: {password_user}"),
                button_exit,
                bte
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()
