import json
import os

class Task:
    """Klasa reprezentująca pojedyncze zadanie."""
    def __init__(self, description, is_completed=False):
        self.description = description
        self.is_completed = is_completed

    def mark_completed(self):
        self.is_completed = True

    def to_dictionary(self):
        """Przygotowuje obiekt do zapisu w formacie JSON."""
        return {"description": self.description, "is_completed": self.is_completed}

    @classmethod
    def from_dictionary(cls, data):
        """Odtwarza obiekt zadania z danych JSON."""
        return cls(data["description"], data["is_completed"])

    def __str__(self):
        status = "[X]" if self.is_completed else "[ ]"
        return f"{status} {self.description}"


class ToDoList:
    """Klasa zarządzająca całą listą zadań."""
    def __init__(self, filename="todo_data.json"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, description):
        self.tasks.append(Task(description))
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_tasks()
            return removed
        return None

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_tasks()
            return True
        return False

    def show_tasks(self):
        if not self.tasks:
            print("Brak zadań. Masz wolne!")
        else:
            for idx, task in enumerate(self.tasks):
                print(f"{idx + 1}. {task}")

    def save_tasks(self):
        """Zapisuje zadania do pliku JSON."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dictionary() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def load_tasks(self):
        """Wczytuje zadania z pliku JSON przy starcie programu."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    self.tasks = [Task.from_dictionary(task) for task in data]
                except json.JSONDecodeError:
                    self.tasks = []


def clear_screen():
    """Czyści ekran konsoli dla lepszej czytelności."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Główna pętla programu (interfejs użytkownika)."""
    todo = ToDoList()

    while True:
        clear_screen()
        print("\n=== TWOJA LISTA ZADAŃ ===")
        todo.show_tasks()
        print("=========================")
        print("1. Dodaj nowe zadanie")
        print("2. Oznacz jako zrobione")
        print("3. Usuń zadanie")
        print("4. Wyjdź")
        
        choice = input("\nWybierz opcję (1-4): ")
        
        if choice == '1':
            desc = input("Podaj treść zadania: ")
            if desc.strip():
                todo.add_task(desc)
        elif choice == '2':
            idx = input("Podaj numer zadania do ukończenia: ")
            if idx.isdigit():
                todo.complete_task(int(idx) - 1)
        elif choice == '3':
            idx = input("Podaj numer zadania do usunięcia: ")
            if idx.isdigit():
                todo.remove_task(int(idx) - 1)
        elif choice == '4':
            print("Do widzenia!")
            break
        else:
            input("Nieprawidłowy wybór. Naciśnij Enter, aby spróbować ponownie...")

if __name__ == "__main__":
    main()


# Autor: Marcin Iwanicki
# Wersja: 2.0 - Moja lokalna wersja


