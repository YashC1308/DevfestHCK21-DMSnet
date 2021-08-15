# Store this code in 'app.py' file
  
from flask import Flask, render_template, request, redirect, url_for, session,flash,Markup
import mysql.connector
import requests
import json
import re
from datetime import date
from Account import User
'''
THE MYSQL DATABASE = dims
Table = Contract

Create table contract(

id int(10) not null auto_increment,
party1_id int(10),
party2_id int(10),
party1_pledge varchar(1000) not null,
party2_pledge varchar(1000) not null,
party1_accepted int(1),
party2_accepted int(1),
date varchar(15),
Primary key (id)

)



'''
global user
user  = User()
app = Flask(__name__)
app.secret_key = 'your secret key'


cnx = mysql.connector.connect(user='root', password='15w60ps',
                              host='localhost',
                              database='dims')  
cursor = cnx.cursor()

def Load_Dashboard(party1_Id):


        
        cursor.execute("SELECT party1_Id,party2_Id,date FROM contract WHERE party1_id={} or party2_Id={};".format(party1_Id,party1_Id))


        data1 = cursor.fetchall()

        cursor.execute("SELECT party1_accepted,party2_accepted FROM contract WHERE party1_id={} or party2_Id={};".format(party1_Id,party1_Id))
        accepted = cursor.fetchall()
        cursor.execute("SELECT id FROM contract WHERE party1_id={} or party2_Id={};".format(party1_Id,party1_Id))
        Contract_Id = cursor.fetchall()
        data = []
        for i in range(0,len(data1)):
            if accepted[i][0] == accepted[i][1] and accepted[i][0] ==1:
                out = "Yes"

            else:
                out = "No"
            temp = list(data1[i])
            temp.append(out)
            temp.append(Contract_Id[i][0])

            data.append(temp)
        print(data)
        return data



def Make_Contract(party1_Id,party2_Id,party1_pledge,party2_pledge):
    Date = date.today()

    cursor.execute("INSERT INTO contract  VALUES (NULL,'{}','{}','{}','{}',0,0,'{}');".format(party1_Id,party2_Id,party1_pledge,party2_pledge,Date))
    cnx.commit()

@app.route('/')
@app.route('/index', methods =['GET', 'POST'])





def index():

        
    print('-------------------------------------------------')
            
    return render_template('Index.html')


@app.route('/listing', methods =['GET', 'POST'])
def listing():
    if user.LoggedIn:
        cursor.execute('select * from profiles;')
        data = cursor.fetchall()
        cursor.execute('select type_of_art from profiles group by type_of_art;')
        options = cursor.fetchall()
        if request.method == 'POST' and 'type' in request.form:
            print(request.form)
            cursor.execute("select * from profiles where type_of_art ='{}';".format(request.form['type']))
            data = cursor.fetchall()
            print(data)
        return render_template('listing.html',data = data,options = options)
    else:
        return render_template('login.html', msg = 'Login to your account')

@app.route('/CreateContract', methods =['GET', 'POST'])
def CreateContract():
    if user.LoggedIn:
        msg = 'Please Fill up the Form'
        array = ['ID1','ID2','ID3','ID4']
        print(request.form)
        print(request.method)
        if request.method == 'POST' and 'creator_Id' in request.form:
            print(111)
            if request.form['password']== user.password:
                party1_Id = user.Id
                party2_Id = request.form['creator_Id']
                party2_pledge = request.form['order']
                party1_pledge = request.form['price']
                array = (party1_Id,party2_Id,party1_pledge,party2_pledge)

                if '' in array or 'ID1' in array or 'ID2' in array or 'ID3' in array or 'ID4' in array:
                    msg = 'Please fill the form correctly'
                    print(msg)
                
                else:
                    Make_Contract(party1_Id,party2_Id,party1_pledge,party2_pledge)
                    msg = 'Order Placed succesfully'
                    array = ["","","","",""]
            else:
                msg = 'Please Enter the correct Password'

        return render_template('CreateContract.html', msg = msg,array = array)
    else:
        return render_template('login.html', msg = 'Login to your account')

@app.route('/dashboard', methods =['GET', 'POST'])
def dashboard():

    if user.LoggedIn:

        data = Load_Dashboard(user.Id)




        return render_template('dashboard.html', data = data)
    else:

        return render_template('login.html', msg = 'Login to your account')

@app.route("/contract/<Contract_Id>", methods =['GET', 'POST'])
def ContractDeet(Contract_Id):
    cursor.execute("SELECT * FROM contract WHERE id={};".format(Contract_Id))
           

    data = list(cursor.fetchall()[0])
    if data[5]== 0:
        data[5] = "No"
    else:
        data[5] = "Yes"
    if data[6]== 0:
        data[6] = "No"
    else:
        data[6] = "Yes"
    print(data)
    return render_template('ContractDeets.html', data = data)

@app.route('/login', methods =['GET', 'POST'])
def login():
    print(user.LoggedIn)
    Id = 0
    msg = 'Please Fill up the Form'
    print(request.form)
    if user.LoggedIn:
        print('attempt to load dashboard')
        data = Load_Dashboard(user.Id)
        print('dashboard loaded ')
        return render_template('dashboard.html',data = data)
    else:
        if request.method == 'POST' and 'password' in request.form and 'username' in request.form:
            
            password = request.form['password']
            username = request.form['username']
            cursor.execute("select id ,type from login where password = '{}' and username = '{}'".format(password,username))
            try:
                (Id,Type) = cursor.fetchone()
                print(Id,Type)
            except:
                msg = 'Incorrect Login Credentials'
                
            if Id:
                msg = 'Logged In'
                user.Login(Id,Type,password)
                print('attempt to load dashboard')
                data = Load_Dashboard(user.Id)
                print('dashboard loaded ')
                return render_template('dashboard.html',data = data)

            else:
                msg = 'Incorrect Login Credentials'
        else:
            msg = "Please Fill up the Form"


        return render_template('login.html',msg = msg)

@app.route('/logout', methods =['GET', 'POST'])
def logout():
    user.Logout()
    print(user.LoggedIn)
    return render_template('login.html',msg = 'You have succesfully logged out')


@app.route('/sign_up', methods =['GET', 'POST'])
def sign_up():

    msg = 'Please Fill up the Form'
    print(request.form)

    if request.method == 'POST' and 'password' in request.form and 'username' in request.form and 'email' in request.form and (request.form['type']=='creator' or request.form['type']=='customer') :

        password = request.form['password']
        username = request.form['username']
        password2 = request.form['password2']
        Type = request.form['type']
        if password2 == password:
            cursor.execute("insert into login values(NULL,'{}','{}','{}')".format(username,password,Type))
            cnx.commit()
            msg = "You have signed up succesfully"
        else:
            msg = 'Please make sure both the passwords match'
        

    else:
        msg = "Please Fill up the Form"


    return render_template('sign_up.html',msg = msg)

if __name__ == "__main__":
    app.run()
    
