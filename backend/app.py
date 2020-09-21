from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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

def removeUser(uid):
    uid = request.json["id"]
    if (uid):
        try:
            user = Users.query.get(uid)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False

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
            return jsonify({"error": "Invalid form"})
    except:
        return jsonify({"error": "Invalid form"})

@app.route("/api/register", methods=["POST"])
def register():
    try: 
        email = request.json["email"]
        email = email.lower()
        password = request.json["pwd"]
        username = request.json["username"]
if __name__ == "__main__":
    app.run(debug=True)
            
# Setup liverefresh
if __name__ == "__main__":
  app.run(debug=True)
