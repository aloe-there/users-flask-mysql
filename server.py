from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL      # import the function that will return an instance of a connection
app = Flask(__name__)

@app.route("/users")
def index():
    mysql = connectToMySQL('users_schema')       # call the function, passing in the name of our db
    query = 'SELECT *, DATE_FORMAT(created_at, "%M %d, %Y") as creation_date FROM users;'
    users = mysql.query_db(query)  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html", all_users = users)

@app.route("/users/new")
def create_user():
    return render_template("create.html")

@app.route("/users/add", methods=["POST"])
def add_user_to_db():
    print(request.form)
    mysql = connectToMySQL('users_schema')
    query = "INSERT INTO users (firstname, lastname, email) VALUES (%(fn)s, %(ln)s, %(email)s);"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"]
    }
    new_user_id = mysql.query_db(query,data)
    return redirect('/users')

            
if __name__ == "__main__":
    app.run(debug=True)

