from app import app

print "Running server boss"

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'


app.run(debug=DEBUG, host=HOST, port=PORT)