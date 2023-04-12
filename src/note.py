import abc


class BaseNoteFactory(abc.ABC):

    @abc.abstractmethod
    def create_note(self) -> str:
        pass


class CLINoteFactory(BaseNoteFactory):

    def create_note(self) -> str:
        note = []
        print()
        line = input("Note: ")
        while line:
            note.append(line)
            line = input()
        return '\n'.join(note)
