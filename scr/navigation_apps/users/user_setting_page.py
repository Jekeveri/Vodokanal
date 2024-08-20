import flet as ft

import scr.exit
import scr.func
import scr.BD.bd_user
import scr.navigation_apps.navigations


def setting(page):
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()
    page.appbar = ft.AppBar(
        title=ft.Text("Профиль сотрудника"),
        center_title=True,
        toolbar_height=40,
        bgcolor=ft.colors.BLUE_GREY_50
    )

    def on_click_exit(e):
        scr.BD.bd_user.delete_data_db()
        scr.exit.exit_account(page)

    scr.func.show_snack_bar(page, "Setting")
    result = scr.BD.bd_user.select_user_data()

    bte = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.TIME_TO_LEAVE, color=ft.colors.WHITE),
            ft.Text("Выход", style=ft.TextStyle(color=ft.colors.WHITE))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(top=20, left=50, right=50, bottom=20),
        bgcolor=ft.colors.BLUE_GREY_100,
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

    if result:
        for record in result:
            login_user, password_user, privileges, first_name, last_name = record

    page.add(
        ft.Column(
            [
                ft.Text(f"Сотрудник: {last_name} {first_name}"),
                ft.Text(f"Логин: {login_user}"),
                ft.Text(f"Пароль: {password_user}"),
                bte
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()
