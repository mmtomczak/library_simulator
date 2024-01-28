# Library Simulator
Interactive simulation of working library. Used as a final project for Python and SQL: intro class during my Data Science and Business Analitics studies.

## Project information
The project is build using Python. Flask is used for front-end, and flask-socketio library is used to send simulation messages from back-end to front-end.

In the library customers, with the help of library workers, can rent and return books. If the book that the customer wants to rent is already rented, they can be put in queue for this book. If they change their mind, they can withdraw from the queue. Every action that is performed in the library generates according message that is visible to the user. 

User can control probability of action failure. Action failure means, that the given worker will not perform an action. After setting probability of action failure user can generate simulation. When simulation is generated, number of iterations and sub-iterations can be set. Iterations translate to simulation days, sub-iterations define number of actions that the single worker can perform during one iteration.

For simplicity and to ensure smooth simulation experience some rules were applied. Firstly, every action has the same probability of being chosen. In every sub-iteration, every worker can perform one action. However, for every action a random customer and book is selected. Due to this, some simplifications apply:
- if action is returing book and chosen customer is currently renting at least one book, there is 80% chance that they will return their earliest rented book
- if action is remove from queue and queue for the chosen book is not empty, there is a 70% chance that a random customer will be removed from queue
- if action is add to queue, but the book is currently not rented and the queue is empty, the book will be automatically rented to the customer

User can also view data used and generated in the simulation as well as some statistics regarding it. User can also add data to specific tables in the database. Admin can view registered users and data logs describing data deleted during sumulation as a result of an action. 

## Database schema
Below, you can see image describing the database used in the project:
![Database Schema](https://github.com/mmtomczak/library_simulator/blob/master/static/images/db_schema.png?raw=true)

