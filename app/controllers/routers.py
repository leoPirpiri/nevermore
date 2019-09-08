from app import app

@app.route("/")
def index():
    return "Hello world! teste 3"