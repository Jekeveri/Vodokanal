import flet as ft
import scr.BD.bd_admin.select_server  # Импортируем функцию для получения данных из БД

import scr.navigation_apps.admin.admin_screen as ad


def search_tab(page):
    search_input = ft.TextField(label="Поиск", width=300, on_change=lambda e: update_table())
    filter_dropdown = ft.Dropdown(
        label="Фильтр",
        options=[
            ft.dropdown.Option("Все"),
            ft.dropdown.Option("По адресу"),
            ft.dropdown.Option("По ФИО"),
        ],
        value="Все",
        on_change=lambda e: update_table()
    )

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Checkbox(on_change=lambda e: toggle_all_checkboxes(e.control.value))),
            ft.DataColumn(ft.Text("ФИО")),
            ft.DataColumn(ft.Text("Адрес")),
            ft.DataColumn(ft.Text("Телефон")),
            ft.DataColumn(ft.Text("Личный счет")),
            ft.DataColumn(ft.Text("Дата")),
            ft.DataColumn(ft.Text("Статус задачи")),
            ft.DataColumn(ft.Text("Цель")),
            ft.DataColumn(ft.Text("Тип адреса")),
            ft.DataColumn(ft.Text("ID")),
        ],
        rows=[],
        border=ft.border.all(2, "grey"),
        border_radius=10,
        data_row_max_height=100,
        vertical_lines=ft.BorderSide(1, "grey"),
        horizontal_lines=ft.BorderSide(1, "grey"),
    )

    selected_rows = set()

    def update_table():
        nonlocal selected_rows
        search_value = search_input.value.lower()
        filter_value = filter_dropdown.value

        results = scr.BD.bd_admin.select_server.select_task_data_all()

        filtered_results = [
            record for record in results
            if (filter_value == "Все" or
                (
                            filter_value == "По адресу" and search_value in f"{record[3]}, {record[4]}, {record[5]}, {record[6]}, {record[7]}".lower()) or
                (filter_value == "По ФИО" and search_value in record[1].lower()))
        ]

        data_table.rows.clear()
        for row_data in filtered_results:
            full_address = (
                f"Город: {row_data[3]}\n"
                f"Район: {row_data[4]}\n"
                f"Улица: {row_data[5]}\n"
                f"Дом: {row_data[6]} "
                f"Квартира: {row_data[7]}"
            )
            checkbox = ft.Checkbox(value=row_data[0] in selected_rows,
                                   on_change=lambda e, id=row_data[0]: select_row(id, e.control.value))
            row_data_combined = (
                checkbox,
                row_data[1],
                full_address,
                row_data[13],
                row_data[14],
                row_data[15],
                row_data[17],
                row_data[18],
                row_data[20],
                row_data[0],
            )
            background_color = "lightgrey" if row_data[0] in selected_rows else "white"
            data_table.rows.append(
                ft.DataRow(cells=[
                                     ft.DataCell(checkbox)
                                 ] + [
                                     ft.DataCell(ft.Text(str(cell), max_lines=6, overflow=ft.TextOverflow.FADE)) for
                                     cell in row_data_combined[1:]
                                 ], color=background_color)
            )
        page.update()

    def toggle_all_checkboxes(is_selected):
        nonlocal selected_rows
        if is_selected:
            selected_rows = {int(row.cells[9].content.value) for row in data_table.rows}
            update_button_visibility()
        else:
            selected_rows.clear()
            update_button_visibility()

        for row in data_table.rows:
            checkbox = row.cells[0].content
            checkbox.value = is_selected
            row.color = "lightgrey" if is_selected else "white"

        page.update()

    def select_row(row_id, is_selected):
        nonlocal selected_rows
        if is_selected:
            selected_rows.add(row_id)
            update_button_visibility()
        else:
            selected_rows.discard(row_id)
            update_button_visibility()
        update_table()

    def update_button_visibility():
        if len(selected_rows) == 1:
            button_edit.visible = True
            button_action_2.visible = False
        elif len(selected_rows) > 1:
            button_edit.visible = False
            button_action_2.visible = True
        else:
            button_edit.visible = False
            button_action_2.visible = False
        page.update()

    update_table()

    scrollable_table = ft.Container(
        content=ft.Column([
            ft.Row([
                data_table
            ], scroll=ft.ScrollMode.AUTO)
        ], scroll=ft.ScrollMode.AUTO),
        expand=True,
        height=400
    )

    button_edit = ft.Container(
        ft.Row(
            [
                ft.ElevatedButton("Редактировать",
                                  on_click=lambda e: print(f"Выбрана строка с ID: {list(selected_rows)[0]}"),
                                  disabled=True),
                ft.ElevatedButton("Удалить",
                                  on_click=lambda e: print(f"Выбрана строка с ID: {list(selected_rows)[0]}"),
                                  disabled=True),
                ft.ElevatedButton("Подробнее",
                                  on_click=lambda e: print(f"Выбрана строка с ID: {list(selected_rows)[0]}"),
                                  disabled=True),
                ft.ElevatedButton("Переназначить",
                                  on_click=lambda e: ad.add_new_tab(page, selected_rows), disabled=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        visible=False
    )

    button_action_2 = ft.Container(
        ft.Row(
            [
                ft.ElevatedButton("Удалить",
                                  on_click=lambda e: print(f"Выбрана строка с ID: {list(selected_rows)[0]}"),
                                  disabled=True),
                ft.ElevatedButton("Переназначить",
                                  on_click=lambda e: ad.add_new_tab(page, selected_rows), disabled=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,

        ),
        visible=False
    )

    button_row = ft.Container(
        ft.Row(
            [
                ft.ElevatedButton("Добавить", on_click=lambda e: print("Добавить нажата"), disabled=True),
                button_edit,
                button_action_2
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=10),
    )

    top_bar = ft.Container(
        ft.Row(
            [
                search_input,
                filter_dropdown,
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=10)
    )

    content = ft.Column([
        top_bar,
        scrollable_table,
        button_row,
    ], expand=True)

    return content
