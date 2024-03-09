from collections import UserDict


# CUSTOM ERRORS


class TheNameError(Exception):
    pass


class PhoneIndexError(Exception):
    pass


class PhoneError(Exception):
    pass


class RecordError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# CLASSES


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name):
        if len(str(name)) < 3:
            raise TheNameError()
        self.__value = name


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if not str(phone).isdecimal():
            raise PhoneError()
        elif len(str(phone)) != 10:
            raise PhoneError()
        else:        
            self.__value = phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def delete_phone(self, phone_number):
        index = self.find_phone(phone_number)
        self.phones.pop(index)

    def edit_phone(self, phone_numbers):
        index = self.find_phone(phone_numbers[0])
        self.phones[index] = Phone(phone_numbers[1])

    def find_phone(self, phone_number):
        index = 0
        for item in self.phones:
            if item.value == phone_number:
                return index
            index += 1
        raise PhoneIndexError()

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        if str(record.name) in self.data.keys():
            raise RecordError()
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data[name]

    def delete(self, name):
        self.data.pop(name)


# INPUT ERRORS HANDLER


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as err:
            if isinstance(err, KeyError):
                return "Record not found."
            elif isinstance(err, TypeError):
                return "Enter record name."
            elif isinstance(err, ValueError):
                return "Enter record name and phone number."
            elif isinstance(err, IndexError):
                return "Enter record name."
        except (TheNameError, PhoneIndexError, PhoneError, RecordError) as custom_err:
            if isinstance(custom_err, TheNameError):
                return "Name must have min. 3 characters."
            elif isinstance(custom_err, PhoneIndexError):
                return "No such phone."
            elif isinstance(custom_err, PhoneError):
                return "Phone must have 10 digits."
            elif isinstance(custom_err, RecordError):
                return "Contact with this name already exists."

    return inner


# FUNCTIONS


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def get_command(input):
    commands = {
        "add": add_record,
        "all": show_all,
        "hello": greeting,
        "phone": find_phone,
        "delete": delete_record,
        "add_phone": add_phone,
        "edit_phone": edit_phone,
        "find": find_record,
    }

    command = commands.get(input)
    if not command:
        return invalid_command
    return command


@input_error
def add_record(book, *args):
    name, *phone_number = args
    record = Record(Name(name))
    if phone_number:
        record.add_phone(phone_number[0])
    book.add_record(record)
    return "Contact added."


@input_error
def add_phone(book, *args):
    name, phone_number = args
    record = book.find(name)
    record.add_phone(phone_number)
    return f"Phone added."


@input_error
def edit_phone(book, *args):
    name, *phone_numbers = args
    record = book.find(name)
    record.edit_phone(phone_numbers)
    return f"Phone updated."


@input_error
def find_record(book, *args):
    name = args[0]
    return book.find(name)


def greeting(*_):
    return "How can I help you?"


def invalid_command(*_):
    return "Invalid command."


@input_error
def delete_record(book, *args):
    name = args[0]
    book.delete(name)
    return f"Record deleted."


@input_error
def find_phone(book, *args):
    name, phone_number = args
    record = book.find(name)
    index = record.find_phone(phone_number)
    return f"{record.name}: {record.phones[index]}."


def show_all(book):
    if len(book):
        result = "All contacts: "
        for _, record in book.items():
            result += f"\n{record}"
        return result
    return "No contacts."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        print(get_command(command)(book, *args))


if __name__ == "__main__":
    main()
