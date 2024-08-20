import scr.navigation_apps.admin.admin_screen
import scr.navigation_apps.users.users_screen
import scr.navigation_apps.users.user_setting_page
import scr.navigation_apps.users.ratyng_user_screen
import scr.navigation_apps.users.map_user_screen
import scr.BD.bd_user
import flet as ft

import scr.constants as const


# тут программа смотрит какая роль у человека
def role_definition(privileges, page):
    # Тут мы ищим данные уже из таблици юзера как то так
    if privileges == 1:
        scr.navigation_apps.admin.admin_screen.admin_main(page)
    else:
        employee_navigation(privileges, page)
        scr.navigation_apps.users.users_screen.user_main(page)


def employee_navigation(privileges, page):
    def navigate(e):
        nav = page.navigation_bar.selected_index
        page.controls.clear()
        if privileges == 1:
            pass
        else:
            if nav == 0:
                scr.navigation_apps.users.users_screen.user_main(page)
            elif nav == 1:
                scr.navigation_apps.users.ratyng_user_screen.rating(page)
            elif nav == 2:
                scr.navigation_apps.users.map_user_screen.map(page)
            elif nav == 3:
                scr.navigation_apps.users.user_setting_page.setting(page)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.Image(src=const.tasks_line_icon),
            ft.NavigationBarDestination(const.setting_line_icon),
            ft.NavigationBarDestination(icon=ft.icons.BAR_CHART),
            ft.NavigationBarDestination(icon=ft.icons.LOCATION_ON),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS),
        ], on_change=navigate,
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        indicator_color=ft.colors.TRANSPARENT,
        height=50
    )
