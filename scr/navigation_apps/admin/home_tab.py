import flet as ft
import scr.BD.bd_admin.local
import scr.toggle_user_sessions
import scr.constants as const


def home_tab(page):
    def on_click_exit(e):
        scr.BD.bd_admin.local.delete_data_db()
        scr.toggle_user_sessions.handle_user_sessions(page)

    # Ваша логика для главной вкладки
    content = ft.Container(content=ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.TIME_TO_LEAVE, color=ft.colors.WHITE),
            ft.Text("Выход", style=ft.TextStyle(color=ft.colors.WHITE))
        ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(top=20, left=50, right=50, bottom=20),
        bgcolor=const.tasks_completed_text_color,
        border_radius=ft.border_radius.all(25),
        shadow=ft.BoxShadow(
            offset=ft.Offset(5, 5),
            blur_radius=10,
            color=ft.colors.BLACK38
        ),
        ink=True,
        ink_color=ft.colors.RED_200,
        on_click=on_click_exit,
    ))
    return content
