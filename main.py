from cl_contract import Contract
from db_tables import creating_tables
from cl_project import Project

process = True


def completion():
    """Функция завершает работу программы"""

    global process
    process = False
    return "Работа с программой завершена!"


def all_data():
    """Функция выводит полные списки проектов и договоров"""

    return print(Project.all_projects()), print(Contract.all_contracts())


def main():
    creating_tables()

    while process:

        print("ГЛАВНОЕ МЕНЮ:\n"
              "1) Проект:\n"
              "\t-Создать проект\n"
              "\t-Добавить договор (с выбором проекта, в который добавить)\n"
              "\t-Завершить договор (с выбором проекта и договора для завершения)\n"
              "2) Договор:\n"
              "\t-Создать договор\n"
              "\t-Подтвердить договор\n"
              "\t-Завершить договор\n"
              "3) Списки проектов и договоров\n"
              "4) Завершить работу с программой\n")

        value_user = input("Выберите одну из предложенных категорий (1, 2, 3 или 4): ")

        if value_user == "1":
            working_with_projects = True

            while working_with_projects:
                print("Проект:\n"
                      "\t1) Создать проект\n"
                      "\t2) Добавить договор (с выбором проекта, в который добавить)\n"
                      "\t3) Завершить договор (с выбором проекта и договора для завершения)\n"
                      "\t4) Списки проектов и договоров\n"
                      "\t5) Вернуться в Главное меню\n"
                      "\t6) Завершить работу с программой\n")
                value_project = input("\nВыберите одну из предложенных категорий для проекта: (1, 2, 3, 4, 5 или 6): ")

                if value_project == "1":
                    print(Project.create_a_project())

                elif value_project == "2":
                    print(Project.add_contract())

                elif value_project == "3":
                    print(Project.completion_contract())

                elif value_project == "4":
                    all_data()

                elif value_project == "5":
                    working_with_projects = False

                elif value_project == "6":
                    working_with_projects = False
                    print(completion())

                else:
                    print("\nНеправильно выбрана позиций! Попробуйте ещё раз!\n")

        elif value_user == "2":
            working_with_contracts = True

            while working_with_contracts:

                print("Договор:\n"
                      "\t1) Создать договор\n"
                      "\t2) Подтвердить договор (с выбором договора для подтверждения)\n"
                      "\t3) Завершить договор (с выбором договора для завершения)\n"
                      "\t4) Списки проектов и договоров\n"
                      "\t5) Вернуться в Главное меню\n"
                      "\t6) Завершить работу с программой\n")

                value_contract = input("\nВыберите одну из предложенных категорий для проекта: (1, 2, 3, 4, 5 или 6): ")

                if value_contract == "1":
                    print(Contract.create_contract())

                elif value_contract == "2":
                    print(Contract.confirmation_contract())

                elif value_contract == "3":
                    print(Contract.completion_contract())

                elif value_contract == "4":
                    all_data()

                elif value_contract == "5":
                    working_with_contracts = False

                elif value_contract == "6":
                    working_with_contracts = False
                    print(completion())

                else:
                    print("\nНеправильно выбрана позиций! Попробуйте ещё раз!\n")

        elif value_user == "3":
            all_data()

        elif value_user == "4":
            print(completion())

        else:
            print("\nВыберите одну из предложенных позиций: 1, 2, 3 или 4!\n")


if __name__ == '__main__':
    main()
