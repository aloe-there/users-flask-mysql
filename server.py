from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL      # import the function that will return an instance of a connection
app = Flask(__name__)

@app.route('/')
def go_to_home():
    return redirect('/users')

@app.route("/users")
def home_page():
    mysql = connectToMySQL('users_schema')       # call the function, passing in the name of our db
    query = 'SELECT *, DATE_FORMAT(created_at, "%M %d, %Y") as creation_date FROM users;'
    users = mysql.query_db(query)  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html", all_users = users)

@app.route("/users/new")
def create_user():
    return render_template("create.html")

@app.route("/users/<int:id>")
def show_user(id):
    mysql = connectToMySQL('users_schema')       # call the function, passing in the name of our db
    query = f'SELECT *, DATE_FORMAT(created_at, "%M %d, %Y") as creation_date, \
                        DATE_FORMAT(updated_at, "%M %d, %Y at %h:%i %p") as update_datetime \
                        FROM users WHERE id={id};'
    user = mysql.query_db(query)  # call the query_db function, pass in the query as a string
    print("Show",user)
    return render_template("show.html", user=user[0])

@app.route("/users/<int:id>/edit")
def edit_user(id):
    mysql = connectToMySQL('users_schema') 
    query = f"SELECT * FROM users WHERE id={id};"
    user = mysql.query_db(query)
    return render_template("update.html", user=user[0])

@app.route("/users/add", methods=["POST"])
def add_user_to_db():
    print(request.form)
    mysql = connectToMySQL('users_schema')
    query = "INSERT INTO users (firstname, lastname, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(email)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"]
    }
    new_user_id = mysql.query_db(query, data)
    return redirect(f"/users/{new_user_id}")

@app.route("/users/<int:id>/update", methods=["POST"])
def update_user(id):
    mysql = connectToMySQL('users_schema')
    query = "UPDATE users SET firstname=%(fn)s,  lastname=%(ln)s, email=%(email)s, updated_at=NOW() WHERE id=%(id)s"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"],
        "id": id
    }
    mysql.query_db(query, data)
    return redirect(f"/users/{id}")

@app.route("/users/<int:id>/delete")
def delete_user(id):
    mysql = connectToMySQL('users_schema')
    query = f"DELETE FROM users WHERE id={id};"
    mysql.query_db(query)
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)

