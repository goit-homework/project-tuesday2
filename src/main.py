from .models.address_book import AddressBook
from .models.notebook import NoteBook
from .models.record import Record
from .models.note import Note
from .utils.storage import save_data, load_data
from .utils.suggest import suggest_command


def command(name, *, description, usage=None, min_args=0):
    """Decorator to register a command handler with error handling and args validation."""
    def decorator(func):
        def wrapper(self, args):
            if len(args) < min_args:
                return f"Usage: {usage or name}"
            try:
                return func(self, args)
            except (ValueError, KeyError, IndexError) as e:
                return f"Error: {e}"
        wrapper._is_command = True
        wrapper._command_name = name
        wrapper._description = description
        wrapper._usage = usage or name
        return wrapper
    return decorator


class Command:
    """Represents a bot command with handler and description."""

    def __init__(self, handler, description, usage):
        self.handler = handler
        self.description = description
        self.usage = usage


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
                self.commands[cmd_name] = Command(attr, attr._description, attr._usage)

    def parse_input(self, user_input):
        """Parse user input into command and arguments."""
        parts = user_input.split()
        if not parts:
            return "", []
        return parts[0].strip().lower(), parts[1:]

    # Contact commands
    @command("add", description="Add contact with name and phone", usage="add <name> <phone>", min_args=2)
    def add_contact(self, args):
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

    @command("change", description="Change phone number for contact", usage="change <name> <old_phone> <new_phone>", min_args=3)
    def change_contact(self, args):
        name, old, new = args[0], args[1], args[2]
        record = self.book.find(name)
        if not record:
            return f"Contact {name} not found."
        record.edit_phone(old, new)
        return "Contact updated."

    @command("phone", description="Show contact phones", usage="phone <name>", min_args=1)
    def show_contact(self, args):
        record = self.book.find(args[0])
        return str(record) if record else "Contact not found."

    @command("all", description="Show all contacts")
    def show_all_contacts(self, args):
        if not self.book.data:
            return "No contacts saved."
        return "\n".join(f"{i}. {r}" for i, r in enumerate(self.book.data.values(), 1))

    @command("add-birthday", description="Add birthday to contact", usage="add-birthday <name> <DD.MM.YYYY>", min_args=2)
    def add_birthday(self, args):
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.add_birthday(args[1])
        return "Birthday added."

    @command("show-birthday", description="Show contact birthday", usage="show-birthday <name>", min_args=1)
    def show_birthday(self, args):
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        return str(record.birthday) if record.birthday else "Birthday not set."

    @command("birthdays", description="Show upcoming birthdays", usage="birthdays [days]")
    def upcoming_birthdays(self, args):
        days = int(args[0]) if args else 7
        result = self.book.get_upcoming_birthdays(days)
        return str(result) if result else f"No birthdays in the next {days} days."

    @command("add-email", description="Add email to contact", usage="add-email <name> <email>", min_args=2)
    def add_email(self, args):
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.add_email(args[1])
        return "Email added."

    @command("edit-email", description="Edit contact email", usage="edit-email <name> <email>", min_args=2)
    def edit_email(self, args):
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.edit_email(args[1])
        return "Email updated."

    @command("add-address", description="Add address to contact", usage="add-address <name> <address>", min_args=2)
    def add_address(self, args):
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.add_address(" ".join(args[1:]))
        return "Address added."

    @command("edit-address", description="Edit contact address", usage="edit-address <name> <address>", min_args=2)
    def edit_address(self, args):
        record = self.book.find(args[0])
        if not record:
            return "Contact not found."
        record.edit_address(" ".join(args[1:]))
        return "Address updated."

    @command("search", description="Search contacts by query", usage="search <query>", min_args=1)
    def search_contacts(self, args):
        results = self.book.search(" ".join(args))
        return "\n".join(str(r) for r in results) if results else "No contacts found."

    @command("delete", description="Delete contact", usage="delete <name>", min_args=1)
    def delete_contact(self, args):
        self.book.delete(args[0])
        return f"Contact {args[0]} deleted."

    # Note commands
    @command("add-note", description="Add new note", usage="add-note <title>", min_args=1)
    def add_note(self, args):
        title = " ".join(args)
        body = input("Enter note body: ")
        note = Note(title, body)
        self.notebook.add_note(note)
        return f"Note '{title}' added."

    @command("show-notes", description="Show all notes")
    def show_all_notes(self, args):
        if not self.notebook.data:
            return "No notes saved."
        return "\n".join(str(n) for n in self.notebook.data.values())

    @command("find-note", description="Find note by query", usage="find-note <query>", min_args=1)
    def find_note(self, args):
        results = self.notebook.search(" ".join(args))
        return "\n".join(str(n) for n in results) if results else "No notes found."

    @command("edit-note", description="Edit note by ID", usage="edit-note <id>", min_args=1)
    def edit_note(self, args):
        note_id = int(args[0])
        note = self.notebook.find_by_id(note_id)
        if not note:
            return "Note not found."
        title = input("New title (empty to keep): ")
        body = input("New body (empty to keep): ")
        self.notebook.edit_note(note_id, title or None, body or None)
        return "Note updated."

    @command("delete-note", description="Delete note by ID", usage="delete-note <id>", min_args=1)
    def delete_note(self, args):
        self.notebook.delete(int(args[0]))
        return "Note deleted."

    @command("add-tag", description="Add tag to note", usage="add-tag <note_id> <tag>", min_args=2)
    def add_tag(self, args):
        note = self.notebook.find_by_id(int(args[0]))
        if not note:
            return "Note not found."
        note.add_tag(args[1])
        return "Tag added."

    @command("remove-tag", description="Remove tag from note", usage="remove-tag <note_id> <tag>", min_args=2)
    def remove_tag(self, args):
        note = self.notebook.find_by_id(int(args[0]))
        if not note:
            return "Note not found."
        note.remove_tag(args[1])
        return "Tag removed."

    @command("find-by-tag", description="Find notes by tag", usage="find-by-tag <tag>", min_args=1)
    def find_by_tag(self, args):
        results = self.notebook.find_by_tag(args[0])
        return "\n".join(str(n) for n in results) if results else "No notes with this tag."

    @command("sort-by-tag", description="Sort notes by tags")
    def sort_by_tags(self, args):
        result = self.notebook.sort_by_tags()
        if not result:
            return "No notes saved."
        lines = []
        for tag, notes in result.items():
            lines.append(f"[{tag}]")
            for note in notes:
                lines.append(f"  {note}")
        return "\n".join(lines)

    @command("hello", description="Greet the bot")
    def hello(self, args):
        return "How can I help you?"

    @command("help", description="Show available commands")
    def show_help(self, args):
        lines = ["\nAvailable commands:", "-" * 70]
        for cmd_name, cmd in sorted(self.commands.items()):
            lines.append(f"  {cmd.usage:<40} - {cmd.description}")
        lines.append(f"  {'close / exit':<40} - Exit and save")
        lines.append("-" * 70)
        return "\n".join(lines)

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
            elif command in self.commands:
                result = self.commands[command].handler(args)
                if result:
                    print(result)
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
