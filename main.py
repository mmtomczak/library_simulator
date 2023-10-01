from system import LibrarySystem

# TODO Simulation class
# TODO User interface class

# TODO setup tests


library = LibrarySystem()
library.add_book('Catcher in the rye', 'Some guy', "AV387921873")
library.add_book('Catcher in the rye', 'Some guy', "AV387921873")
library.add_book('Catcher in the rye', 'Some guy', "AV387921873")
library.add_worker("Steve", 'librarian')
library.add_customer("Mike")

library.add_to_queue(library.customers[0].id, 2200)
print(library.books[0].queue)
library.remove_from_queue(library.customers[0].id, 2200)
print(library.books[0].queue)

# print(library.customers[0].rented_books)
# print(library.customers[0].rented_books[0].current_renter.name)
# library.return_book(library.customers[0].id, 2200)
# print(library.customers[0].rented_books)
