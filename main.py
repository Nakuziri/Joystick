from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
import flask_login

conn = pymysql.connect(
   database="xcampos_joystick",
   user='xcampos',
   password='221349988',
   host='10.100.33.60', 
   cursorclass=pymysql.cursors.DictCursor
)

app = Flask(__name__)


app.secret_key = 'bombaclaaattttt'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

class user:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__ (self,id,username):
        self.username = username
        self.id = id

    def get_id(self):
        return str(self.id)
    
@login_manager.user_loader
def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `ID` = " + str(user_id))
    result = cursor.fetchone()
    cursor.close()
    conn.commit()

    if result is None:
        return None
    
    return user(result["ID"],result['Username'])

@app.route('/land')
def landingpage():
    if flask_login.current_user.is_authenticated:
        return redirect('feed')
   

    return render_template('land.html.jinja')

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

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        usernameLog = request.form["usernameLog"]
        passwordLog = request.form["passwordLog"]
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE `Username` = '{usernameLog}' ")

        result = cursor.fetchone()

        cursor.close()
        conn.commit()

        if passwordLog == result['Password']:
            user = load_user(result['ID'])
            flask_login.login_user(user)
            return redirect('/feed')
        
    return render_template('sign_in.html')

@app.route('/feed',methods=['GET','POST'])
@flask_login.login_required
def post_feed():
    if user.is_authenticated:
        return flask_login.current_user
    else:
        return render_template('sign_in.html')