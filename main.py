import flet as ft
import json
import os

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(page: ft.Page):
    page.title = "إدارة البيانات"
    page.scroll = "auto"
    data = load_data()
    filtered_data = data.copy()
    edit_index = None

    # البحث
    search_field = ft.TextField(label="بحث...", on_change=lambda e: perform_search())

    # الحقول
    name_field = ft.TextField(label="الاسم الثلاثي")
    mother_field = ft.TextField(label="اسم الأم")
    birth_field = ft.TextField(label="المواليد")
    address_field = ft.TextField(label="السكن")
    id_field = ft.TextField(label="الرقم الذاتي")
    phone_field = ft.TextField(label="رقم الهاتف")

    # الحقول مجمعة
    field_controls = [
        name_field,
        mother_field,
        birth_field,
        address_field,
        id_field,
        phone_field,
    ]

    dialog = None

    def refresh_table():
        rows = []
        for i, item in enumerate(filtered_data):
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["name"])),
                    ft.DataCell(ft.Text(item["mother"])),
                    ft.DataCell(ft.Text(item["birth"])),
                    ft.DataCell(ft.Text(item["address"])),
                    ft.DataCell(ft.Text(item["id"])),
                    ft.DataCell(ft.Text(item["phone"])),
                    ft.DataCell(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=i: edit_item(idx))),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=i: delete_item(idx))),
                ]
            )
            rows.append(row)
        table.rows = rows
        page.update()

    def open_dialog(is_edit=False):
        nonlocal dialog
        dialog = ft.AlertDialog(
            title=ft.Text("تعديل البيانات" if is_edit else "إدخال البيانات"),
            content=ft.Column(controls=field_controls, tight=True),
            actions=[
                ft.TextButton("إلغاء", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("حفظ", on_click=lambda e: save_item())
            ],
            on_dismiss=lambda e: None,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def clear_fields():
        for f in field_controls:
            f.value = ""

    def open_add_dialog(e=None):
        nonlocal edit_index
        edit_index = None
        clear_fields()
        open_dialog()

    def save_item():
        nonlocal edit_index, data, filtered_data
        item = {
            "name": name_field.value,
            "mother": mother_field.value,
            "birth": birth_field.value,
            "address": address_field.value,
            "id": id_field.value,
            "phone": phone_field.value
        }
        if edit_index is not None:
            data[edit_index] = item
        else:
            data.append(item)
        save_data(data)
        filtered_data = data.copy()
        refresh_table()
        dialog.open = False
        page.update()

    def delete_item(index):
        del data[index]
        save_data(data)
        filtered_data[:] = data
        refresh_table()

    def edit_item(index):
        nonlocal edit_index
        edit_index = index
        item = filtered_data[index]
        name_field.value = item["name"]
        mother_field.value = item["mother"]
        birth_field.value = item["birth"]
        address_field.value = item["address"]
        id_field.value = item["id"]
        phone_field.value = item["phone"]
        open_dialog(is_edit=True)

    def perform_search():
        nonlocal filtered_data
        query = search_field.value.strip().lower()
        if query == "":
            filtered_data = data.copy()
        else:
            filtered_data = [
                item for item in data
                if query in json.dumps(item, ensure_ascii=False).lower()
            ]
        refresh_table()

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الاسم الثلاثي")),
            ft.DataColumn(ft.Text("اسم الأم")),
            ft.DataColumn(ft.Text("المواليد")),
            ft.DataColumn(ft.Text("السكن")),
            ft.DataColumn(ft.Text("الرقم الذاتي")),
            ft.DataColumn(ft.Text("رقم الهاتف")),
            ft.DataColumn(ft.Text("تعديل")),
            ft.DataColumn(ft.Text("حذف")),
        ],
        rows=[],
    )

    add_button = ft.ElevatedButton(text="إضافة بيانات", on_click=open_add_dialog)

    page.add(
        search_field,
        add_button,
        table,
    )

    refresh_table()

ft.app(target=main)
