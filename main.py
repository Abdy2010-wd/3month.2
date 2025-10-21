import flet as ft 
from db import main_db


def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text))
        page.update()


    def create_task_row(task_id, task_text,completed):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        checkbox = ft.Checkbox(value=bool(completed), on_change=None)


        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Редактировать", on_click=enable_edit, icon_color=ft.Colors.ORANGE_700)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id)
            load_task()
        
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED)

        return ft.Row([checkbox, task_field, edit_button, save_button, delete_button])

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completed=None))

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=None),
        ft.ElevatedButton("в работу", on_click=None),
        ft.ElevatedButton("Готово", on_click=None)
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    

    task_input.value = ''
    page.update()

    task_input = ft.TextField(label='Введите новую задачу', expand=True)
    add_button = ft.IconButton(icon=ft.Icons.ADD, tooltip='Добавить задачу', on_click=add_task)

    page.add(ft.Row([task_input, add_button]), task_list)

    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)





# Homework 5-6 flet as ft
import sqlite3
from datetime import datetime

# --- Настройка базы данных ---
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_task_to_db(text):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO tasks (text, created_at) VALUES (?, ?)", (text, created_at))
    conn.commit()
    conn.close()

def get_tasks_from_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, created_at FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def main(page: ft.Page):
    page.title = "Список задач"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    init_db()  

    task_input = ft.TextField(label="Введите задачу", expand=True)
    tasks_column = ft.Column()

    def load_tasks():
        tasks_column.controls.clear()
        for task_id, text, created_at in get_tasks_from_db():
            task_row = ft.Row(
                controls=[
                    ft.Text(text, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"📅 {created_at}", size=12, italic=True, color=ft.colors.GREY),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            tasks_column.controls.append(task_row)
        page.update()

    def add_task(e):
        text = task_input.value.strip()
        if text:
            add_task_to_db(text)
            task_input.value = ""
            load_tasks()

    # Кнопка добавления
    add_button = ft.ElevatedButton("Добавить", on_click=add_task)

   
    page.add(
        ft.Row(
            controls=[task_input, add_button],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Divider(),
        ft.Text("Мои задачи:", size=20, weight=ft.FontWeight.BOLD),
        tasks_column,
    )

    load_tasks() 


ft.app(target=main)