from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
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

class DataEntryApp(MDApp):
    def build(self):
        self.data = load_data()
        self.filtered_data = self.data.copy()
        self.dialog = None
        self.edit_index = None

        self.screen = MDScreen()
        self.layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        self.search_field = MDTextField(hint_text="بحث...", on_text_validate=self.perform_search)
        self.layout.add_widget(self.search_field)

        self.table = MDDataTable(
            column_data=[
                ("الاسم الثلاثي", dp(30)),
                ("اسم الأم", dp(25)),
                ("المواليد", dp(20)),
                ("السكن", dp(25)),
                ("الرقم الذاتي", dp(25)),
                ("رقم الهاتف", dp(25)),
                ("تعديل", dp(20)),
                ("حذف", dp(20)),
            ],
            row_data=self.get_table_data(),
            use_pagination=True,
        )
        self.layout.add_widget(self.table)

        self.add_button = MDRaisedButton(text="إضافة بيانات", on_release=self.open_add_dialog)
        self.layout.add_widget(self.add_button)

        self.screen.add_widget(self.layout)
        return self.screen

    def get_table_data(self):
        return [
            (
                item["name"],
                item["mother"],
                item["birth"],
                item["address"],
                item["id"],
                item["phone"],
                ("✏", lambda x=item: self.edit_item(x)),
                ("🗑", lambda x=item: self.delete_item(x)),
            )
            for item in self.filtered_data
        ]

    def refresh_table(self):
        self.table.row_data = self.get_table_data()

    def open_add_dialog(self, *args):
        self.dialog_content = MDBoxLayout(orientation="vertical", spacing=10)
        self.fields = {
            "name": MDTextField(hint_text="الاسم الثلاثي"),
            "mother": MDTextField(hint_text="اسم الأم"),
            "birth": MDTextField(hint_text="المواليد"),
            "address": MDTextField(hint_text="السكن"),
            "id": MDTextField(hint_text="الرقم الذاتي"),
            "phone": MDTextField(hint_text="رقم الهاتف"),
        }
        for field in self.fields.values():
            self.dialog_content.add_widget(field)

        self.dialog = MDDialog(
            title="إدخال البيانات",
            type="custom",
            content_cls=self.dialog_content,
            buttons=[
                MDRaisedButton(text="حفظ", on_release=self.save_item),
                MDRaisedButton(text="إلغاء", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def save_item(self, *args):
        item = {k: field.text for k, field in self.fields.items()}
        if self.edit_index is not None:
            self.data[self.edit_index] = item
            self.edit_index = None
        else:
            self.data.append(item)
        save_data(self.data)
        self.filtered_data = self.data.copy()
        self.refresh_table()
        self.dialog.dismiss()

    def delete_item(self, item):
        self.data.remove(item)
        save_data(self.data)
        self.filtered_data = self.data.copy()
        self.refresh_table()

    def edit_item(self, item):
        self.edit_index = self.data.index(item)
        self.open_add_dialog()
        for k in self.fields:
            self.fields[k].text = item[k]

    def perform_search(self, *args):
        query = self.search_field.text.strip().lower()
        if query == "":
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = [
                item for item in self.data
                if query in json.dumps(item, ensure_ascii=False).lower()
            ]
        self.refresh_table()

if __name__ == "__main__":
    DataEntryApp().run()
