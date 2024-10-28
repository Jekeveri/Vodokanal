import datetime
import os
import flet as ft
import scr.BD.bd_users.update_bd
import scr.BD.bd_users.delete_bd
import scr.BD.bd_users.insert_bd
import scr.BD.bd_users.select_bd
import scr.BD.bd_server
import scr.toggle_user_sessions
import scr.func
import scr.constants as const
import scr.navigation_apps.users.doing_work.chose_meters

m_value = ""
m_remark = ""
statuses = []
sorting = "Адрес"
search_history_list = []  # длина будет--------------------------максимум 10


def update_data(page, meter_id, id_task, where):
    screen_width = page.width
    screen_height = page.height

    def bottom_sheet_yes(e):
        page.close(bottom_sheet)
        page.close(dlg_modal)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    def bottom_sheet_no(e):
        page.close(bottom_sheet)

    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Вы точно хотите выйти?"),
                    ft.Text("Не сохраненные данные удалятся!"),
                    ft.Row(
                        [
                            ft.ElevatedButton("Да", on_click=bottom_sheet_yes),
                            ft.ElevatedButton("Нет", on_click=bottom_sheet_no)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
            ),
        ),
    )

    # Обработка нажатия кнопки сохранения
    def on_click_time_task(e):
        today = datetime.datetime.now().strftime("%H:%M:%S")
        average_consumption = 20
        value = int(reading_value.value) - int(last_reading_value)
        procent = abs(average_consumption - abs(value)) / ((abs(value) + average_consumption) / 2) * 100
        if remark.value and reading_value.value:  # Упростил проверку на пустоту
            if procent < 20 or value == 0:
                scr.BD.bd_users.update_bd.update_local_tasks(
                    str(today), id_task, reading_value.value, remark.value, meter_id)
                scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)
                page.close(dlg_modal)
                page.update()
            else:
                scr.func.show_alert_yn(page, "Прикрепите фото/видео прибора")
        else:
            reading_value.error_text = "✱ Введите данные"
            page.update()

    # Обработка нажатия кнопки назад
    def on_click_back(e):
        if reading_value.value != new_reading_value or remark.value != meter_remark:
            page.open(bottom_sheet)
        else:
            page.close(dlg_modal)
            scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    # Инициализация переменных на случай, если данные не будут получены
    marka = "Неизвестно"
    meter_number = "Неизвестно"
    instalation_day = "Неизвестно"
    meter_type = "Неизвестно"
    seal_number = "Неизвестно"
    location = "Неизвестно"
    meter_remark = "Неизвестно"

    results_meters_data = scr.BD.bd_users.select_bd.select_meters_data_new_for_one(id_task, meter_id)
    if results_meters_data:
        for result in results_meters_data:
            id_meters, meter_number, instalation_day, meter_type, id_address, marka, seal_number, \
                date_next_verification, location, status_filling, meter_remark, type_protection = result
    result_info_meters = f"Счетчик: {marka} \nДата установки: {instalation_day} \nТип: {meter_type}"

    dict_checkboxes = {}

    def on_checkbox_change(checkbox, name):
        dict_checkboxes[name] = checkbox.value

    def toggle_checkbox(e, checkbox, name):
        checkbox.value = not checkbox.value
        checkbox.update()
        on_checkbox_change(checkbox, name)

    marka_checkbox = ft.Ref[ft.Checkbox]()
    serial_number_checkbox = ft.Ref[ft.Checkbox]()
    seal_number_checkbox = ft.Ref[ft.Checkbox]()

    dict_checkboxes["marka"] = False
    dict_checkboxes["serial_number"] = False
    dict_checkboxes["seal"] = False

    content = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Checkbox(on_change=lambda e, name="marka": on_checkbox_change(e.control, name),
                                        ref=marka_checkbox),
                            ft.Text("Марка счетчика совпадает с "),
                        ]),
                        ft.Row([
                            ft.Text(f"{marka}", weight=ft.FontWeight.BOLD),
                            ft.Text("?")
                        ])
                    ]
                ),
                on_click=lambda e, name="marka": toggle_checkbox(e, marka_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Checkbox(on_change=lambda e, name="serial_number": on_checkbox_change(e.control, name),
                                        ref=serial_number_checkbox),
                            ft.Text("Заводской номер счетчика"),
                        ]),
                        ft.Row([
                            ft.Text("совпадает с "),
                            ft.Text(f"{meter_number}", weight=ft.FontWeight.BOLD),
                            ft.Text("?")
                        ]),
                    ]
                ),
                on_click=lambda e, name="serial_number": toggle_checkbox(e, serial_number_checkbox.current, name)
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Checkbox(on_change=lambda e, name="seal": on_checkbox_change(e.control, name),
                                        ref=seal_number_checkbox),
                            ft.Text("Номер пломбы совпадает с "),
                        ]),
                        ft.Row([
                            ft.Text(f"{seal_number}", weight=ft.FontWeight.BOLD),
                            ft.Text("?")
                        ]),
                    ]
                ),
                on_click=lambda e, name="seal": toggle_checkbox(e, seal_number_checkbox.current, name)
            )
        ]
    )

    def button_yes(e):
        chect_list = [name for name, is_checked in dict_checkboxes.items() if not is_checked]
        message_string = ""
        today = datetime.datetime.now()
        date = datetime.datetime.strptime(date_next_verification, "%Y-%m-%d")
        total_months = (today.year - date.year) * 12 + (today.month - date.month)
        if not chect_list:
            page.close(check_meters_data)
        for chect in chect_list:
            if chect == "marka":
                message_string += "Включите в акт несоответствие Марки счетчика\n"
            elif chect == "serial_number":
                message_string += "Включите в акт несоответствие Заводского номера\n"
            elif chect == "seal":
                message_string += "Включите в акт несоответствие Номера пломбы\n"
        if total_months >= 6:
            message_string += "Включите в акт предписание о скором выходе МПИ\n"
        page.open(dlg_modal)
        scr.func.show_alert_yn(page, message_string)
        page.close(check_meters_data)

    def button_no(e):
        page.close(check_meters_data)
        scr.navigation_apps.users.doing_work.chose_meters.show_meters_data(page, id_task, where)

    check_meters_data = ft.AlertDialog(
        modal=True,
        content=content,
        title=ft.Text("Уточните Данные"),
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Да", on_click=button_yes, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=button_no, bgcolor=ft.colors.BLUE_200),
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    last_reading_date = "Неизвестно"
    last_reading_value = "Неизвестно"
    new_reading_value = ""

    results = scr.BD.bd_users.select_bd.select_meter_reading_new(meter_id)
    if results:
        for result in results:
            id_meters, last_reading_date, last_reading_value, new_reading_date, new_reading_value = result
            if new_reading_value is None:
                new_reading_value = ""

    reading_value = ft.TextField(label="Показания счетчика", value=new_reading_value)
    remark = ft.TextField(label="Примечания по счетчику", value=meter_remark, multiline=True, min_lines=1,
                          max_lines=3)

    title = ft.Column(
        [
            ft.Text(result_info_meters, size=17),
        ]
    )

    # Поля ввода для редактирования данных счетчика
    marka_textfield = ft.TextField(label="Марка", value=marka)
    meter_number_textfield = ft.TextField(label="Заводской номер", value=meter_number)
    seal_number_textfield = ft.TextField(label="Номер пломбы", value=seal_number)
    location_textfield = ft.TextField(label="Место расположения", value=location)
    meter_type_textfield = ft.TextField(label="Тип услуги", value=meter_type)

    # Расширяемый список для редактирования данных счетчика
    dop_buttons_redact = ft.Row(
        [
            ft.Column(
                [
                    marka_textfield,
                    meter_number_textfield,
                    seal_number_textfield,
                    location_textfield,
                    meter_type_textfield,
                ]
            )
        ]
    )

    panels = [
        ft.ExpansionPanel(
            header=ft.Text("Редактирование данных счётчика"),
            can_tap_header=True,
            content=dop_buttons_redact,
            expanded=False,
            aspect_ratio=100,
            bgcolor=ft.colors.BLUE_100
        ),
    ]

    panel_list = ft.ExpansionPanelList(
        elevation=10,
        controls=panels
    )

    def save_image_to_db(file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)
        scr.BD.bd_users.insert_bd.insert_photo(file_name, file_data, id_task, meter_id)

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                save_image_to_db(file.path)  # Сохраняем изображение в базу данных
                update_saving_data(meter_id, id_task)
                scr.func.show_snack_bar(page, f"Изображение {file.name} сохранено в базу данных.")
        else:
            scr.func.show_snack_bar(page, "Выбор файла отменен.")

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    selected_images = {}
    save_photos = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, )

    def on_click_delete_photo(e, id_p, meter_id, id_task):
        scr.BD.bd_users.delete_bd.delete_photo_db(id_p)
        if id_p in selected_images:
            del selected_images[id_p]
        update_saving_data(meter_id, id_task)
        page.update()

    def update_saving_data(meter_id, id_task):
        images = scr.BD.bd_users.select_bd.select_photo_data_new(meter_id, id_task)
        if images:
            selected_images.clear()
            for result in images:
                id_photo, value_photo, file_name1, task_id, meter_id = result
                selected_images[id_photo] = file_name1  # Добавляем фото в словарь
        save_photos.controls.clear()
        if selected_images:
            for id_page, file in selected_images.items():
                save_photos.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(file),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, id_p=id_page: on_click_delete_photo(e, id_p, meter_id, id_task)
                                )
                            ]
                        )
                    )
                )
        page.update()

    update_saving_data(meter_id, id_task)

    def zagr(e):
        pick_files_dialog.pick_files(allow_multiple=True, allowed_extensions=["jpeg", "gif", "png", "webp"])

    # Основной контент модального окна
    meters_data = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Дата контрольных показаний: {last_reading_date}", size=17),
                ft.Text(f"Контрольные показания: {last_reading_value}", size=17),
                reading_value,
                remark,
                save_photos,
                ft.ElevatedButton("Добавить фотографию", on_click=zagr),
                ft.Column(
                    [
                        panel_list
                    ], scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ], scroll=ft.ScrollMode.AUTO,
        )
    )

    # Модальное окно с данными счетчика
    dlg_modal = ft.AlertDialog(
        modal=True,
        content=meters_data,
        title=title,
        actions=[
            ft.Row(
                [
                    ft.ElevatedButton("Сохранить", on_click=on_click_time_task, bgcolor=ft.colors.BLUE_200),
                    ft.ElevatedButton("Назад", on_click=on_click_back, bgcolor=ft.colors.RED_200)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    # Очищаем и обновляем контент страницы
    page.controls.clear()
    page.open(check_meters_data)
    page.update()
