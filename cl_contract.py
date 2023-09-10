from datetime import datetime
from prettytable import PrettyTable
from config import db_name, host, user, password
from peewee import PostgresqlDatabase, Model, CharField, DateTimeField, IntegrityError

db = PostgresqlDatabase(database=db_name, host=host, port=5432, user=user, password=password)


class Contract(Model):
    error_messages = {
        "existing_contract_name": "\nДоговор с таким названием уже существует! Попробуйте ввести другое название!\n",
        "invalid_contract_number": "\nВведен неверный номер договора!\n",
    }

    lst_contract_ids = []

    contract_name = CharField(unique=True, max_length=100, null=True)
    date_of_creation = DateTimeField(default=datetime.now())
    date_of_signing = DateTimeField(default=None)
    status = CharField(default='Черновик', max_length=100)
    to_project = CharField(max_length=100, default=None)

    class Meta:
        database = db
        db_table = 'contracts'

    @classmethod
    def table_output(cls, field_names, data):
        """Функция, которая формирует таблицу из полученных данных"""

        _table = PrettyTable()
        _table.field_names = field_names

        for _object in data:
            cls.lst_contract_ids.append(_object.id)
            _table.add_row([_object.id, _object.contract_name])

        return _table

    @classmethod
    def create_contract(cls):
        """Функция создает договор, если договор с таким название существует, возвращает ошибку"""

        try:
            contract_name = input('Введите название договора: ')
            Contract.create(contract_name=contract_name)
            return 'Договор создан!\n'
        except IntegrityError:
            return cls.error_messages["existing_contract_name"]

    @classmethod
    def confirmation_contract(cls):
        """Функция изменяет статус договора Черновик => Активен (Подтверждает договор),
           также при подтверждении договора проставляется время подтверждения"""

        contracts = cls.select().where(cls.status == 'Черновик').order_by(cls.id)
        if contracts:
            print('Таблица договоров: ')
            print(cls.table_output(field_names=['Номер договора', 'Название договора'], data=contracts))

            number_contract = input('Введите номер договора для подтверждения: ')
            if number_contract.isdigit() and int(number_contract) in cls.lst_contract_ids:
                cls.lst_contract_ids.clear()
                contract_confirmation = cls.get(cls.id == int(number_contract), cls.status == "Черновик")
                contract_confirmation.status = "Активен"
                contract_confirmation.date_of_signing = datetime.now()
                contract_confirmation.save()
                return f'Договор: {contract_confirmation.contract_name} успешно подтвержден!'
            else:
                return cls.error_messages["invalid_contract_number"]
        else:
            return 'Нет договоров для подтверждения.\n'

    @classmethod
    def completion_contract(cls):
        """Функция изменяет статус договора с Активен --> Завершен (Завершает действие договора договор)"""

        contracts = cls.select().where(cls.status != 'Завершен')

        if contracts:
            print('\nТаблица договоров, которые вы можете завершить: ')
            print(cls.table_output(field_names=['Номер договора', 'Название договора'], data=contracts))

            number_contract = input('Введите номер договора для завершения: ')

            if number_contract.isdigit() and int(number_contract) in cls.lst_contract_ids:
                cls.lst_contract_ids.clear()
                contract_confirmation = cls.get(cls.id == number_contract,
                                                (cls.status != 'Завершен'))
                contract_confirmation.status = "Завершен"
                contract_confirmation.save()

                return f'Договор: {contract_confirmation.contract_name} успешно завершен!'

            else:
                return cls.error_messages["invalid_contract_number"]

        else:
            return 'Договоров для завершения нет!\n'

    @classmethod
    def all_contracts(cls):
        """Функция возвращает таблицу со всеми договорами, если они есть"""

        contracts = cls.select().order_by(cls.id)
        if contracts:
            print('Таблица договоров:')
            return cls.table_output(field_names=['Номер договора', 'Название договора'], data=contracts)
        else:
            return 'Нет договоров.'


db.close()
