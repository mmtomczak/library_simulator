import random
from library_sys.system import LibrarySystem
import numpy as np

# List of actions performed in the library_sys
# Change in possible actions requires changes in print_result and print_result_debug methods of Simulation class,
# changes in perform_action method may also be required
ACTIONS = ["rent_book", "return_book", "add_to_queue", "remove_from_queue"]


class Simulation:
    """
    Create object of a Simulation class

    Args:
        db_path (str): path to the database with library data
        debug (bool, optional): create Simulation object in debug mode, defaults to False
        print_messages (bool, optional): print library_sys action messages, defaults to True

    Keyword Args:
        failure_prob (float): sets a probability of skipping an action in iteration, defaults to 0.5
        fast_messages (bool): turn off pauses between next messages, defaults to False
        print_failures (bool): print information if an action in iteration was failed, defaults to False
        long_pause (int): sets a long pause duration in seconds, defaults to 2. Set to 0 when fast_messages is True
        short_pause (int): sets a short pause duration in seconds, defaults to 1.
            Set to 0 when fast_messages is True

    Attributes:
        system (LibrarySystem): library system object that the library_sys is based on
        _db_path (str): path to the database used in LibrarySystem class instance
        books (list): list of books present in the library
        workers (list): list of workers present in the library
        customers (list): list of customers present in the library
        day (int): day of the library_sys, starts at 1, increments by 1 after every iteration
        long_pause (int): length of a long pause in the library_sys, defaults to 2 seconds
        short_pause (int): length of a short pause in the library_sys, defaults to 1 second
    """
    def __init__(self, db_path: str = None, debug: bool = False, print_messages: bool = True, **kwargs):
        self.system = LibrarySystem(database=db_path)
        self._db_path = db_path
        self.books = self.system.books
        self.workers = self.system.workers
        self.customers = self.system.customers
        self.day = 1
        self.debug = debug
        self.print_messages = print_messages
        self.print_failures = kwargs.get("print_failures", False)
        self.failure_prob = kwargs.get("failure_prob", 0.5)
        self.action_probs = kwargs.get("action_probs", [1/len(ACTIONS) for _ in range(len(ACTIONS))])
        if kwargs.get("fast_messages", False):
            self.long_pause = 0
            self.short_pause = 0
        else:
            self.long_pause = kwargs.get("long_pause", 2)
            self.short_pause = kwargs.get("short_pause", 1)

    def run_and_return_messages(self, num_sub_actions: int = 1):
        """
        Runs a simulation and collects response messages for one day with number of provided actions

        Args:
            num_sub_actions (int): Numbers of actions that are to be performed during one day (one iteration)

        Returns:
            List of all messages that were a result of actions performed during one day, includes all break lines for
                actions and day
        """
        results = []
        try:
            # Get iteration break line
            results.append(self.get_iteration_start())
            for _ in range(num_sub_actions):
                # Get action messages
                for action in self.get_action_messages():
                    results.append(action)
                # Get action break line
                results.append(f"{'-' * 104}")

            # Get iteration end message
            results.append(self.get_iteration_end())
            results.append(f"{'*' * 100}\n")

            # Increment library system day value
            self.day += 1
            # Increment library date to match simulation day
            self.system.update_date(1)
        except AttributeError as err:
            # In case of incorrect action selected add simulation stop error message
            results.append(f"\nSimulation stop due to error\n{err}\nRevise possible actions!\n")

        return results

    def get_action_messages(self):
        """
        Returns a list of all messages for sub-actions that were a result of one action in simulation. Determines if
            a sub-action was successful (resulted in a new message added) or unsuccessful (sub-action was skipped due
            to a random choice). Number of sub-actions is determined by the count of library workers - each worker has
            a chance to perform a sub-action, determined by failure_prob attribute, during one action.

        Returns:
            List of messages, does NOT include break lines.
        """
        messages = []
        # Get a number of sub-actions
        num_subactions = len(self.workers)
        for worker in self.workers:
            # Set sub-action complete as False - sub-action is performed
            subaction_complete = False

            if not np.random.choice([0, 1], p=[self.failure_prob, 1 - self.failure_prob]):
                # If failure_prob determined that sub-action is failed set subaction_complete to True
                subaction_complete = True

            while not subaction_complete:
                # Choose random customer for sub-action
                action_customer = random.choice(self.customers)
                # Choose random book for sub-action
                action_book = random.choice(self.books)
                # Choose random library action that will be performed in sub-action
                action = np.random.choice(ACTIONS, p=self.action_probs)
                # Get result and performed action (performed action may differ from possible library actions)
                result, action = self.perform_action(book=action_book,
                                                     customer=action_customer,
                                                     action=action,
                                                     worker=worker)

                if not result and action == "return_book" and type(result) != float:
                    # if result is false check if action was 'return_book' - in this case result may be of a float type
                    # if action was not a 'return_book' and result was not of a float type then the action was failed -
                    # repeat the loop
                    if self.print_failures:
                        print("ACTION FAIL FIRST STEP")
                elif not result and action != "return_book" and type(result) != float:
                    if self.print_failures:
                        print("ACTION FAIL SECOND STEP")
                else:
                    # if sub-action was successful append message
                    messages.append(self.get_result(action=action,
                                                    book=action_book,
                                                    customer=action_customer,
                                                    worker=worker,
                                                    result=result))
                    # indicate sub-action completion
                    subaction_complete = True
        return messages

    def perform_action(self, book, customer, action, worker):
        """
        Performs a selected library system action

        Args:
            book: Book that is a part of a performed action.
            customer: Customer that is a part of a performed action.
            action: Action that is to be performed.
            worker: Worker that is a part of a performed action

        Returns:
            Tuple of bool and string. Bool indicates the status of action - True if successful, False otherwise.
            String indicates action performed.
        """
        # Get action function
        action_func = getattr(self.system, action)

        try:
            # Get action result
            result = action_func(book_id=book.id, customer_id=customer.id, worker_id=worker.id)
        except ValueError:
            # if ValueError was raised then action was failed
            return False, action

        if action == "add_to_queue":
            # if action is to add customer to a book queue check if book is not rented and queue is empty
            if book.current_renter == customer:
                # if both true book is automatically rented to the customer
                return result, "auto_rent"

        if action == "return_book":
            # if book is returned check if it can be automatically rented to the first customer in queue
            auto_rent_result = self.try_auto_rent(book, worker)
            if auto_rent_result:
                # if true return return_rent action
                return result, "return_rent"

        return result, action

    def try_auto_rent(self, book, worker):
        """
        Checks and if possible automatically rents selected book to the first customer in queue

        Args:
            book (Book): Book to be automatically rented
            worker (Worker): Worker that rents the book

        Returns:
            True if book was automatically rented, False otherwise
        """
        if not book.is_rented() and book.queue:
            return self.system.rent_book(customer_id=book.queue[0].id, book_id=book.id, worker_id=worker.id)
        return False

    def get_iteration_start(self):
        """
        Returns a message for iteration start

        Returns:
            string indicating iteration start
        """
        return f"{'>'*28} DAY {self.day} {'<'*28}"

    def get_iteration_end(self):
        """
        Returns a message for iteration end

        Returns:
            string indicating iteration end
        """
        return f"{'-'*41} END OF THE DAY {self.day} {'-'*41}"

    def get_sim_date(self):
        """
            Returns a message for simulation date

            Returns:
                string indicating simulation date
        """
        return f"{'*'*5} {self.system.date.day}/{self.system.date.month}/{self.system.date.year} {'*'*5}"

    @staticmethod
    def get_result(action: str, book, customer, worker, result):
        """
        Return a string message for a performed library action

        Args:
            action (str): Library action that was performed
            book: Book that was used in the performed action
            customer: Customer that was used in the performed action
            worker: Worker that was used in the performed action
            result: Result of action - for 'return_book' and 'return_rent' action result is of a float type,
                bool otherwise

        Returns:
            string corresponding to selected action and result
        """
        if action == "auto_rent":
            # message for automatic book rent
            return "{} {} rented a book titled '{}' to customer named {} because queue was empty".format(
                worker.position, worker.name, book.title, customer.name)
        elif action == "rent_book":
            # message for book rent
            return "{} {} rented a book titled '{}' to customer named {}".format(
                worker.position, worker.name, book.title, customer.name)
        elif action == "return_book":
            if result > 0:
                # message for a book return if overdue fee was paid
                return """{} {} took an overdue return of book titled '{}' from customer named {}
                    (paid fee = {})""".format(
                    worker.position, worker.name, book.title, customer.name, result)
            else:
                # message for a book return if no fee was paid
                return "{} {} took a return of book titled '{}' from customer named {}".format(
                    worker.position, worker.name, book.title, customer.name)
        elif action == "add_to_queue":
            # message for adding customer to a book queue
            return "{} {} added a customer named {} to a queue for a book titled '{}'".format(
                worker.position, worker.name, customer.name, book.title)
        elif action == "remove_from_queue":
            # message for removing a customer form book queue
            return "{} {} removed a customer named {} from a queue for a book titled '{}'".format(
                worker.position, worker.name, customer.name, book.title)

        elif action == "return_rent":
            if result > 0:
                # message for automatic book rent when book is returned and overdue fee is paid
                return """{} {} took an overdue return of book titled '{}' from customer named {},
                    (paid fee = {}) and automatically rented it to: {}""".format(
                    worker.position, worker.name, book.title, customer.name, result, book.current_renter.name)
            else:
                # message for automatic book rent when book is returned and no fee is paid
                return """{} {} took a return of book titled '{}' from customer named {},
                    and automatically rented it to: {}""".format(
                    worker.position, worker.name, book.title, customer.name, book.current_renter.name)

    @staticmethod
    def get_result_debug(action, book, customer, worker, result):
        """
        Return a debug string message for a performed library action

        Args:
            action (str): Library action that was performed
            book: Book that was used in the performed action
            customer: Customer that was used in the performed action
            worker: Worker that was used in the performed action
            result: Result of action - for 'return_book' and 'return_rent' action result is of a float type,
                bool otherwise

        Returns:
            string in debug (simplified) format corresponding to selected action and result
        """
        if action == "auto_rent":
            return "AUTO RENT {} rented {} to {} ".format(worker.id, book.id, customer.id)
        elif action == "rent_book":
            return "RENT {} rented {} to {}".format(worker.id, book.id, customer.id)
        elif action == "return_book":
            if result > 0:
                return "OVERDUE {} took {} from {}, FEE = {}".format(worker.id, book.id, customer.id, result)
            else:
                return "RETURN {} took {} from {}".format(worker.id, book.id, customer.id)
        elif action == "add_to_queue":
            return "ADD QUEUE {} added {} for {}".format(worker.id, book.id, customer.id)
        elif action == "remove_from_queue":
            return "REMOVE QUEUE {} removed {} for {}".format(worker.id, book.id, customer.id)
        elif action == "return_rent":
            if result > 0:
                return "RETURN RENT {} took {} from {} auto rent to {}, FEE = {}".format(worker.id,
                                                                                         book.id,
                                                                                         customer.id,
                                                                                         book.current_renter.id,
                                                                                         result)
            else:
                return "RETURN RENT {} took {} from {} auto rent to {}".format(worker.id, book.id, customer.id,
                                                                               book.current_renter.id)

    def _clear_simulation(self, **kwargs):
        """
        Clears the data in the library_sys and creates new instance of LibrarySimulation class

        Keyword Args:
            db_path (str): Path to the database containing library data, defaults to None
        """
        del self.system
        self.system = LibrarySystem(db_path=kwargs.get("db_path", None))
        self.books = []
        self.workers = []
        self.customers = []

    def generate_simulation(self, **kwargs):
        """
        Generates a new simulation by loading a library data from database. Prints messages according to a result.

        Keyword Args:
             db_path (str): Path to a library data database location
        """
        try:
            self.system.load_database()
            print("\n\tSIMULATION GENERATED\n")
        except AttributeError as err:
            print(f"\n\n\tIncorrect attributes in library system parameters file\n\t"
                  f"Creating library system with no database connection\n\n{err}\n\n")
            self._clear_simulation(db_path=self._db_path)
