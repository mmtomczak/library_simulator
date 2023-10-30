import warnings
from system import LibrarySystem

BOOK_ATTRS = ['id', 'title', 'author', 'isbn', 'publisher', 'year_published']
WORKER_ATTRS = ['id', 'name', 'position']
CUSTOMER_ATTRS = ['id', 'name']

# TODO: add custom warning functions
# TODO: create output messages class


class Simulation:
    def __init__(self, db_path=None):
        self.system = LibrarySystem(database=db_path)
        self._generated = False
        self.books = self.system.books
        self.workers = self.system.workers
        self.customers = self.system.customers
    
    def query_library_data(self, item_list: str, query, by: str):
        data = []
        try:
            raw_data = getattr(self.system, item_list)
        except AttributeError:
            # TODO: incorrect list selected
            return []

        if not raw_data:
            return []

        for item in raw_data:
            try:
                target = getattr(item, by)
            except AttributeError:
                # TODO: incorrect item attribute
                return []

            if isinstance(query, str):
                target = target.lower()
                query = query.lower()

            if query in target:
                data.append(item)
        return data

    def get_all_attribute_values(self, item_list: str, attr: str):
        data = []
        try:
            raw_data = getattr(self.system, item_list)
        except AttributeError:
            warnings.warn('List {} not found in the library system'.format(item_list), Warning)
            return None

        for item in raw_data:
            try:
                data.append(getattr(item, attr))
            except AttributeError:
                warnings.warn('Attribute {} not found in {} list object'.format(attr, item_list), Warning)
                continue
        return data

    # def add_book(self, **kwargs):
    #     self.system.add_book(title=kwargs['title'], author=kwargs['author'], isbn=kwargs['isbn'],
    #                          publisher=kwargs['publisher'], year_published=kwargs['year_published'])
    #     return "Added book titled '{}' by {} to the library.".format(kwargs['title'], kwargs['author'])
    #
    # def add_worker(self, **kwargs):
    #     self.system.add_worker(name=kwargs['name'], position=kwargs['position'])
    #     return "Added worker named {} at position {} to the library".format(kwargs['name'], kwargs['position'])
    #
    # def add_customer(self, **kwargs):
    #     self.system.add_customer(name=kwargs['name'])
    #     return "Added customer named {} to the library".format(kwargs['name'])
    #
    # def remove_book(self, book_id: int):
    #     self.system.remove_book(book_id=book_id)
    #     return "Removed book with the ID of {} from the library".format(book_id)
    #
    # def remove_worker(self, worker_id: int):
    #     self.system.remove_worker(worker_id=worker_id)
    #     return "Removed worker with the ID of {} from the library".format(worker_id)
    #
    # def remove_customer(self, customer_id: int):
    #     self.system.remove_customer(customer_id=customer_id)
    #     return "Removed customer with the ID of {} from the library".format(customer_id)
    #
    # def add_items(self, item_list: list, target_func: str):
    #     func = getattr(self, target_func)
    #     for item in item_list:
    #         func(**item)

    def _clear_simulation(self):
        del self.system
        self.system = LibrarySystem()
        self.books = []
        self.workers = []
        self.customers = []
        self._generated = False

    def generate_simulation(self):
        if self._generated:
            print(f"\n\n\tSimulation already generated\n\t"
                  f"Do you want to generate clean simulation?(y/n):")
            response = str(input()).lower()
            if response == "y":
                self._clear_simulation()
                print("\n\tGenerating new simulation...\n\n")
            elif response == "n":
                return 0
            else:
                print("\n\tIncorrect input. Generated simulation will not be changed.\n\n")
                return 0

        try:
            self.system.load_database()
        except AttributeError as err:
            print(f"\n\n\tIncorrect attributes in simulation parameters file\n\t"
                  f"Clearing the simulation\n\n{err}\n\n")
            self._clear_simulation()
        self._generated = True
