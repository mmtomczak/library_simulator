from system import LibrarySystem


library = LibrarySystem()
library.add_book('Catcher in the rye', 'Some guy', "AV387921873")
library.add_book('Catcher in the rye', 'Some guy', "AV387921873")
library.add_book('Catcher in the rye', 'Some guy', "AV387921873")
library.add_worker("Steve", 'librarian')
library.add_customer("Mike")

print(library.books)

library.try_rent_book(library.customers[0], 2200)
print(library.customers[0].rented_books[0].return_date)
print(library.customers[0].rented_books[0].current_renter.name)
library.return_book(library.customers[0], 2200)
print(library.customers[0].rented_books)
