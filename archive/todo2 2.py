from datetime import date
from enum import Enum
from uuid import uuid4

class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class Item():
    __creation_date = date.today()
    __title = "empty"
    __status = Status.NOT_STARTED
    __priority = Priority.LOW
    __flag = False
    __url = ""
    __due_date = date
    __state = False
    __notes = ""
    __icon = ""

    def __init__(self, title:str=None):
        if title is not None:
            self.__title = title
        self.__id = str(uuid4())

    @property
    def title(self)->str:
        """ Returns the Title of the item """
        return self.__title 
    
    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        self.__priority = value

    @property
    def creation_date(self):
        return self.__creation_date

    @creation_date.setter
    def creation_date(self, value):
        self.__creation_date = value
    
    @property
    def age(self):
        return self.__creation_date - date.today()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def id(self):
        return self.__id
    
    @property
    def flag(self):
        return self.__flag

    @flag.setter
    def flag(self, value:bool):
        self.__flag = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value:str):
        self.__url = value
    
    @property
    def due_date(self):
        return self.__due_date

    @due_date.setter
    def due_date(self, value:date):
        self.__due_date = value
    
    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, value:str):
        self.__icon = value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value:bool):
        self.__state = value

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, value:str):
        self.__value = value

class Todo():
    __todos = []

    def __init__(self):
        print("new todo list created")
        self._current = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < len(self.__todos) -1:
            self._current += 1
            print(self.__todos[self._current].title)
            return self.__todos[self._current]
        else:
            self._current = -1
        raise StopIteration

    def __len__(self):
        return len(self.__todos)

    def new_item(self, item:Item):
        self.__todos.append(item)

    @property
    def items(self)->list:
        return self.__todos

    def show(self):
        print("*"*80)
        for item in self.__todos:
            print(item.title, item.status, item.priority, item.age)

    def remove_item(self, uuid:str=None, title:str=None)->bool:
        if title is None and uuid is None:
            print("You need to provide some details for me to remove it, either UUID or title")
        if uuid is None and title:
            for item in self.__todos:
                if item.title == title:
                    self.__todos.remove(item)
                    return True
            print("Item with title", title, 'not found')
            return False
        if uuid:
            self.__todos.remove(uuid)
            return True

i = Item("Get Shopping")
l = Todo()
l.new_item(i)
l.show()
l.remove_item(title="Get Shopping")
l.show()