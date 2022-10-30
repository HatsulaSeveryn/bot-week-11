from collections import UserDict
from datetime import date
import re


def input_error(message: str = ''):
    """
    Decorator function for handling input errors
    :param message: optional parameter to specify the input error
    """

    def inner(handler):
        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except Exception as error_:
                print(error_, '\n', message)

        return wrapper

    return inner


class Field:

    def __init__(self, value):
        self._value = str(value)

    def __repr__(self):
        return self._value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return self._value == other.value


class Name(Field):

    pass


class Phone(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    @input_error('Wrong phone number format, try: {+}{10-15 digits without spaces or other symbols}')
    def value(self, phone_num):
        if not phone_num:
            pass
        else:
            if re.fullmatch(r'[+]?\d{10,15}', phone_num.strip()):
                self._value = phone_num.strip()
            else:
                raise ValueError


class Birthday(Field):

    def __init__(self, value):
        self._value = str(value)
        self.year_ = int(value.split('.')[0])
        self.month_ = int(value.split('.')[1])
        self.day_ = int(value.split('.')[2])
        super().__init__(self)

    @property
    def value(self):
        return self._value

    @value.setter
    @input_error('Wrong birthday format, try: {yyyy.mm.dd}')
    def value(self, value):
        if not value:
            pass
        else:
            if re.fullmatch(r'\d{4}[.]\d{2}[.]\d{2}', value.strip()):
                self._value = value.strip()
            else:
                raise ValueError


class Record:

    def __init__(self, name, *args):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday('1900.01.01')

    @input_error()
    def add_phone(self, phone, *args):
        print(f'{phone} has been added to the {self.name} record')
        return self.phones.append(Phone(phone))

    @input_error('Phone not found!')
    def delete_phone(self, phone, *args):
        print(f'{phone} has been deleted from the {self.name} record')
        return self.phones.remove(Phone(phone))

    @input_error('Incorrect phone number when trying to update!')
    def change_phone(self, old_phone, new_phone, *args):
        print(f'{old_phone} has been changed to {new_phone} in the {self.name} record')
        self.phones.remove(Phone(old_phone))
        return self.phones.append(Phone(new_phone))

    @input_error()
    def add_birthday(self, birthday, *args):
        print(f'{self.name} birthday has been added')
        self.birthday.value = birthday


    @input_error()
    def days_to_birthday(self, *args):
        if self.birthday:
            today_ = date.today()
            birthday_ = date(today_.year, self.birthday.month_, self.birthday.day_)
            if today_ == birthday_:
                print('Happy birthday!')
            else:
                if birthday_ < today_:
                    birthday_ = birthday_.replace(year=today_.year + 1)
                print(f'Days until birthday: {birthday_ - today_}')

    def __repr__(self):
        return f'{self.name}: phones {self.phones}, birthday {self.birthday}'


class AddressBook(UserDict):

    @input_error()
    def add_record(self, record, *args):
        if record.name._value not in self.data:
            self.data[record.name._value] = record
            print(f'{record} has been added')
        else:
            print(f'User with name {record.name._value} already exist')

    @input_error('Update record: update {name} add/delete/change {phone} {new phone}(optional)')
    def update_record(self, record, option, *phones):
        if record.name._value in self.data:
            match option:
                case 'add':
                    self.data[record.name._value].add_phone(Phone(phones[0]))
                case 'delete':
                    self.data[record.name._value].delete_phone(Phone(phones[0]))
                case 'change':
                    self.data[record.name._value].change_phone(Phone(phones[0]), Phone(phones[1]))
        else:
            print(f"Record with name {record.name} doesn't exist!")
            raise NameError

    @input_error('Unable to delete. Record not found!')
    def delete_record(self, record, *args):
        print(f'Record {record} has been deleted!')
        del self.data[record.name._value]

    @input_error()
    def show_phones(self, name):
        print(self.data[name])

    @input_error()
    def show_all(self):
        print(self.__repr__())

    def iterator(self, count: int):
        i = 0
        while i < count:
            i += 1
            yield list(self.data.items())[i]

    def __repr__(self):
        return self.data


def main():
    book = AddressBook()

    while True:
        user_command = (input('...').lower()).split()
        match user_command[0]:
            case 'add':
                book.add_record(Record(*user_command[1:]))
            case 'update':
                book.update_record(Record(user_command[1]), user_command[2], *user_command[3:])
            case 'delete':
                book.delete_record(Record(*user_command[1:]))
            case 'birthday':
                book[user_command[1]].add_birthday(user_command[2])
            case 'days':
                    book[user_command[1]].days_to_birthday()
            case 'phone':
                book.show_phones(Record(*user_command[1:]))
            case 'show':
                book.show_all()
            case 'close' | 'exit' | 'quit':
                quit()
            case _:
                print('Wrong command!')


if __name__ == '__main__':
    main()

