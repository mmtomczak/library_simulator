import sqlite3
from Simulation import Simulation
from flask import Flask, url_for, request, render_template, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap4
from database_generator import DatabaseGenerator
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd

# Create flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET"

# Create and initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
# Initialize flask bootstrap
bootstrap = Bootstrap4(app)
# Create socket for app
socket = SocketIO(app, async_handlers=True)

# Create global simulation variable
sim = None

# Connect to the library database and create cursor
db = sqlite3.connect("database/library.db", check_same_thread=False)
cur = db.cursor()


# Create User class template that will be used to authorize users
class User(UserMixin):
    pass


# Load user by user_id
@login_manager.user_loader
def load_user(user_id):
    # Create User class object
    user = User()
    try:
        # Selects user_id, name and username for user with a given user_id from users table and assigns it as attributes
        # of the User class object
        (user.id, user.name, user.username) = cur.execute(f"""
        SELECT user_id, name, username FROM users WHERE user_id='{user_id}'
        """).fetchone()
    except TypeError:
        # If TypeError occurred no user will be loaded
        user = None
    return user


@app.route('/main', methods=["POST", "GET"])
@login_required
def main():
    """
    Renders main page, redirects to simulation when the method is POST. Requires logged-in user

    Returns:
        Renders template on GET, redirects on POST
    """
    global sim
    status = False if not sim else True
    if request.method == "POST":
        if request.form.get('data-reset'):
            DatabaseGenerator(cur=cur, db=db)
        # redirect to simulation page
        # if POST method is used create new simulation with selected failure_prob
        sim = Simulation(db_cursor=cur,
                         db_con=db,
                         failure_prob=float(request.form['failure-prob']))
        sim.generate_simulation()
        # Redirect to the simulation page
        return redirect(url_for('.simulation', sim=sim, bootstrap=bootstrap))
    # render main template
    return render_template("index.html", bootstrap=bootstrap, user=current_user, status=status)


@app.route("/", methods=["POST", "GET"])
def login_page():
    """
    Renders login page and logs-in users.

    Returns:
        Renders template for login.html if method is "GET", redirects if method is "POST"
    """
    if request.method == "POST":
        # Get username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Selects password and user_idf rom users table for user with given username
        result = cur.execute(f"SELECT password, user_id FROM users WHERE username = '{username}'").fetchone()
        # If username is not found in the database
        if not result:
            # Send flash message
            flash("Username not found!")
            # Redirect to the login page
            return redirect(url_for('login_page'))
        # Else if passwords do not match
        elif not check_password_hash(result[0], password):
            # Send flash message
            flash("Incorrect password!")
            # Redirect to the login page
            return redirect(url_for('login_page'))
        else:
            # Load and login user with given user_id
            user = load_user(result[1])
            login_user(user)
            # Redirect to the main page
            return redirect(url_for('main'))
    # Render login page template
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Renders register page template and registers users

    Returns:
        Renders template for 'register.html' for "GET", redirects to url for 'main' on "POST"
    """
    if request.method == "POST":
        # Get username
        username = request.form.get('username')
        # Select data from users table for given username to check if username already exists
        if cur.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchone():
            # Send flash message
            flash("Username already exists")
            # Redirect to the registration page
            return redirect(url_for('register'))

        if request.form.get('password') != request.form.get('password_confirm'):
            flash("Passwords do not match")
            return redirect(url_for('register'))

        # Hash and salt password
        hash_password = generate_password_hash(request.form.get('password'),
                                               method='pbkdf2:sha256',
                                               salt_length=8)

        # Insert user's name, username and hashed password into users table
        cur.execute("INSERT INTO users(name, username, password) VALUES(?,?,?)",
                    (request.form.get('name'), username, hash_password))
        db.commit()

        # Select the new user ID from users table
        new_user = cur.execute(f"SELECT user_id FROM users WHERE username = '{username}'").fetchone()[0]
        # Load and login user
        user = load_user(new_user)
        login_user(user)
        # Redirect to the url for main
        return redirect(url_for('main'))
    # Render template for registration page
    return render_template("register.html")


@app.route('/logout')
@login_required
def logout():
    """
    Logouts current user and redirects to login page

    Returns:
        redirect to url for login_page
    """
    # Logout the current user
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('login_page'))


@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    """
    Deletes user of given user_id, if possible. Redirects to the table template

    Args:
        user_id (int): ID of selected user

    Returns:

    """
    # Get the username of the user with given user_id from users table
    user = cur.execute(f"SELECT username FROM users WHERE user_id = {user_id}").fetchone()
    # If username is 'admin'
    if user[0] == 'admin':
        # Send flash message
        flash("Cannot delete admin account")
        # Redirect to main
        return redirect(url_for('tables', table_name='users'))

    # Delete row from users table where user_id column has a value of given user ID
    cur.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")
    db.commit()
    # Send flash message
    flash(f"User '{user[0]}' has been deleted from the database")
    # Redirect to main
    return redirect(url_for('tables', table_name='users'))


@app.route("/delete_account")
def delete_account():
    """
    Deletes currently logged-in account

    Returns:
        Redirects for login page or main
    """
    # Get current user's ID and username
    user_id = current_user.id
    user_name = current_user.username
    # If current user is admin
    if user_name == "admin":
        # Send flash message
        flash("Cannot delete admin account")
        # Redirect to main
        return redirect(url_for('main'))
    # Delete row from users table where user_id matches current user ID
    cur.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")
    db.commit()
    # Send flash message
    flash("Account deleted")
    # Redirect to login page
    return redirect(url_for('login_page'))


@app.route("/analytics")
def get_analytics():
    """
    Creates plots and renders analytics page

    Returns:
        Render of analytics.html template
    """
    global db

    df_books = pd.read_sql_query("SELECT COUNT(*) AS count, title FROM books GROUP BY title", db)
    plot_and_save(data=df_books, x='count', y='title', path="static/images/books.png")

    df_rents = pd.read_sql_query("SELECT COUNT(*) as count, customers.name FROM rents "
                                 "JOIN customers ON rents.customer_id = customers.customer_id "
                                 "GROUP BY rents.customer_id", db)
    plot_and_save(df_rents, x='name', y='count', path="static/images/customer_rents.png", font_scale=0.7,
                  xtick_rotation=45)

    df_return_days = pd.read_sql_query("SELECT COUNT(name) as count, customers.name, return_date FROM rents "
                                       "JOIN customers ON customers.customer_id=rents.customer_id "
                                       "GROUP BY customers.name, return_date", db)
    plot_and_save(data=df_return_days, x='return_date', y='name', size='count', kind='scatter',
                  path="static/images/return_days.png", font_scale=0.4, xtick_rotation=45)

    df_queues = pd.read_sql_query("SELECT SUM(data.count) AS sum, books.title FROM "
                                  "(SELECT COUNT(customer_id) AS count, book_id FROM queues GROUP BY book_id) AS data "
                                  "JOIN books ON data.book_id=books.book_id GROUP BY books.title", db)
    plot_and_save(data=df_queues, x='sum', y='title', path="static/images/queue_numbers.png")
    return render_template('analytics.html', user=current_user)


def plot_and_save(data, x, y, path, **kwargs):
    """
    Creates plot for a given data and saves it

    Args:
        data (pandas.DataFrame): DataFrame with data that is to be plotted
        x (str): Name of the column from the DataFrame that is to be plotted on x-axis
        y (str): Name of the column from the DataFrame that is to be plotted on y-axis
        path (str): Path, where plot is to be saved

    Keyword Args:
        figsize (tuple of int): Figure size, defaults to (100, 50)
        font_scale (float): Scale of the plot font, defaults to 0.3
        axes_grid (bool): If axes grid are to be shown, defaults to True
        transparent_bg (bool): If plot background is to be transparent when saved, defaults to True
        kind (str): Kind of plot that to be created, defaults to bar plot, else creates scatterplot
        plt_color (str): Color of the plot, defaults to gray
        hue (str | None): Column from DataFrame that will decide hue of the plot points, defaults to None
        size (str | None): Column from DataFrame that will decide size of the plot points, defaults to None
        xlabel (str | None): X-axis label, defaults to None
        ylabel (str | None): Y-axis label, defaults to None
        xtick_rotation (int): Rotation (in degrees) of x-axis ticks, defaults to 0
        dpi (int): DPI of the saved plot, defaults to 1000
    """
    plt.tight_layout()
    sns.set(rc={'figure.figsize': kwargs.get('figsize', (100, 50))})
    sns.set(font_scale=kwargs.get('font_scale', 0.3))
    rcParams['axes.grid'] = kwargs.get('axes_grid', True)
    rcParams['savefig.transparent'] = kwargs.get('transparent_bg', True)

    if kwargs.get('kind', 'bar') == 'bar':
        fig = sns.barplot(data=data, x=x, y=y, color=kwargs.get('plt_color', 'gray'))
    else:
        fig = sns.scatterplot(data=data, x=x, y=y, hue=kwargs.get('hue', None), size=kwargs.get('size', None),
                              color=kwargs.get('color', 'gray'))

    fig.set(xlabel=kwargs.get('xlabel', None), ylabel=kwargs.get('ylabel', None))
    fig.set_xticklabels(fig.get_xticklabels(), rotation=kwargs.get('xtick_rotation', 0))
    fig.get_figure().savefig(path, dpi=kwargs.get('dpi', 1000))
    plt.clf()


@app.route("/insert_data/<table_name>", methods=["POST", "GET"])
@login_required
def insert_data(table_name):
    """
    Inserts new data into given table. Supports inserts into customers, workers and books tables. Utilizes
    LibrarySystem object methods for data insertion - thus requires the simulation to be generated

    Args:
        table_name (str): Name of the table that the data will be inserted into

    Returns:
        Sends flash message and redirects to the same page with data
    """
    # Get the global sim variable
    global sim
    # If method is 'POST' and simulation is generated
    if request.method == "POST" and sim:
        try:
            if table_name == "customers":
                sim.insert_data(table_name=table_name,
                                name=request.form.get("field_1"))
            elif table_name == "workers":
                sim.insert_data(table_name=table_name,
                                name=request.form.get("field_1"),
                                position=request.form.get("field_2"))
            elif table_name == "books":
                sim.insert_data(table_name=table_name,
                                title=request.form.get("field_1"),
                                author=request.form.get("field_2"),
                                isbn=request.form.get("field_3"),
                                publisher=request.form.get("field_4"),
                                year_published=int(request.form.get("field_5")))
            else:
                # If not a correct table name specified send flash message
                flash(f"Incorrect datatable specified: cannot insert data into {table_name} table!")
                return redirect(url_for("tables", table_name=table_name))
            # Send flash message indicating successful action
            flash(f"Successfully inserted new data into {table_name} table!")
            return redirect(url_for("tables", table_name=table_name))
        except ValueError:
            # Value error can be encountered when changing str to int for books table column year_published
            flash(f"Wrong datatype provided - year of publication must be an integer!")
            return redirect(url_for("tables", table_name=table_name))

    # If simulation is not generated but the method is 'POST'
    if not sim and request.method == "POST":
        # Flash a message indicating that the data cannot be added when sim is not generated
        flash("Cannot insert data if the simulation is not generated")
        return redirect(url_for("tables", table_name=table_name))
    # When method is 'GET' send flash message indicating incorrect request and redirect to main page
    flash("Incorrect request")
    return redirect(url_for("main"))


@app.route("/tables/<table_name>")
@login_required
def tables(table_name):
    """
    Renders tables.html template with given data. Requires logged-in user

    Args:
        table_name: name of table that is to be generated

    Returns:
        Renders template
    """
    try:
        # If queues table is selected
        if table_name == 'queues':
            # Select customer name, worker name, worker position, book ID, book title, book author, book publisher,
            # book ISBN, book year of publication for all items from queues table joined
            # with customers table on column customer_id for both tables
            # then with workers table on column worker_id for both tables
            # then with books table on column book_id for both tables
            # orders the items first by book_id column from books table, then by entry_id column from queues table
            table = cur.execute(f"""
            SELECT customers.name, workers.name, workers.position,
            books.book_id, books.title, books.author, books.publisher, books.isbn, books.year_published FROM queues
            JOIN customers ON queues.customer_id = customers.customer_id
            JOIN workers ON queues.worker_id = workers.worker_id
            JOIN books ON queues.book_id = books.book_id ORDER BY books.book_id, queues.entry_id
            """).fetchall()
            # Set column names
            column_names = ["Customer name", "Worker name", "Worker position", "Book ID", "Book title",
                            "Book author", "Book publisher", "Book ISBN", "Year of publication"]
        # Else if rents table is selected
        elif table_name == 'rents':
            # Select return date, customer name, worker name, worker position, book ID, book title, book author,
            # book publisher, book ISBN, book year of publication for all items from rents table joined
            # with customers table on column customer_id for both tables
            # then with workers table on column worker_id for both tables
            # then with books table on column book_id for both tables
            # orders the items first by customer_id column from customers table, then by return_date column from
            # rents table
            table = cur.execute(f"""
            SELECT return_date, customers.name, workers.name,
            workers.position, books.book_id, books.title, books.author, books.publisher, books.isbn, 
            books.year_published FROM rents
            JOIN customers ON rents.customer_id = customers.customer_id
            JOIN workers ON rents.worker_id = workers.worker_id
            JOIN books ON rents.book_id = books.book_id ORDER BY customers.customer_id, return_date
            """).fetchall()
            # Set column names
            column_names = ["Return date", "Customer name", "Worker name", "Worker position", "Book ID", "Book title",
                            "Book author", "Book publisher", "Book ISBN", "Year of publication"]
        # Else if logs table is selected
        elif table_name == 'logs':
            # If current user is not admin
            if current_user.username != 'admin':
                # raise PermissionError
                raise PermissionError
            # Get all columns and rows from logs table
            table = cur.execute("""SELECT * FROM logs""")
            # Set column names
            column_names = ["Log ID", "Action", "Customer ID", "Book ID", "Worker ID"]
        # Else if users table is selected
        elif table_name == 'users':
            # If current user is not admin
            if current_user.username != 'admin':
                # raise PermissionError
                raise PermissionError
            # Get all columns and rows from users table
            table = cur.execute("""SELECT * FROM users""")
            # Set column names
            column_names = ["User ID", "Name", "Username", "Password hash", "Delete"]
        else:
            # Select all rows and columns from selected table
            table = cur.execute(f"""
            SELECT * FROM {table_name}
            """).fetchall()
            # If workers table is selected
            if table_name == 'workers':
                # Set column names
                column_names = ["ID", "Name", "Position"]
            # Else if customers table is selected
            elif table_name == 'customers':
                # Set column names
                column_names = ["ID", "Name"]
            # Else means that the books table is selected
            else:
                # Set column names
                column_names = ["ID", "Title", "Author", "ISBN", "Publisher", "Year of publication"]
    except PermissionError:
        # If PermissionError is raised set table and column_names variables to None
        table = None
        column_names = None
    # Render template with correct data
    return render_template("table.html", table=table, colnames=column_names, title=table_name,
                           bootstrap=bootstrap, user=current_user)


@app.route("/sim")
@login_required
def simulation():
    """Renders simulation page template. Requires logged-in user"""
    return render_template('simulation.html', bootstrap=bootstrap, user=current_user)


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
        socket.emit('redirect', {'url': url_for('main')})
        # return none to stop function from continuing
        return None
    for _ in range(int(iters)):
        # for every iteration get action messages
        result = sim.run_and_return_messages(num_sub_iterations=int(actions))
        for log in result:
            # for every message emit message and pause socket for 1 second
            socket.send(log)
            socket.sleep(1)
    # at the end sent empty message
    socket.send(None)


if __name__ == "__main__":
    socket.run(app, allow_unsafe_werkzeug=True)
