# Personal Assistant Bot

CLI-бот для управління контактами та нотатками.

## Встановлення

```bash
# Клонувати репозиторій
git clone https://github.com/goit-homework/project-tuesday2.git
cd project-tuesday2

# Встановити як пакет
pip install .
```

Після встановлення бот доступний з будь-якого місця в системі:

```bash
assistant-bot
```

### Альтернативний запуск (без встановлення)

```bash
python -m assistant_bot.main
```

## Команди

### Контакти
| Команда | Опис |
|---------|------|
| `add <name> <phone>` | Додати контакт |
| `change <name> <old_phone> <new_phone>` | Змінити телефон |
| `phone <name>` | Показати контакт |
| `all` | Показати всі контакти |
| `add-birthday <name> <DD.MM.YYYY>` | Додати день народження |
| `show-birthday <name>` | Показати день народження |
| `birthdays [days]` | Дні народження через N днів (за замовч. 7) |
| `add-email <name> <email>` | Додати email |
| `edit-email <name> <email>` | Змінити email |
| `add-address <name> <address>` | Додати адресу |
| `edit-address <name> <address>` | Змінити адресу |
| `search <query>` | Пошук контактів |
| `delete <name>` | Видалити контакт |

### Нотатки
| Команда | Опис |
|---------|------|
| `add-note <title>` | Додати нотатку |
| `show-notes` | Показати всі нотатки |
| `find-note <query>` | Пошук нотаток |
| `edit-note <id>` | Редагувати нотатку |
| `delete-note <id>` | Видалити нотатку |

### Теги
| Команда | Опис |
|---------|------|
| `add-tag <note_id> <tag>` | Додати тег |
| `remove-tag <note_id> <tag>` | Видалити тег |
| `find-by-tag <tag>` | Пошук за тегом |
| `sort-by-tag` | Сортування за тегами |

### Інше
| Команда | Опис |
|---------|------|
| `hello` | Привітання |
| `help` | Список команд |
| `close` / `exit` | Вихід (автозбереження) |

## Валідація

- **Телефон**: 10-15 цифр, може починатися з `+`
- **Email**: формат `user@domain.tld`
- **День народження**: формат `DD.MM.YYYY`

## Збереження даних

Дані зберігаються автоматично при виході (`close`/`exit`) у файл `data.pkl` в поточній директорії.

## Структура проєкту

```
assistant_bot/
  bot.py             — AssistantBot (головний клас, команди)
  main.py            — точка входу
  models/
    fields.py        — Field, Name, Phone, Birthday, Email, Address
    record.py        — Record (контакт)
    address_book.py  — AddressBook (колекція контактів)
    note.py          — Note, Tag
    notebook.py      — NoteBook (колекція нотаток)
  utils/
    decorators.py    — command декоратор (реєстрація, валідація, обробка помилок)
    storage.py       — збереження/завантаження даних (pickle)
    suggest.py       — підказка найближчої команди (difflib)
```
