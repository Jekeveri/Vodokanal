import flet as ft
import scr.BD.bd_server  # Импортируем функцию для получения данных о сотрудниках
import scr.BD.bd_admin.update_server
import scr.navigation_apps.admin.admin_screen

emp_id = None


def employer_tab(page, id_tasks):
    search_input = ft.TextField(label="Поиск", width=300, on_change=lambda e: update_table())
    filter_dropdown = ft.Dropdown(
        label="Фильтр",
        options=[
            ft.dropdown.Option("Все"),
            ft.dropdown.Option("По имени"),
            ft.dropdown.Option("По телефону"),
        ],
        value="Все",
        on_change=lambda e: update_table()
    )

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Выбор")),
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("ФИО")),
            ft.DataColumn(ft.Text("Телефон")),
            ft.DataColumn(ft.Text("К-во задач сегодня")),
            ft.DataColumn(ft.Text("К-во выполненных задач сегодня")),
            ft.DataColumn(ft.Text("К-во невыполненных задач сегодня")),
            ft.DataColumn(ft.Text("Общее к-во невыполненных задач")),
        ],
        data=[],
        border=ft.border.all(2, "grey"),
        border_radius=10,
        data_row_max_height=100,
        vertical_lines=ft.BorderSide(1, "grey"),
        horizontal_lines=ft.BorderSide(1, "grey"),
    )

    selected_row = None

    def update_table():
        nonlocal selected_row
        search_value = search_input.value.lower()
        filter_value = filter_dropdown.value

        results = scr.BD.bd_server.select_employer_data_statistic_tasks()

        filtered_results = [
            record for record in results
            if (filter_value == "Все" or
                (filter_value == "По имени" and search_value in record[1].lower()) or
                (filter_value == "По телефону" and search_value in record[2].lower()))
        ]

        data_table.rows.clear()
        for row_data in filtered_results:
            checkbox = ft.Checkbox(value=row_data[0] == selected_row,
                on_change=lambda e, id=row_data[0]: select_row(id, e.control.value))
            row_data_combined = (
                checkbox,
                row_data[0],
                row_data[1],
                row_data[2],
                row_data[3],
                row_data[4],
                row_data[5],
                row_data[6],
            )
            background_color = "lightgrey" if row_data[0] == selected_row else "white"
            data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(checkbox)
                ] + [
                    ft.DataCell(ft.Text(cell, max_lines=6, overflow=ft.TextOverflow.FADE)) for
                    cell in row_data_combined[1:]
                ], color=background_color)
            )
        page.update()

    update_table()

    def select_row(row_id, is_selected):
        nonlocal selected_row
        global emp_id
        if is_selected:
            selected_row = row_id
            bottom_bar.visible = True
            emp_id = row_id
        else:
            selected_row = None
            bottom_bar.visible = False
        update_table()

    def update_task(e):
        scr.BD.bd_admin.update_server.set_employer_to_task(id_tasks, emp_id)
        scr.navigation_apps.admin.admin_screen.return_tab()


    bottom_bar = ft.Container(
        ft.Row([
            ft.ElevatedButton("Назначить", on_click=update_task),
        ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        visible=False,
        padding=ft.padding.symmetric(horizontal=10, vertical=10)
    )

    top_bar = ft.Container(
        ft.Row([
            search_input,
            filter_dropdown,
        ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=10)
    )

    scrollable_table = ft.Container(
        content=ft.Column([
            ft.Row([
                data_table
            ], scroll=ft.ScrollMode.AUTO)
        ], scroll=ft.ScrollMode.AUTO),
        expand=True,
        height=400
    )

    content = ft.Column([
        top_bar,
        scrollable_table,
        bottom_bar
    ])

    return content