import scr.navigation_apps.admin.admin_screen
import scr.navigation_apps.users.users_screen
import scr.navigation_apps.users.user_seting_page
import scr.navigation_apps.users.ratyng_user_screen
import scr.navigation_apps.users.map_user_screen
import scr.BD.bd_user
import flet as ft


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
        if nav == 0:
            if privileges == 1:
                pass
            else:
                scr.navigation_apps.users.users_screen.user_main(page)
        elif nav == 1:
            if privileges == 1:
                pass
            else:
                scr.navigation_apps.users.ratyng_user_screen.rating(page)
        elif nav == 2:
            if privileges == 1:
                pass
            else:
                scr.navigation_apps.users.map_user_screen.map(page)
        elif nav == 3:
            if privileges == 1:
                pass
            else:
                scr.navigation_apps.users.user_seting_page.setting(page)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.TASK_ROUNDED, ),
            ft.NavigationBarDestination(icon=ft.icons.BAR_CHART),
            ft.NavigationBarDestination(icon=ft.icons.LOCATION_ON),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS),
        ], on_change=navigate,
        elevation=0.1
    )
