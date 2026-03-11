from .models.address_book import AddressBook
from .models.notebook import NoteBook
from .models.record import Record
from .models.note import Note
from .utils.storage import save_data, load_data
from .utils.suggest import suggest_command


def command(name, description):
    """Decorator to register a command handler."""
    def decorator(func):
        func._is_command = True
        func._command_name = name
        func._description = description
        return func
    return decorator


class Command:
    """Represents a bot command with handler and description."""

    def __init__(self, handler, description):
        self.handler = handler
        self.description = description


class AssistantBot:
    """Personal assistant bot for managing contacts and notes."""

    def __init__(self):
        result = load_data()
        self.book, self.notebook = result if result else (AddressBook(), NoteBook())

        # Auto-register commands from decorated methods
        self.commands = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, '_is_command'):
                cmd_name = attr._command_name
                self.commands[cmd_name] = Command(attr, attr._description)

    def parse_input(self, user_input):
        """Parse user input into command and arguments."""
        parts = user_input.split()
        if not parts:
            return "", []
        return parts[0].strip().lower(), parts[1:]

    # Contact commands
    @command("add", "Add contact with name and phone")
    def add_contact(self, args):
        """Add a new contact or add phone to existing contact."""
        if len(args) < 2:
            return "Usage: add <name> <phone>"
        name, phone = args[0], args[1]
        record = self.book.find(name)
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."
        else:
            message = "Phone added to existing contact."
        record.add_phone(phone)
        return message

    @command("change", "Change phone number for contact")
    def change_contact(self, args):
        if len(args) < 3:
            return "Usage: change <name> <old_phone> <new_phone>"
        name, old, new = args[0], args[1], args[2]
        record = self.book.find(name)
        if not record:
            return f"Contact {name} not found."
        record.edit_phone(old, new)
        return "Contact updated."

    @command("phone", "Show contact phones")
    def show_contact(self, args):
        if len(args) < 1:
            return "Usage: phone <name>"
        record = self.book.find(args[0])
        return str(record) if record else "Contact not found."

    @command("all", "Show all contacts")
    def show_all_contacts(self, args):
        if not self.book.data:
            return "No contacts saved."
        return "\n".join(f"{i}. {r}" for i, r in enumerate(self.book.data.values(), 1))

    @command("add-birthday", "Add birthday to contact")
    def add_birthday(self, args):
        if len(args) < 2:
            return "Usage: add-birthday <name> <DD.MM.YYYY>"
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.add_birthday(args[1])
        return "Birthday added."

    @command("show-birthday", "Show contact birthday")
    def show_birthday(self, args):
        if len(args) < 1:
            return "Usage: show-birthday <name>"
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        return str(record.birthday) if record.birthday else "Birthday not set."

    @command("birthdays", "Show upcoming birthdays")
    def upcoming_birthdays(self, args):
        days = int(args[0]) if args else 7
        result = self.book.get_upcoming_birthdays(days)
        return str(result) if result else f"No birthdays in the next {days} days."

    @command("add-email", "Add email to contact")
    def add_email(self, args):
        if len(args) < 2:
            return "Usage: add-email <name> <email>"
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.add_email(args[1])
        return "Email added."

    @command("edit-email", "Edit contact email")
    def edit_email(self, args):
        if len(args) < 2:
            return "Usage: edit-email <name> <email>"
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.edit_email(args[1])
        return "Email updated."

    @command("add-address", "Add address to contact")
    def add_address(self, args):
        if len(args) < 2:
            return "Usage: add-address <name> <address>"
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.add_address(" ".join(args[1:]))
        return "Address added."

    @command("edit-address", "Edit contact address")
    def edit_address(self, args):
        if len(args) < 2:
            return "Usage: edit-address <name> <address>"
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.edit_address(" ".join(args[1:]))
        return "Address updated."

    @command("search", "Search contacts by query")
    def search_contacts(self, args):
        if len(args) < 1:
            return "Usage: search <query>"
        results = self.book.search(" ".join(args))
        return "\n".join(str(r) for r in results) if results else "No contacts found."

    @command("delete", "Delete contact")
    def delete_contact(self, args):
        if len(args) < 1:
            return "Usage: delete <name>"
        self.book.delete(args[0])
        return f"Contact {args[0]} deleted."

    # Note commands
    @command("add-note", "Add new note")
    def add_note(self, args):
        if len(args) < 1:
            return "Usage: add-note <title>"
        title = " ".join(args)
        body = input("Enter note body: ")
        note = Note(title, body)
        self.notebook.add_note(note)
        return f"Note '{title}' added."

    @command("show-notes", "Show all notes")
    def show_all_notes(self, args):
        if not self.notebook.data:
            return "No notes saved."
        return "\n".join(str(n) for n in self.notebook.data.values())

    @command("find-note", "Find note by query")
    def find_note(self, args):
        if len(args) < 1:
            return "Usage: find-note <query>"
        results = self.notebook.search(" ".join(args))
        return "\n".join(str(n) for n in results) if results else "No notes found."

    @command("edit-note", "Edit note by ID")
    def edit_note(self, args):
        if len(args) < 1:
            return "Usage: edit-note <id>"
        note_id = int(args[0])
        note = self.notebook.find_by_id(note_id)
        if not note:
            return "Note not found."
        title = input("New title (empty to keep): ")
        body = input("New body (empty to keep): ")
        self.notebook.edit_note(note_id, title or None, body or None)
        return "Note updated."

    @command("delete-note", "Delete note by ID")
    def delete_note(self, args):
        if len(args) < 1:
            return "Usage: delete-note <id>"
        self.notebook.delete(int(args[0]))
        return "Note deleted."

    @command("add-tag", "Add tag to note")
    def add_tag(self, args):
        if len(args) < 2:
            return "Usage: add-tag <note_id> <tag>"
        note = self.notebook.find_by_id(int(args[0]))
        if not note:
            return "Note not found."
        note.add_tag(args[1])
        return "Tag added."

    @command("remove-tag", "Remove tag from note")
    def remove_tag(self, args):
        if len(args) < 2:
            return "Usage: remove-tag <note_id> <tag>"
        note = self.notebook.find_by_id(int(args[0]))
        if not note:
            return "Note not found."
        note.remove_tag(args[1])
        return "Tag removed."

    @command("find-by-tag", "Find notes by tag")
    def find_by_tag(self, args):
        if len(args) < 1:
            return "Usage: find-by-tag <tag>"
        results = self.notebook.find_by_tag(args[0])
        return "\n".join(str(n) for n in results) if results else "No notes with this tag."

    @command("sort-by-tag", "Sort notes by tags")
    def sort_by_tags(self, args):
        result = self.notebook.sort_by_tags()
        return str(result) if result else "No notes saved."

    def show_help(self):
        """Display available commands with descriptions."""
        print("\nAvailable commands:")
        print("-" * 70)
        for cmd_name, cmd in sorted(self.commands.items()):
            print(f"  {cmd_name:<20} - {cmd.description}")
        print(f"  hello               - Greet the bot")
        print(f"  help                - Show this help")
        print(f"  close / exit        - Exit and save")
        print("-" * 70)

    def run(self):
        """Main loop."""
        print("Welcome to the assistant bot!")
        print("Type 'help' to see available commands.")

        while True:
            user_input = input("\nEnter a command: ").strip()
            if not user_input:
                continue

            command, args = self.parse_input(user_input)

            if command in ("close", "exit"):
                save_data(self.book, self.notebook)
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "help":
                self.show_help()
            elif command in self.commands:
                try:
                    cmd = self.commands[command]
                    result = cmd.handler(args)
                    if result:
                        print(result)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                suggestion = suggest_command(command, list(self.commands.keys()))
                if suggestion:
                    print(f"Unknown command. Did you mean: {suggestion}?")
                else:
                    print("Invalid command. Type 'help' for available commands.")


def main():
    bot = AssistantBot()
    bot.run()


if __name__ == "__main__":
    main()
