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
    page.title = "تطبيق إدخال بيانات"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.window_width = 700
    page.window_height = 600

    data = load_data()
    filtered_data = data.copy()
    selected_index = None

    # إدخالات الحقول
    name_field = ft.TextField(label="الاسم", width=200)
    mother_field = ft.TextField(label="اسم الأم", width=200)
    birth_field = ft.TextField(label="المواليد", width=200)
    address_field = ft.TextField(label="السكن", width=200)
    id_field = ft.TextField(label="الرقم الذاتي", width=200)
    phone_field = ft.TextField(label="رقم الهاتف", width=200)
    search_field = ft.TextField(label="بحث", width=300)

    # جدول عرض البيانات
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الاسم")),
            ft.DataColumn(ft.Text("الأم")),
            ft.DataColumn(ft.Text("المواليد")),
            ft.DataColumn(ft.Text("السكن")),
            ft.DataColumn(ft.Text("الرقم الذاتي")),
            ft.DataColumn(ft.Text("رقم الهاتف")),
            ft.DataColumn(ft.Text("تعديل")),
            ft.DataColumn(ft.Text("حذف")),
        ],
        rows=[]
    )

    def update_table():
        data_table.rows.clear()
        for i, row in enumerate(filtered_data):
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row["name"])),
                        ft.DataCell(ft.Text(row["mother"])),
                        ft.DataCell(ft.Text(row["birth"])),
                        ft.DataCell(ft.Text(row["address"])),
                        ft.DataCell(ft.Text(row["id"])),
                        ft.DataCell(ft.Text(row["phone"])),
                        ft.DataCell(ft.IconButton(
                            icon=ft.icons.EDIT,
                            on_click=lambda e, idx=i: edit_record(idx)
                        )),
                        ft.DataCell(ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, idx=i: delete_record(idx)
                        )),
                    ]
                )
            )
        page.update()

    def clear_fields():
        name_field.value = ""
        mother_field.value = ""
        birth_field.value = ""
        address_field.value = ""
        id_field.value = ""
        phone_field.value = ""

    def add_record(e):
        nonlocal data, filtered_data
        if not name_field.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("حقل الاسم مطلوب!"))
            page.snack_bar.open = True
            page.update()
            return
        new_entry = {
            "name": name_field.value.strip(),
            "mother": mother_field.value.strip(),
            "birth": birth_field.value.strip(),
            "address": address_field.value.strip(),
            "id": id_field.value.strip(),
            "phone": phone_field.value.strip()
        }
        data.append(new_entry)
        save_data(data)
        filtered_data = data.copy()
        update_table()
        clear_fields()

    def edit_record(idx):
        nonlocal selected_index
        selected_index = idx
        record = filtered_data[idx]
        name_field.value = record["name"]
        mother_field.value = record["mother"]
        birth_field.value = record["birth"]
        address_field.value = record["address"]
        id_field.value = record["id"]
        phone_field.value = record["phone"]
        add_btn.text = "تحديث"
        page.update()

    def update_record(e):
        nonlocal selected_index, data, filtered_data
        if selected_index is None:
            return
        updated_entry = {
            "name": name_field.value.strip(),
            "mother": mother_field.value.strip(),
            "birth": birth_field.value.strip(),
            "address": address_field.value.strip(),
            "id": id_field.value.strip(),
            "phone": phone_field.value.strip()
        }
        # تحديث في قائمة البيانات الأصلية:
        # لأن filtered_data قد تكون نتيجة بحث، نحتاج لتحديد العنصر الصحيح في data
        original_idx = data.index(filtered_data[selected_index])
        data[original_idx] = updated_entry

        save_data(data)
        filtered_data = data.copy()
        update_table()
        clear_fields()
        add_btn.text = "إضافة"
        selected_index = None
        page.update()

    def delete_record(idx):
        nonlocal data, filtered_data
        # حذف العنصر الأصلي من data
        original_idx = data.index(filtered_data[idx])
        del data[original_idx]
        save_data(data)
        filtered_data = data.copy()
        update_table()
        page.update()

    def on_add_update_click(e):
        if add_btn.text == "إضافة":
            add_record(e)
        else:
            update_record(e)

    def search_records(e):
        nonlocal filtered_data
        keyword = search_field.value.strip()
        if keyword == "":
            filtered_data = data.copy()
        else:
            filtered_data = [
                item for item in data if
                keyword in item["name"] or
                keyword in item["mother"] or
                keyword in item["birth"] or
                keyword in item["address"] or
                keyword in item["id"] or
                keyword in item["phone"]
            ]
        update_table()

    add_btn = ft.ElevatedButton(text="إضافة", on_click=on_add_update_click)

    # بناء الواجهة
    page.add(
        ft.Row(
            controls=[
                ft.Column(controls=[name_field, mother_field, birth_field], spacing=10),
                ft.Column(controls=[address_field, id_field, phone_field], spacing=10),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=50
        ),
        ft.Row(
            controls=[
                add_btn,
                ft.ElevatedButton(text="مسح الحقول", on_click=lambda e: clear_fields()),
                search_field,
                ft.ElevatedButton(text="بحث", on_click=search_records)
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        ft.Divider(),
        data_table
    )

    update_table()

if __name__ == "__main__":
    ft.app(target=main)
