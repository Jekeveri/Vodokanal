import flet as ft

import scr.navigation_apps.users.main_users_screen


def show_snack_bar(page, message):
    snack_bar = ft.SnackBar(
        content=ft.Text(message),
        open=True,
        duration=800
    )
    page.overlay.append(snack_bar)
    page.update()


def show_alert_yn(page, message, integer_for_someone):
    def on_button_yes(e):
        page.close(bs)
        # scr.navigation_apps.users.users_screen.add_meters(page, integer_for_someone)

    def on_button_no(e):
        page.close(bs)

    bs = ft.AlertDialog(
        modal=True,
        title=ft.Text("Предупреждение"),
        content=ft.Text(message),
        actions=[
            ft.ElevatedButton("ДА", on_click=on_button_yes),
            ft.ElevatedButton("НЕТ", on_click=on_button_no)
        ],
    )
    page.open(bs)
    page.update()
