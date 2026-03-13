from __future__ import annotations
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        cleaned = self._normalize(value)
        if not self._is_valid(cleaned):
            raise ValueError(
                "Invalid phone format. Use 10 to 15 digits, optionally starting with '+'."
            )
        super().__init__(cleaned)

    @staticmethod
    def _normalize(value: str) -> str:
        return (
            value.strip()
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

    @staticmethod
    def _is_valid(value: str) -> bool:
        if value.startswith("+"):
            digits = value[1:]
            return digits.isdigit() and 10 <= len(digits) <= 15
        return value.isdigit() and 10 <= len(value) <= 15


class Email(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not self._is_valid(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    @staticmethod
    def _is_valid(value: str) -> bool:
        if "@" not in value or value.count("@") != 1:
            return False
        local, domain = value.split("@")
        if not local or not domain:
            return False
        if "." not in domain:
            return False
        if domain.startswith(".") or domain.endswith("."):
            return False
        return True


class Address(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            birthday_date = datetime.strptime(value.strip(), "%d.%m.%Y").date()
        except ValueError as exc:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.") from exc
        super().__init__(birthday_date)

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


