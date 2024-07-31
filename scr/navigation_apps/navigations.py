import scr.navigation_apps.admin.admin_screen
import scr.navigation_apps.users.users_screen
import scr.BD.bd_user


# тут программа смотрит какая роль у человека
def role_definition(privileges, page):
    print("Заходит")
    # Тут мы ищим данные уже из таблици юзера как то так
    if privileges == 1:
        scr.navigation_apps.admin.admin_screen.admin_main(page)
    else:
        print("Заходит1")
        scr.navigation_apps.users.users_screen.user_main(page)
