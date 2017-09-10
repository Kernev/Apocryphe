"""LarousseSynset provide a good way to interprete Larousse.fr en-fr traductions and to convert them to a real good
database"""


class LarousseSynset:
    def __init__(self):
        self.name = None
        self.gramatical_category = None
        self.meanings = []

    def last_meaning(self):
        if len(self.meanings) is not 0:
            return self.meanings[-1]
        return None

    def add_number(self, new_number):
        new_meaning = Meaning()
        new_meaning.number = new_number
        self.meanings.append(new_meaning)

    def set_traduction(self, new_traduction, new_metadatas):
        try:
            self.last_meaning().traduction = Traduction(new_traduction, Metadata(new_metadatas))
        except AttributeError:  # If last meaning doesn't exist
            raise AttributeError  # TODO: delete this error test line
            # return    TODO: remove commentary after removed precedent line

    def add_example(self, new_example, new_metadatas):
        try:
            self.last_meaning().examples.append(Example(new_example, Metadata(new_metadatas)))
        except AttributeError:  # If last meaning doesn't exist
            raise AttributeError  # TODO: delete this error test line
            # return    TODO: remove commentary after removed precedent line


class Meaning:
    def __init__(self):
        self.number = None
        self.traduction = None
        self.examples = []


class Traduction:
    def __init__(self, new_traduction, new_metadata):
        self.traduction = new_traduction
        self.metadatas = new_metadata


class Example:
    def __init__(self, new_example, new_metadatas):
        self.example = new_example.raw
        self.example_trad = new_example.trad
        self.metadatas = new_metadatas


class Metadata:
    def __init__(self, new_metadatas):
        self.domain = new_metadatas.domain
        self.metalang = new_metadatas.metalang
        self.category = new_metadatas.category
