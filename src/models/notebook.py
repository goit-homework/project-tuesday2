from collections import UserDict


class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self._next_id = 1

    def add_note(self, note):
        note.id = self._next_id
        self.data[self._next_id] = note
        self._next_id += 1
        return note.id

    def find_by_id(self, note_id):
        return self.data.get(note_id)

    def search(self, query):
        result = []
        query = query.lower()

        for note in self.data.values():
            if query in note.title.lower() or query in note.body.lower():
                result.append(note)

        return result

    def edit_note(self, note_id, new_title=None, new_body=None):
        note = self.data.get(note_id)

        if not note:
            return None

        if new_title:
            note.title = new_title

        if new_body:
            note.body = new_body

        return note

    def delete(self, note_id):
        return self.data.pop(note_id, None)

    def find_by_tag(self, tag):
        result = []

        for note in self.data.values():
            if tag in note.tags:
                result.append(note)

        return result

    def sort_by_tags(self):
        tag_dict = {}

        for note in self.data.values():
            for tag in note.tags:
                tag_dict.setdefault(tag, []).append(note)

        return dict(sorted(tag_dict.items()))