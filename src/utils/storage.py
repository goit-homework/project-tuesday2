import pickle
from pathlib import Path
from ..models.address_book import AddressBook
from ..models.notebook import NoteBook

DATA_DIR = Path.home() / ".assistant"
DATA_FILE = DATA_DIR / "data.pkl"


def save_data(book, notebook):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "wb") as f:
        pickle.dump((book, notebook), f)


def load_data():
    try:
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook(), NoteBook()
