from datetime import datetime
spisoc = []
def spisok():
    if len(spisoc) == 0:
        print('Список пуст')
    else:
        print("Ваши растения:")
        for i, rast in enumerate(spisoc):
            print(f"{i+1}. {rast['name']} | Посадка: {rast['date']} | Полив: каждые {rast['poliv']} дней")
# Функция для вывода нашего списка растений


def dobavlenie():
    name = input('Введите название растения: ').strip().title()
    if not name:
        print("❌ Название не может быть пустым.")
        return

    while True:
        date_str = input('Введите дату посадки (ГГГГ-ММ-ДД): ')
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            break  
        except ValueError:
            print("❌ Неверный формат даты или несуществующая дата. Пример: 2025-04-10")

    while True:
        try:
            poliv = int(input('Введите как часто надо поливать (дней): '))
            if poliv <= 0:
                print("❌ Количество дней должно быть больше 0.")
                continue
            break
        except ValueError:
            print("❌ Введите число! Например: 3")
    rastenie = {
        'name': name,
        'date': date_str,
        'poliv': poliv,
        'last_watered': date
    }
    spisoc.append(rastenie)
    print(f"✅ {name} добавлен!")

# --- запорос добавлять ли еще?---
    again = input("Хотите добавить ещё одно растение? (да/нет): ").lower()
    if again not in ['да', 'д']:
        break
# Функция для добавления растений в список


def proverka_poliva():
    today = datetime.today()
    nuzhno_polivat = False

    for rast in spisoc:
        days_passed = (today - rast['last_watered']).days
        if days_passed >= rast['poliv']:
            print(f"💧 ПОЛЕЙ: {rast['name']} (не поливали {days_passed} дней)")
            nuzhno_polivat = True

    if not nuzhno_polivat:
        print("Всё в порядке — поливать не надо.")

# Функция для проверки полива



def polito():
    if len(spisoc) == 0:
        print('Сначала добавьте растения!')
        return

    print("Какое растение вы полили?")
    for i, rast in enumerate(spisoc):
        print(f"{i+1}. {rast['name']}")
    while True:
        try:
            num = int(input("Введите номер: ")) - 1
            if 0 <= num < len(spisoc):
                spisoc[num]['last_watered'] = datetime.today()
                print(f"✅ {spisoc[num]['name']} отмечено как политое!")
            else:
                print("❌ Нет такого номера")
        except ValueError:
            print("❌ Введите число!")
# Функция для отметки растений как полито

def udalit():
    if len(spisoc) == 0:
        print('Список пуст')
        return

    print("Какое растение удалить?")
    for i, rast in enumerate(spisoc):
        print(f"{i+1}. {rast['name']}")

    while True:
        try:
            num = int(input("Введите номер: ")) - 1
            if 0 <= num < len(spisoc):
                name = spisoc[num]['name']
                del spisoc[num]
                print(f"✅ {name} удалён!")
                break
            else:
                print("❌ Нет такого номера. Попробуйте снова.")
        except ValueError:
            print("❌ Введите число!")

# Функция для удаления растений из списка



def menu():
    while True:
        if spisoc:
            proverka_poliva()
        print('ПРИВЕТ САДОВОД!🌱')
        print('1. Посмотреть список посаженных растений')
        print('2. Добавить в список новое растение')
        print('3. Отметить растение "ПОЛИТО" и обновить таймер')
        print('4. Удалить растение из списка')
        print('5. Выход')

        choice = input('Выберите действие: ')

        if choice == '1':
            spisok()
        elif choice == '2':
            dobavlenie()
        elif choice == '3':
            polito()
        elif choice == '4':
            udalit()
        elif choice == '5':
            print('До свидания 🌱')
            break
        else:
            print('❌ Неверный ввод. Пожалуйста, выберите действие из списка.')


if __name__ == '__main__':
    menu()
