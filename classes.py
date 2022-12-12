from collections import UserDict
from datetime import date
import pickle


'''
Класс AddressBook наследуемый от UserDict
в котором хранится словарь с контактами
'''
class AddressBook(UserDict):
    

    def __init__(self, file_path="contact_book"):
        super().__init__()
        self.file_path = f"{file_path}.bin"

    '''
    Метод класа который записывает 
    все данные которые вводит пользователь 
    '''
    def add_record(self, name):
        self.data[name] = Record(name)

    '''
    Метод класа который возвращает генератор по записям
    реализуется для постраничного вывода списка контактов
    '''
    def iterator(self, count):

        page = []
        i = 0

        for record in self.data.values():

            page.append(record)
            i += 1

            if i == count:

                yield page
                page = []
                i = 0

        if page:
            yield page

    '''
    Метод класса для сохранения книги контактов
    '''
    def save_to_file(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.data, file)
        return f"Contact book has save {self.file_path}"

    '''
    Метод класса для загрузки книги контактов
    '''
    def load_from_file(self):
        with open(self.file_path, "rb") as file:
            self.data = pickle.load(file)
        return f"Contact book loaded{self.file_path}"

    '''
    Метод класса для поиска значений в книге контактов
    '''
    def search_in_contact_book(self, search):
        result = []
        for key, record in self.data.items():
            if search in key:
                result.append(f"{search} find in contact {key}.")
            for numbers in record.phones:
                if search in numbers.value:
                    result.append(f"{search} find in number {numbers.value} contact {key}.")
        return result


'''
Класс Record, который отвечает за логику 
добавления/удаления/редактирования 
необязательных полей и хранения обязательного поля Name.
'''
class Record:

    def __init__(self, name, phone=None, birthday=None):

        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else None

    '''
    Метод отвечающий за удаление 
    необязательных значений
    '''
    def delete_phone(self, number):

        for values in self.phones:

            if values.value == number:

                self.phones.remove(values)
                return f"Phone number {number} delete for contact {self.name.value}."
        
        else:
            return f"Don't find {number} in contact {self.name.value}"

    '''
    Метод отвечающий за изменение 
    необязательных значений
    '''
    def edit_phone(self, old_number, new_number):

        for values in self.phones:

            if values.value == old_number:

                values.value = new_number
                return f"Phone number {old_number} has change {new_number} in contact {self.name.value}."
        
        else:
            return f"Don't find {old_number} in contact {self.name.value}"
    
    '''
    Метод отвечающий за добавление необязательных 
    значений типа номер телефона
    '''
    def add_phone(self, number):

        self.phones.append(Phone(number))
        return f"Phone number {number} add in contact {self.name.value}."
    
    '''
    Метод отвечающий за добавление необязательных 
    значений типа дата рождения,
    ожидается что ввод будет гггг.мм.дд
    '''    
    def set_birthday(self, birthdays_data):

        self.birthday = Birthday(birthdays_data)
        return f"Date birthday add {self.birthday.value} to contact {self.name.value}."

    '''
    Метод отвечающий за вычисление колличества 
    дней до дня рождения
    '''  
    def days_to_birthday(self):

        today = date.today()
        future_birthday = date(year=today.year, month=self.birthday.value.month, day=self.birthday.value.day)
        result = (future_birthday - today).days
        if result > 0:
            return result
        else:
            future_birthday = date(year=today.year+1, month=self.birthday.value.month, day=self.birthday.value.day)
            result = (future_birthday - today).days
            return result


'''
Класс Field, логика для атрибутов value 
классов наследников
'''
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


'''
Класс Name наследуется из класса Field, на будущее
'''
class Name(Field):
    pass


'''
Класс Phone наследуется из класса Field, 
в котором происходит проверка
на корректность ввода номера телефона
'''
class Phone(Field):

    @Field.value.setter
    def value(self, value):

        if not value.isdigit():
            raise ValueError("Phone number is not value. Please enter only numbers.")

        self._value = value


'''
Класс Birthday наследуется из класса Field
реализует проверку введенной даты рождения контакта
'''
class Birthday(Field):

    @Field.value.setter
    def value(self, new_value: str):

        try:
            new_value = [int(i) for i in new_value.split(".")]
            birthday_date = date(*new_value)

        except ValueError:
            raise ValueError("Data in not value. Enter numbers in format yyyy.mm.dd.")

        except TypeError:
            raise ValueError("Data in not value. Enter numbers in format yyyy.mm.dd.")

        if birthday_date <= date.today():
            self._value = birthday_date

        else:
            raise ValueError("Date is not value. Date in a future")