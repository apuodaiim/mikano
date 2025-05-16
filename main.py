from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
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

class DataEntryApp(App):
    def build(self):
        self.data = load_data()
        self.filtered_data = self.data.copy()
        self.edit_index = None

        self.root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # حقل البحث
        self.search_input = TextInput(hint_text="بحث...", size_hint_y=None, height=40)
        self.search_input.bind(on_text_validate=self.perform_search)
        self.root_layout.add_widget(self.search_input)

        # المنطقة التي تحتوي على الجدول
        self.table_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.table_layout)

        self.root_layout.add_widget(self.scroll)

        # زر الإضافة
        add_button = Button(text="إضافة بيانات", size_hint_y=None, height=50)
        add_button.bind(on_release=self.open_add_popup)
        self.root_layout.add_widget(add_button)

        self.refresh_table()
        return self.root_layout

    def refresh_table(self):
        self.table_layout.clear_widgets()
        for index, item in enumerate(self.filtered_data):
            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(Label(text=item["name"]))
            row.add_widget(Label(text=item["mother"]))
            row.add_widget(Label(text=item["birth"]))
            row.add_widget(Label(text=item["address"]))
            row.add_widget(Label(text=item["id"]))
            row.add_widget(Label(text=item["phone"]))

            edit_btn = Button(text="تعديل", size_hint_x=None, width=70)
            edit_btn.bind(on_release=lambda x, i=index: self.edit_item(i))
            row.add_widget(edit_btn)

            del_btn = Button(text="حذف", size_hint_x=None, width=70)
            del_btn.bind(on_release=lambda x, i=index: self.delete_item(i))
            row.add_widget(del_btn)

            self.table_layout.add_widget(row)

    def open_add_popup(self, *args):
        self.popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.fields = {
            "name": TextInput(hint_text="الاسم الثلاثي"),
            "mother": TextInput(hint_text="اسم الأم"),
            "birth": TextInput(hint_text="المواليد"),
            "address": TextInput(hint_text="السكن"),
            "id": TextInput(hint_text="الرقم الذاتي"),
            "phone": TextInput(hint_text="رقم الهاتف"),
        }

        for field in self.fields.values():
            self.popup_layout.add_widget(field)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        save_btn = Button(text="حفظ")
        save_btn.bind(on_release=self.save_item)
        cancel_btn = Button(text="إلغاء")
        cancel_btn.bind(on_release=lambda x: self.popup.dismiss())
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)

        self.popup_layout.add_widget(btn_layout)

        self.popup = Popup(title="إدخال البيانات", content=self.popup_layout,
                           size_hint=(0.9, 0.9))
        self.popup.open()

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
        self.popup.dismiss()

    def delete_item(self, index):
        del self.data[index]
        save_data(self.data)
        self.filtered_data = self.data.copy()
        self.refresh_table()

    def edit_item(self, index):
        self.edit_index = index
        self.open_add_popup()
        item = self.data[index]
        for k in self.fields:
            self.fields[k].text = item[k]

    def perform_search(self, *args):
        query = self.search_input.text.strip().lower()
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
