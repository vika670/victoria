
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Константы
DATA_FILE = "books_data.json"

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker — Учет прочитанных книг")
        self.root.geometry("750x600")

        # Загрузка данных
        self.books = self.load_data()

        # Создание интерфейса
        self.create_widgets()
        
        # Заполнение таблицы начальными данными
        self.update_table(self.books)

    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                return []
        return []

    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")

    def create_widgets(self):
        """Создание элементов графического интерфейса"""
        
        # --- Секция добавления книги ---
        add_frame = tk.LabelFrame(self.root, text="Добавить новую книгу", padx=10, pady=10)
        add_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(add_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(add_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        tk.Label(add_frame, text="Автор:").grid(row=0, column=2, sticky="w")
        self.author_entry = tk.Entry(add_frame)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5, sticky="we")

        tk.Label(add_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.genre_entry = tk.Entry(add_frame)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        tk.Label(add_frame, text="Страниц:").grid(row=1, column=2, sticky="w")
        self.pages_entry = tk.Entry(add_frame)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5, sticky="we")

        btn_add = tk.Button(add_frame, text="Добавить книгу", bg="#4CAF50", fg="white", 
                            command=self.add_book)
        btn_add.grid(row=2, column=0, columnspan=4, pady=10, sticky="we")

        # Настройка растяжения колонок в фрейме
        for i in range(4):
            add_frame.grid_columnconfigure(i, weight=1)

        # --- Секция фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(filter_frame, text="Жанр:").pack(side="left", padx=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=15)
        self.filter_genre_entry.pack(side="left", padx=5)

        self.filter_pages_var = tk.BooleanVar()
        tk.Checkbutton(filter_frame, text="Более 200 страниц", 
                       variable=self.filter_pages_var).pack(side="left", padx=10)

        tk.Button(filter_frame, text="Применить фильтр", 
                  command=self.apply_filter).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Сбросить", 
                  command=self.reset_filter).pack(side="left", padx=5)

        # --- Секция таблицы ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Создание таблицы (Treeview)
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")

        self.tree.column("pages", width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)

        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    # --- Логика работы ---

    def add_book(self):
        """Добавление книги с валидацией"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Валидация: Проверка на пустоту
        if not (title and author and genre and pages):
            messagebox.showwarning("Внимание", "Все поля должны быть заполнены!")
            return

        # Валидация: Числовое поле
        if not pages.isdigit():
            messagebox.showwarning("Ошибка", "Количество страниц должно быть целым числом!")
            return

        # Создание объекта книги
        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        # Обновление данных
        self.books.append(new_book)
        self.save_data()
        self.update_table(self.books)
        
        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"Книга '{title}' успешно добавлена!")

    def update_table(self, data_list):
        """Очистка и заполнение таблицы новыми данными"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for book in data_list:
            self.tree.insert("", tk.END, values=(
                book["title"], 
                book["author"], 
                book["genre"], 
                book["pages"]
            ))

    def apply_filter(self):
        """Логика фильтрации списка книг"""
        genre_filter = self.filter_genre_entry.get().lower().strip()
        show_large_only = self.filter_pages_var.get()

        filtered_list = self.books

        # Фильтр по жанру
        if genre_filter:
            filtered_list = [b for b in filtered_list if genre_filter in b["genre"].lower()]

        # Фильтр по количеству страниц (> 200)
        if show_large_only:
            filtered_list = [b for b in filtered_list if b["pages"] > 200]

        self.update_table(filtered_list)

    def reset_filter(self):
        """Сброс всех фильтров"""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_var.set(False)
        self.update_table(self.books)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
