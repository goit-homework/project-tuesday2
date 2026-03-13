from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):
    def add_record(self, record): #add new record to address_book
        key = record.name.value.lower()
        self.data[key] = record

    def find(self, name): #get contact data for Name
        key = name.lower()
        return self.data.get(key)

    def delete(self, name): #delete contact data
        key = name.lower()

        if key in self.data:
            del self.data[key]
        else:
            raise ValueError("Contact not found.")

    def search(self, query):
        query = query.lower()
        results = []

        for record in self.data.values():

            if query in record.name.value.lower(): #search by name
                results.append(record)
                continue

            if record not in results and hasattr(record, "phones"):
                for phone in record.phones:
                    if query in str(phone):
                        results.append(record)
                        break

            if record not in results and hasattr(record, "email") and record.email:
                if query in str(record.email).lower():
                    results.append(record)

            if record not in results and hasattr(record, "address") and record.address:
                if query in str(record.address).lower():
                    results.append(record)

        return results

    def get_upcoming_birthdays(self, days=7): #return contacts with birthdays in 7 days
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():

            if not hasattr(record, "birthday") or not record.birthday:
                continue

            birthday = record.birthday.value

            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            delta = (birthday_this_year - today).days

            if 0 <= delta <= days:

                congratulation_day = birthday_this_year

                if congratulation_day.weekday() == 5: #birthday on weekend
                    congratulation_day += timedelta(days=2)

                elif congratulation_day.weekday() == 6: #birthday on weekend
                    congratulation_day += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "birthday": birthday_this_year.strftime("%d.%m.%Y"),
                    "congratulation_date": congratulation_day.strftime("%d.%m.%Y")
                })

        return sorted(upcoming, key=lambda x: x["congratulation_date"])

    def __str__(self): #show all contacts
        if not self.data:
            return "Address book is empty."

        lines = []

        for record in self.data.values():
            lines.append(str(record))

        return "\n".join(lines)
