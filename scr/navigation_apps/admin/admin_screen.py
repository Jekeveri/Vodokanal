import flet as ft

import scr.BD.bd_user
import scr.exit


def admin_main(page):
    page.clean()
    page.controls.clear()
    page.title = "Администратор"
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
    page.update()
