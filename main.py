from flask import Flask, g,  render_template, request, redirect
import pymysql
import pymysql.cursors
import flask_login



app = Flask(__name__)

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="xcampos",
        password="221349988",
        database="xcampos_joystick",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 




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
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `users` WHERE `ID` = " + str(user_id))
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()

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


        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `users` (`username`, `password`,`email`) VALUES ('{username}', '{password}', '{email}')")
        cursor.close()
        get_db().commit()
    
    return render_template("register.html")

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        usernameLog = request.form["usernameLog"]
        passwordLog = request.form["passwordLog"]
        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE `Username` = '{usernameLog}' ")

        result = cursor.fetchone()

        cursor.close()
        get_db().commit()

        if passwordLog == result['Password']:
            user = load_user(result['ID'])
            flask_login.login_user(user)
            return redirect('/feed')
        
    return render_template('sign_in.html')

@app.route('/feed',methods=['GET','POST'])
@flask_login.login_required
def post_feed():
    return render_template('feed.html.jinja')

@app.route('/post', methods=['POST'])
@flask_login.login_required
def create_post():
    description = request.form['description']
    user_id = flask_login.current_user.id

    cursor = get_db().cursor()

    cursor.execute("INSERT INTO `posts` (`description`, `user_id`)")