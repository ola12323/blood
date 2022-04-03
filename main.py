import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import pickle
import yaml

model = pickle.load(open('blood.pkl', 'rb'))
model1 = pickle.load(open('file.pkl', 'rb'))

app = Flask(__name__)

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,password))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if (password) == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
            return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/blood', methods=['GET', 'POST'])
def blood():
    return render_template('blood.html')

@app.route('/blood1', methods=['GET', 'POST'])
def blood1():
    return render_template('blood1.html')

@app.route('/predykcja', methods=['POST'])
def home1():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    arr = np.array([[data1, data2, data3, data4]])
    pred = model.predict(arr)
    return render_template('after.html', data=pred)


@app.route('/predykcja2', methods=['POST'])
def home2():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    data5 = request.form['e']
    data6 = request.form['f']
    data7 = request.form['g']
    arr = np.array([[data1, data2, data3, data4, data5, data6, data7]])
    pred = model1.predict(arr)
    return render_template('prediction.html', data=pred)


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)
