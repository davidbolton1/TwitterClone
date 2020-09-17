from flask import Flask

app = Flask(__name__)

#First route
@app.route('/')
def index():
    return "Hello, world!"

# Setup liverefresh
if __name__ == "__main__":
  app.run(debug=True)
