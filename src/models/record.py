from .fields import Name, Phone, Birthday, Email, Address


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, new_email):
        if self.email:
            self.email.value = new_email
        else:
            self.email = Email(new_email)

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, new_address):
        if self.address:
            self.address.value = new_address
        else:
            self.address = Address(new_address)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)

        result = f"Name: {self.name.value}"

        if phones:
            result += f", Phones: {phones}"

        if self.birthday:
            result += f", Birthday: {self.birthday.value}"

        if self.email:
            result += f", Email: {self.email.value}"

        if self.address:
            result += f", Address: {self.address.value}"

        return result