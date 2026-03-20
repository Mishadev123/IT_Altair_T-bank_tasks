import os

FILENAME = "my_library.txt"
SEP = ","


class Book:
    def __init__(self, title, author, genre, year, desc):
        self.title = title.strip()
        self.author = author.strip()
        self.genre = genre.strip()
        self.year = year.strip()
        self.desc = desc.strip()
        self.read = False
        self.fav = False


class Library:
    def __init__(self):
        self.books = []
        self.load()

    def load(self):
        if not os.path.exists(FILENAME):
            return

        try:
            with open(FILENAME, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = [p.strip() for p in line.split(SEP)]
                    if len(parts) < 5:
                        continue

                    title, author, genre, year, desc = parts[:5]
                    book = Book(title, author, genre, year, desc)

                    if len(parts) >= 6:
                        val = parts[5].lower()
                        book.read = val in ("да", "прочитано", "yes", "true", "1", "п")
                    if len(parts) >= 7:
                        val = parts[6].lower()
                        book.fav = val in ("да", "в избранном", "yes", "true", "1")

                    self.books.append(book)
        except Exception as e:
            print("Ошибка загрузки:", e)

    def save(self):
        try:
            with open(FILENAME, "w", encoding="utf-8") as f:
                for b in self.books:
                    read_str = "да" if b.read else "нет"
                    fav_str = "да" if b.fav else "нет"
                    safe_title  = b.title.replace(SEP, " ")
                    safe_author = b.author.replace(SEP, " ")
                    safe_genre  = b.genre.replace(SEP, " ")
                    safe_desc   = b.desc.replace(SEP, " ")

                    line = SEP.join([
                        safe_title,
                        safe_author,
                        safe_genre,
                        b.year,
                        safe_desc,
                        read_str,
                        fav_str
                    ])
                    f.write(line + "\n")
        except Exception as e:
            print("Ошибка сохранения:", e)

    def add_book(self):
        print("\nДобавление книги")
        title  = input("Название          : ").strip()
        author = input("Автор             : ").strip()
        genre  = input("Жанр              : ").strip()
        year   = input("Год               : ").strip()
        desc   = input("Краткое описание  : ").strip()

        book = Book(title, author, genre, year, desc)
        self.books.append(book)
        self.save()
        print("Книга добавлена\n")
        input("Enter...")

    def show_all(self):
        print("\n=== Просмотр библиотеки ===")
        print("1 — весь список")
        print("2 — сортировка по названию")
        print("3 — сортировка по автору")
        print("4 — сортировка по году")
        print("5 — сортировка по жанру")
        print("6 — вывод прочитанные")
        print("7 — вывод непрочитанные")
        print("0 — назад")

        choice = input("\nВыбор → ").strip()

        if choice == "0":
            return

        temp = self.books[:]

        if choice == "2":
            temp.sort(key=lambda x: x.title.lower())
        elif choice == "3":
            temp.sort(key=lambda x: x.author.lower())
        elif choice == "4":
            def safe_year(b):
                try: return int(b.year)
                except: return 9999
            temp.sort(key=safe_year)
        elif choice == "5":
            g = input("Жанр → ").strip().lower()
            if g:
                temp = [b for b in temp if b.genre.lower() == g]
        elif choice == "6":
            temp = [b for b in temp if b.read]
        elif choice == "7":
            temp = [b for b in temp if not b.read]

        if not temp:
            print("Нет книг по условиям")
        else:
            print()
            for i, b in enumerate(temp, 1):
                status = "прочитано" if b.read else "не прочитано"
                fav = "да" if b.fav else "нет"
                print(f"{i:2}. {b.title}, {b.author}, {b.genre}, {b.year}, {status}, {fav}")

        input("\nEnter...")

    def change_status(self):
        print("\n=== Смена статуса прочитано / не прочитано ===")

        if not self.books:
            print("Книг пока нет")
            input("\nEnter...")
            return

        print()
        for i, b in enumerate(self.books, 1):
            status = "прочитано" if b.read else "не прочитано"
            fav = "да" if b.fav else "нет"
            print(f"{i:2}. {b.title}, {b.author}, {b.genre}, {b.year}, {status}, {fav}")

        try:
            n = input("\nНомер книги → ").strip()
            idx = int(n) - 1
            if 0 <= idx < len(self.books):
                b = self.books[idx]
                b.read = not b.read
                self.save()
                print(f"Статус изменён → {'прочитано' if b.read else 'не прочитано'}")
            else:
                print("Неверный номер")
        except ValueError:
            print("Нужно ввести число")

        input("\nEnter...")

    def add_fav(self):
        print("\n=== Добавить в избранное ===")

        if not self.books:
            print("Книг пока нет")
            input("\nEnter...")
            return

        print()
        for i, b in enumerate(self.books, 1):
            status = "прочитано" if b.read else "не прочитано"
            fav = "да" if b.fav else "нет"
            print(f"{i:2}. {b.title}, {b.author}, {b.genre}, {b.year}, {status}, {fav}")

        try:
            n = input("\nНомер книги → ").strip()
            idx = int(n) - 1
            if 0 <= idx < len(self.books):
                self.books[idx].fav = True
                self.save()
                print("Добавлено в избранное")
            else:
                print("Неверный номер")
        except ValueError:
            print("Нужно число")

        input("\nEnter...")

    def remove_fav(self):
        print("\n=== Убрать из избранного ===")

        favs = [b for b in self.books if b.fav]
        if not favs:
            print("В избранном ничего нет")
            input("\nEnter...")
            return

        print()
        for i, b in enumerate(favs, 1):
            status = "прочитано" if b.read else "не прочитано"
            print(f"{i:2}. {b.title}, {b.author}, {b.genre}, {b.year}, {status}, да")

        try:
            n = input("\nНомер книги из списка выше → ").strip()
            idx = int(n) - 1
            if 0 <= idx < len(favs):
                favs[idx].fav = False
                self.save()
                print("Убрано из избранного")
            else:
                print("Неверный номер")
        except ValueError:
            print("Нужно число")

        input("\nEnter...")

    def delete_book(self):
        print("\n=== Удаление книги ===")

        if not self.books:
            print("Книг пока нет")
            input("\nEnter...")
            return

        print()
        for i, b in enumerate(self.books, 1):
            status = "прочитано" if b.read else "не прочитано"
            fav = "да" if b.fav else "нет"
            print(f"{i:2}. {b.title}, {b.author}, {b.genre}, {b.year}, {status}, {fav}")

        try:
            n = input("\nНомер книги → ").strip()
            idx = int(n) - 1
            if 0 <= idx < len(self.books):
                removed = self.books.pop(idx)
                self.save()
                print(f"Удалена книга: {removed.title}")
            else:
                print("Неверный номер")
        except ValueError:
            print("Нужно число")

        input("\nEnter...")


def main():
    lib = Library()

    while True:
        print("\n" + "═" * 40)
        print("          T - Б И Б Л И О Т Е К А          ")
        print("═" * 40)
        print(" 1  Добавить книгу")
        print(" 2  Просмотр (сортировка / фильтры)")
        print(" 3  Показать избранное")
        print(" 4  Поменять статус прочитано")
        print(" 5  Добавить в избранное")
        print(" 6  Убрать из избранного")
        print(" 7  Удалить книгу")
        print(" 0  Выход")
        print("═" * 40)

        cmd = input("→ ").strip()

        if   cmd == "1": lib.add_book()
        elif cmd == "2": lib.show_all()
        elif cmd == "3": lib.show_fav()
        elif cmd == "4": lib.change_status()
        elif cmd == "5": lib.add_fav()
        elif cmd == "6": lib.remove_fav()
        elif cmd == "7": lib.delete_book()
        elif cmd in ("0", "выход", "q"):
            print("\nДо свидания!\n")
            break
        else:
            print("Такого пункта нет")
            input("\nEnter...")


def show_fav(self):
    favs = [b for b in self.books if b.fav]
    if not favs:
        print("\nИзбранного пока нет")
        input("\nEnter...")
        return

    print("\nИзбранные книги:")
    print()
    for i, b in enumerate(favs, 1):
        status = "прочитано" if b.read else "не прочитано"
        print(f"{i:2}. {b.title}, {b.author}, {b.genre}, {b.year}, {status}, да")

    input("\nEnter...")


Library.show_fav = show_fav

if __name__ == "__main__":
    main()