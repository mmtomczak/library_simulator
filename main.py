from Simulation import Simulation
from flask import Flask, url_for, request, render_template, redirect
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap4
from database_generator import DatabaseGenerator

# Create flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET"
# initialize flask bootstrap
bootstrap = Bootstrap4(app)
# create socket for app
socket = SocketIO(app, async_handlers=True)

# create global simulation variable
sim = None


@app.route('/', methods=["POST", "GET"])
def main():
    """
    Renders main page, redirects to simulation when the method is POST

    Returns:
        Renders template on GET, redirects on POST
    """
    if request.method == "POST":
        if request.form.get('data-reset'):
            DatabaseGenerator('database/library.db')
        # redirect to simulation page
        # if POST method is used create new simulation with selected failure_prob
        global sim
        sim = Simulation(db_path='database/library.db',
                         failure_prob=float(request.form['failure-prob']))
        sim.generate_simulation()
        return redirect(url_for('.simulation', sim=sim, bootstrap=bootstrap))
    # render main template
    return render_template("index.html", bootstrap=bootstrap)


@app.route("/tables/<table_name>")
def tables(table_name):
    """
    Renders tables.html template with given data

    Args:
        table_name: name of table that is to be generated

    Returns:
        Renders template
    """
    # get global simulation variables
    global sim
    # get variable with simulation status
    no_sim = True if sim is None else False
    if not no_sim:
        # if simulation is generated
        if table_name == 'queues':
            table = sim.system._cursor.execute(f"""SELECT customers.name, workers.name, workers.position,
            books.book_id, books.title, books.author, books.publisher, books.isbn, books.year_published FROM queues
            JOIN customers ON queues.customer_id = customers.customer_id
            JOIN workers ON queues.worker_id = workers.worker_id
            JOIN books ON queues.book_id = books.book_id ORDER BY customers.name""").fetchall()
            schema = ["Customer name", "Worker name", "Worker position", "Book ID", "Book title",
                      "Book author", "Book publisher", "Book ISBN", "Year of publication"]
        elif table_name == 'rents':
            table = sim.system._cursor.execute(f"""SELECT return_date, customers.name, workers.name,
            workers.position, books.book_id, books.title, books.author, books.publisher, books.isbn, 
            books.year_published FROM rents
            JOIN customers ON rents.customer_id = customers.customer_id
            JOIN workers ON rents.worker_id = workers.worker_id
            JOIN books ON rents.book_id = books.book_id ORDER BY customers.name, return_date""").fetchall()
            schema = ["Return date", "Customer name", "Worker name", "Worker position", "Book ID", "Book title",
                      "Book author", "Book publisher", "Book ISBN", "Year of publication"]
        else:
            table = sim.system._cursor.execute(f"""SELECT * FROM {table_name}""").fetchall()
            if table_name == 'workers':
                schema = ["ID", "Name", "Position"]
            elif table_name == 'customers':
                schema = ["ID", "Name"]
            else:
                schema = ["ID", "Title", "Author", "ISBN", "Publisher", "Year of publication"]
    else:
        # if there is no simulation generated assign None to table and schema variables
        table = None
        schema = None
    return render_template("table.html", table=table, schema=schema, title=table_name,
                           bootstrap=bootstrap, no_sim=no_sim)


@app.route("/sim")
def simulation():
    """Renders simulation page template"""
    return render_template('simulation.html', bootstrap=bootstrap)


@socket.on('message')
def handle_message(iters, actions):
    """
    Handler for incoming socket messages. Emits socket messages containing results of performed actions.

    Args:
        iters: number of iterations in simulation run
        actions: number of action per iteration
    """
    global sim
    if sim is None:
        # if no simulation is generated redirect to main page
        print("No simulation generated!")
        socket.emit('redirect', {'url': url_for('main')})
        # return none to stop function from continuing
        return None
    for _ in range(int(iters)):
        # for every iteration get action messages
        result = sim.run_and_return_messages(num_sub_actions=int(actions))
        for log in result:
            # for every message emit message and pause socket for 1 second
            socket.send(log)
            socket.sleep(1)
    # at the end sent empty message
    socket.send(None)


if __name__ == "__main__":
    socket.run(app, allow_unsafe_werkzeug=True)
