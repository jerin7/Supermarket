from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_cors import cross_origin
import pandas as pd
import pyodbc

employee = { "Jerin" : "jerin1234"}


#connection to database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-QAE3V34M\MY_INSTANCE1;'
                      'Database=Supermarket;'
                      'Trusted_Connection=yes;');


app = Flask(__name__,template_folder='template')
app.secret_key = 'hello'    #Secret key.

@app.route('/')             #This is a decorator.
@cross_origin()
def home():
    return render_template('index1.html')


@app.route('/login', methods=['POST','GET']) 
@cross_origin()
def login():
    flag = 0
    if request.method == 'POST':
        user = request.form['name']   #'name' is the name of the dictionary key.
        pwd = request.form['password']
        for key, value in employee.items():
            if key == user and value == pwd:
                session['user'] = user      #'user' is the name of the dictionary key.
                #flash("Login Succesful!")
                return redirect(url_for("product"))
                flag = 1
                break
        if flag == 0:
            flash("INCORRECT USERNAME or PASSWORD !!")
            return redirect(url_for('login'))
    else:
        if 'user' in session:       #Check notes 446-448.
            flash("Already logged in")
            return redirect(url_for('product'))

        return render_template('login.html')


@app.route('/user')
@cross_origin()
def user():
    if 'user' in session:
        user = session['user']
        return render_template('user.html', user = user)
    else:
        flash("You are not logged in yet.")
        return redirect(url_for('login'))


@app.route('/logout')
@cross_origin()
def logout():
    #The next 3 lines of code is for checking if the user is in the session. And if he is there then we will logout with the user name.
    if 'user' in session:
        user = session['user']
        flash(f"You have succesfully logged out, {user}.","info")
    session.pop('user',None)    #Remove the user data from our sessions. None is a message associated with removing that data.
    return redirect(url_for('home'))


@app.route("/supermarket", methods = ["GET", "POST"])
@cross_origin()
def supermarket():
    data1 = pd.read_sql("SELECT * FROM supermarket", conn)
    result=data1.to_html()
    return result


    
@app.route("/product", methods = ["GET", "POST"])
@cross_origin()
def product():
    data2 = pd.read_sql("SELECT * FROM product", conn)
    result=data2.to_html()
    return result

@app.route("/customer", methods = ["GET", "POST"])
@cross_origin()
def customer():
    data3 = pd.read_sql("SELECT * FROM customer", conn)
    result=data3.to_html()
    return result


@app.route("/department", methods = ["GET", "POST"])
@cross_origin()
def department():
    data4 = pd.read_sql("SELECT * FROM department", conn)
    result=data4.to_html()
    return result
	
@app.route("/fetch", methods=['POST', 'GET'])	
def fetch():
    if request.method == "POST":
        prodid = request.form['prod_id']
        
        with cnxn as conn:
            with conn.cursor() as cursor:
                cursor.execute( "SELECT * FROM product WHERE prod_id = ?" ,(prodid) )
                data = cursor.fetchall()
            return render_template("index.html", data=data)
    else:
        return render_template("fetch.html")
		
@app.route("/add", methods=['POST', 'GET'])  
def add(): 
    if request.method == "POST":
        prod_id = request.form['prod_id']
        name = request.form['name']
        price = request.form['price']
        with cnxn as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO product VALUES (?, ?, ?)", (prod_id, name, price))
            return render_template("add.html")
    else:
        return render_template('add.html')  


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug = True) 
#The "debug = True" will make the server update by itself and make the changes for us.
