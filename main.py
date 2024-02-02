from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors

conn = pymysql.connect(
   database="xcampos_joystick",
   user='xcampos',
   password='221349988',
   host='10.100.33.60', 
   cursorclass=pymysql.cursors.DictCursor
)

app = Flask(__name__)

@app.route('/land')
def index():
    user_name = 'goodjob'

    return render_template('land.html.jinja', user_name = user_name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Do this for every input in your form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]


        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `users` (`username`, `password`,`email`) VALUES ('{username}', '{password}', '{email}')")
        cursor.close()
        conn.commit()
    
    return render_template("register.html")
