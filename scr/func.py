import flet as ft


def show_snack_bar(page, message):
    snack_bar = ft.SnackBar(
        content=ft.Text(message),
        open=True,
        duration=800
    )
    page.overlay.append(snack_bar)
    page.update()