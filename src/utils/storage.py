import pickle
from pathlib import Path
from ..models.address_book import AddressBook
from ..models.notebook import NoteBook

DATA_FILE = Path.cwd() / "data.pkl"


def save_data(book, notebook):
    with open(DATA_FILE, "wb") as f:
        pickle.dump((book, notebook), f)


def load_data():
    try:
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook(), NoteBook()
