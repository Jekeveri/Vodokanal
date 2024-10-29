import flet as ft
from scr.navigation_apps.admin.home_tab import home_tab
from scr.navigation_apps.admin.search_tab import search_tab
from scr.navigation_apps.admin.assignment_tab import assignment_tab
from scr.navigation_apps.admin.controller_tab import controller_tab
from scr.navigation_apps.admin.task_controller import employer_tab

tabs = []  # Список для хранения вкладок


def admin_main(page):
    page.title = "Admin Panel"
    page.controls.clear()

    global t  # Делаем t глобальным, чтобы можно было добавлять вкладки
    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        scrollable=True,
        tabs=[
            ft.Tab(text="Главная", content=home_tab(page)),
            ft.Tab(text="Поиск", content=search_tab(page)),
            ft.Tab(text="Назначение", content=assignment_tab(page)),
            ft.Tab(text="Контроллеры", content=controller_tab(page)),
        ],
        expand=1,
    )
    page.add(t)
    page.update()


def add_new_tab(page, selected_rows):
    new_tab = ft.Tab(text="Назначение - Задач", content=employer_tab(page, selected_rows))
    t.tabs.append(new_tab)
    t.selected_index = len(t.tabs) - 1  # Устанавливаем новую вкладку активной
    t.update()


def return_tab():
    global t
    if len(t.tabs) > 1:
        t.tabs.pop()  # Удаляем текущую вкладку

        t.selected_index = len(t.tabs) - 2  # Устанавливаем предыдущую вкладку активной
        t.update()
    else:
        print("Нельзя удалить последнюю вкладку")
