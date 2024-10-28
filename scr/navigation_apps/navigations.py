import scr.navigation_apps.admin.admin_screen
import scr.navigation_apps.users.pages.main_users_screen
import scr.navigation_apps.users.pages.user_setting_screen
import scr.navigation_apps.users.pages.ratyng_user_screen
import scr.navigation_apps.users.pages.future_user_screen
import flet as ft


# тут программа смотрит какая роль у человека
def role_definition(privileges, page):
    if privileges == 1:
        scr.navigation_apps.admin.admin_screen.admin_main(page)
    elif privileges == 2:
        employee_navigation(privileges, page)
        scr.navigation_apps.users.pages.main_users_screen.user_main(page)
    else:
        debugging()


def employee_navigation(privileges, page):
    def navigate(e):
        nav = page.navigation_bar.selected_index
        page.controls.clear()
        if privileges == 1:
            pass
        else:
            if nav == 0:
                scr.navigation_apps.users.pages.main_users_screen.user_main(page)
            elif nav == 1:
                scr.navigation_apps.users.pages.future_user_screen.main(page)
            elif nav == 2:
                scr.navigation_apps.users.pages.ratyng_user_screen.rating(page)
            elif nav == 3:
                scr.navigation_apps.users.pages.user_setting_screen.setting(page)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.ASSIGNMENT_OUTLINED, selected_icon=ft.icons.ASSIGNMENT_ROUNDED),
            ft.NavigationBarDestination(icon=ft.icons.TIMER_OUTLINED, selected_icon=ft.icons.TIMER_ROUNDED),
            ft.NavigationBarDestination(icon=ft.icons.ASSESSMENT_OUTLINED, selected_icon=ft.icons.ASSESSMENT_ROUNDED),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS_OUTLINED, selected_icon=ft.icons.SETTINGS_ROUNDED),
        ], on_change=navigate,
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        indicator_color=ft.colors.TRANSPARENT,
        height=50
    )


def debugging():
    print('Тут можно добавить инфу по приложению, может быть обратную связь')

