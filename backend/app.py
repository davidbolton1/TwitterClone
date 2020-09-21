from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

# Set db file to users.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# Database with SQLAlchemy
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True) 
    # Set a primary_key makes it so that this value is unique and can be used to identify this record.
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    # Constructor for db setup
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd

db.create_all()
#First route to test
@app.route('/')
def index():
    return "Test route yes!"

#Api routes
#Get user function to return user info from our database
def getUsers():
    users = Users.query.all()
    return [{"id": i.id, "username": i.username, "email": i.email, "password": i.pwd} for i in users]

#Add user given submitted info
def addUser(username, email, pwd):
    if (username and pwd and email):
        try:
            user = Users(username, email, pwd)
            db.session.add(user)
            db.session.commit()
            return True
            #For error handing, print exception
        except Exception as exc:
            print(exc)
            return False
    else:
        return False

#Route to remove a user
#Query the database for the user given an id, delete
def removeUser(currentid):
    currentid = request.json["id"]
    if (currentid):
        try:
            user = Users.query.get(currentid)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as exc:
            print(exc)
            return False
    else:
        return False

#Login route, post request to database given an email and password
@app.route("/api/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["pwd"]
        if (email and password):
            users = getUsers()
            ## Check If a user exists
            return jsonify(len(list(filter(lambda x: x["email"] == email and x["password"] == password, users))) == 1)
        else:
            return jsonify({"error": "Invalid informaiton, please try again."})
    except:
        return jsonify({"error": "Invalid information, please try again."})

#Register route, set payload to DB = to email/pw/username given
@app.route("/api/register", methods=["POST"])
def register():
    try: 
        email = request.json["email"]
        email = email.lower()
        password = request.json["pwd"]
        username = request.json["username"]
        #First check if user exists w/ given information
        users = getUsers()
        if(len(list(filter(lambda x: x["email"] == email, users))) == 1):
            return jsonify({"error": "User exists, please try again."})
        #Email validation
        # I SHOULD REALLY IMPROVE THIS WITH A LIBRARY!!!!
        # Regex from https://blog.mailtrap.io/python-validate-email/
        # Currently does not check for typos
        if not re.match(r"^[a-z]([w-]*[a-z]|[w-.]*[a-z]{2,}|[a-z])*@[a-z]([w-]*[a-z]|[w-.]*[a-z]{2,}|[a-z]){4,}?.[a-z]{2,}$", email):
            return jsonify({"error": "Invalid form"})
        addUser(username, email, password)
        return jsonify({"success": True})
    except:
        return jsonify({"error": "Invalid form"})


if __name__ == "__main__":
    app.run(debug=True)
            
# Setup liverefresh
if __name__ == "__main__":
  app.run(debug=True)
