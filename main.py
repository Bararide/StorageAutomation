import asyncio
import sqlite3
import tkinter as tk
from getpass import getpass

from StorageAPI import StorageAPI
from googleSheetTransition import SheetsTransition

SPREADSHEET_URL = None

async def register_user():
    username = username_entry.get()
    password = password_entry.get()
    path = path_entry.get()
    spreadsheet_url = spreadsheet_entry.get().strip()
    column_to_read = column_read_entry.get()
    column_to_modify = column_modify_entry.get()

    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password TEXT, path TEXT, spreadsheet_url TEXT, column_to_read TEXT, column_to_modify TEXT)''')

    c.execute("SELECT username FROM users")
    user = c.fetchone()

    if user:
        c.execute("UPDATE users SET username=?, password=?, path=?, spreadsheet_url=?, column_to_read=?, column_to_modify=?",
                  (username, password, path, spreadsheet_url, column_to_read, column_to_modify))
    else:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                  (username, password, path, spreadsheet_url, column_to_read, column_to_modify))

    conn.commit()
    conn.close()

async def main():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute("SELECT username, password, path, spreadsheet_url, column_to_read, column_to_modify FROM users")
    user = c.fetchone()

    if user:
        try:
            username, password, path, spreadsheet_url, column_to_read, column_to_modify = user
            api = StorageAPI(username, password)
            names = await api.get_product_names()
            names = [name.lower() for name in names]

            transation = SheetsTransition(path, spreadsheet_url)
            transation.column_to_read = column_to_read
            transation.column_to_modify = column_to_modify
            transation.getSheetData()
            transation.CheckSheetData(names)
        except Exception as e:
            status_label.config(text="Возникла ошибка, попробуйте снова")

    conn.close()

def register_button_click():
    loop.run_until_complete(register_user())
    register_button.config(state=tk.NORMAL)
    status_label.config(text="Регистрация прошла успешно!")
    register_button.update()

def start_button_click():
    spreadsheet_url = spreadsheet_entry.get()
    global SPREADSHEET_URL
    SPREADSHEET_URL = spreadsheet_url.strip()

    loop.run_until_complete(main())
    start_button.config(state=tk.NORMAL)
    status_label.config(text="Обновление данных!")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    root = tk.Tk()
    root.title("Автоматизация")
    root.geometry("400x500")

    root.lift()
    root.attributes("-topmost", True)

    username_label = tk.Label(root, text="Имя пользователя в МойСклад:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Пароль от МойСклад:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    path_label = tk.Label(root, text="Путь до файла keys.json:")
    path_label.pack()
    path_entry = tk.Entry(root)
    path_entry.pack()

    spreadsheet_label = tk.Label(root, text="Ссылка на таблицу:")
    spreadsheet_label.pack()
    spreadsheet_entry = tk.Entry(root)
    spreadsheet_entry.pack()

    column_read_label = tk.Label(root, text="Столбец для чтения:")
    column_read_label.pack()
    column_read_entry = tk.Entry(root)
    column_read_entry.pack()

    column_modify_label = tk.Label(root, text="Столбец для изменения:")
    column_modify_label.pack()
    column_modify_entry = tk.Entry(root)
    column_modify_entry.pack()

    register_button = tk.Button(root, text="Регистрация", command=register_button_click)
    register_button.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    start_button = tk.Button(root, text="Старт", command=start_button_click)
    start_button.pack()

    root.mainloop()

    loop.close()