from datetime import datetime
from prettytable import PrettyTable
from cl_contract import Contract
from config import db_name, host, user, password
from peewee import PostgresqlDatabase, Model, CharField, DateTimeField, ForeignKeyField

db = PostgresqlDatabase(database=db_name, host=host, port=5432, user=user, password=password)


class Project(Model):
    error_messages = {
        "invalid_project_number": "Введён неверный номер проекта!\n",
        "no_active_contracts": "Отсутствуют активные договора!"
                               "Для создание проекта нужен АКТИВНЫЙ договор!\n",
        "project_exists": "Проект с таким названием уже существует!\n",
    }
    lst_project_ids = []

    project_name = CharField(unique=True, max_length=100, null=True)
    date_of_creation = DateTimeField(default=datetime.now())
    contract_id = ForeignKeyField(Contract, on_delete='cascade')

    class Meta:
        database = db
        db_table = 'projects'

    @classmethod
    def table_output(cls, field_names, data):
        """Функция, которая формирует таблицу из полученных данных"""

        _table = PrettyTable()
        _table.field_names = field_names

        for _object in data:
            cls.lst_project_ids.append(_object.id)
            _table.add_row([_object.id, _object.project_name])

        return _table

    @classmethod
    def create_a_project(cls):

        """Функция создает проект, с выбором Активного договора, который добавить в проект.
           Также проверка на уникальность имени проекта и существование активных договоров."""

        active_contracts = Contract.select().where(Contract.status == 'Активен', Contract.to_project.is_null())

        if active_contracts:
            project_name = input("Введите название проекта: ")
            project_exists = cls.select().where(cls.project_name == project_name)

            if not project_exists:
                print('\nТаблица Активных договоров:')
                print(Contract.table_output(field_names=['Номер договора', 'Название договора'], data=active_contracts))

                number_active_contract = input("Введите номер договора из таблицы для добавления в проект: ")

                if number_active_contract.isdigit() and int(number_active_contract) in Contract.lst_contract_ids:
                    Contract.lst_contract_ids.clear()
                    cls.create(project_name=project_name, contract_id=int(number_active_contract))
                    contract_update = Contract.update({Contract.to_project: project_name}).where(
                        Contract.id == int(number_active_contract))
                    contract_update.execute()

                    return 'Проект успешно создан!\n'

                else:
                    Contract.lst_contract_ids.clear()
                    return Contract.error_messages["invalid_contract_number"]

            else:
                return cls.error_messages["project_exists"]

        else:
            return cls.error_messages["no_active_contracts"]

    @classmethod
    def add_contract(cls):

        """Функция добавляет активный договор в проект, с выбором проекта в который добавить"""

        projects = cls.select().join(Contract).where(Contract.status == 'Завершен').order_by(cls.id)
        active_contracts = Contract.select().where(
            (Contract.status == 'Активен') & (Contract.to_project.is_null())).order_by(Contract.id)

        if projects and active_contracts:
            print("Таблица проектов: ")
            print(cls.table_output(field_names=["Номер проекта", "Название проекта"], data=projects))

            project_number = input("Введите номер проекта в который добавляем договор: ")

            if project_number.isdigit() and int(project_number) in cls.lst_project_ids:
                cls.lst_project_ids.clear()
                project_number_exists = cls.get_or_none(cls.id == int(project_number))

                print(f'\nВы выбрали проект: {project_number_exists.project_name} '
                      f'с завершенным в нем договором: {project_number_exists.contract_id.contract_name}.\n')
                print('Таблица договоров: ')
                print(Contract.table_output(field_names=['Номер договора', 'Название договора'], data=active_contracts))

                contract_number = input("Введите номер договора для добавления в проект: ")

                if contract_number.isdigit() and int(contract_number) in Contract.lst_contract_ids:
                    Contract.lst_contract_ids.clear()
                    contract_number_exists = Contract.get_or_none(Contract.id == int(contract_number),
                                                                  Contract.status == 'Активен',
                                                                  Contract.to_project.is_null())

                    project_number_exists.contract_id = int(contract_number)
                    contract_number_exists.to_project = project_number_exists.project_name

                    project_number_exists.save()
                    contract_number_exists.save()

                    return 'Проект успешно обновлен!\n'

                else:
                    Contract.lst_contract_ids.clear()
                    return Contract.error_messages["invalid_contract_number"]

            else:
                cls.lst_project_ids.clear()
                return cls.error_messages["invalid_project_number"]

        elif not projects:
            return "Нет проектов с завершенными договорами.\n"

        else:
            return "Нет активных договоров без проекта.\n"

    @classmethod
    def completion_contract(cls):

        """Функция завершает договор с выбранным пользователем проектом"""

        projects = cls.select().join(Contract).where(Contract.status == 'Активен').order_by(cls.id)

        if projects:
            print(cls.table_output(field_names=["Номер", "Название проекта"], data=projects))

            project_number = input("Введите номер проекта в котором завершаем договор: ")

            if project_number.isdigit() and int(project_number) in cls.lst_project_ids:
                cls.lst_project_ids.clear()
                project_number_exists = cls.get_or_none(cls.id == int(project_number))

                print(
                    f'\nВы выбрали проект: {project_number_exists.project_name} '
                    f'с действующим в нем договором: {project_number_exists.contract_id.contract_name}.')

                renew_contract = Contract.update({Contract.status: 'Завершен'}).where(
                    Contract.id == project_number_exists.contract_id,
                    Contract.to_project == project_number_exists.project_name)
                renew_contract.execute()

                return "Договор в выбранном проекте завершен!\n"

            else:
                cls.lst_project_ids.clear()
                return cls.error_messages["invalid_project_number"]

        else:
            return "Нет проектов.\n"

    @classmethod
    def all_projects(cls):
        """Функция возвращает таблицу со всеми существующими проектами"""

        projects = cls.select().order_by(cls.id)
        if projects:
            print('Таблица проектов:')
            return cls.table_output(field_names=['Номер проекта', 'Название проекта'], data=projects)
        else:
            return 'Нет проектов.\n'


db.close()
