from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set db file to users.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# DB
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True) # primary_key makes it so that this value is unique and can be used to identify this record.
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    # Constructor
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd

#First route
@app.route('/')
def index():
    return "Hello, world!"

# Setup liverefresh
if __name__ == "__main__":
  app.run(debug=True)
