import flet as ft
import scr.exit


def main(page: ft.Page):
    page.theme_mode = 'light'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    scr.exit.exit_account(page)


ft.app(target=main, view=ft.FLET_APP)
