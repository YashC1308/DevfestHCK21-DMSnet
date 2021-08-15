# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session, flash, Markup
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
user = User()
app = Flask(__name__)
app.secret_key = 'your secret key'


cnx = mysql.connector.connect(user='root', password='Kuchnahi#00',
                              host='localhost',
                              database='dims')
cursor = cnx.cursor()


def Load_Dashboard(party1_Id):

    cursor.execute("SELECT party1_Id,party2_Id,date FROM contract WHERE party1_id={} or party2_Id={};".format(
        party1_Id, party1_Id))

    data1 = cursor.fetchall()

    cursor.execute("SELECT party1_accepted,party2_accepted FROM contract WHERE party1_id={} or party2_Id={};".format(
        party1_Id, party1_Id))
    accepted = cursor.fetchall()
    cursor.execute("SELECT id FROM contract WHERE party1_id={} or party2_Id={};".format(
        party1_Id, party1_Id))
    Contract_Id = cursor.fetchall()
    data = []
    for i in range(0, len(data1)):
        if accepted[i][0] == accepted[i][1] and accepted[i][0] == 1:
            out = "Yes"

        else:
            out = "No"
        temp = list(data1[i])
        temp.append(out)
        temp.append(Contract_Id[i][0])

        data.append(temp)
    print(data)
    return data


@app.route('/MakeContract', methods=['GET', 'POST'])

def MakeContract():
    values = ['', '', '']
    Date = date.today()
    if request.method == 'POST' and 'creator_Id' in request.form:
        print(111)

        msg = 'Please fill the form correctly'


        cursor.execute("INSERT INTO contract  VALUES (NULL,'{}','{}','{}','{}',1,0,'{}');".format(party1_Id, party2_Id, party1_pledge, party2_pledge, Date))
        cnx.commit()
        msg = 'Order Placed succesfully'
        array = ["", "", "", "", ""]
    else:
        msg = 'Please Enter the correct Password'

    return render_template('CreateContract.html', msg=msg, values=["", "", "", "", ""])


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

    print('-------------------------------------------------')

    return render_template('Index.html')


@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if user.LoggedIn:
        pictures = ['Profile_pic1.jpg', 'Profile_pic2.jpg', 'Profile_pic3.jpg',
                    'Profile_pic4.jpg', 'Profile_pic5.jpg', 'Profile_pic6.jpg']
        cursor.execute('select * from profiles;')
        data1 = cursor.fetchall()
        cursor.execute(
            'select type_of_art from profiles group by type_of_art;')
        options = cursor.fetchall()
        if request.method == 'POST' and 'type' in request.form:
            print(request.form)
            cursor.execute(
                "select * from profiles where type_of_art ='{}';".format(request.form['type']))
            data1 = cursor.fetchall()
        data = []
        for i in data1:
            data.append(list(i))
        for i in range(len(data)):
            j = i
            while j > 5:
                j -= 5
            data[i].append(pictures[j])

        return render_template('listing.html', data=data, options=options)
    else:
        return render_template('login.html', msg='Login to your account')




@app.route('/CreateContract/<id>', methods=['GET', 'POST'])
def CreateContract(id):
    values = ['', '', '']
    if user.LoggedIn:
        try:
            if id:
                
                cursor.execute(
                    "SELECT * FROM contract WHERE id={};".format(id))
                values = list(cursor.fetchall()[0])
        except:
            values = ['', '', '']
        msg = 'Please Fill up the Form'
        array = ['ID1', 'ID2', 'ID3', 'ID4']
        return render_template('CreateContract.html', values=values)

    else:
        return render_template('login.html', msg='Login to your account', values=values)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if user.LoggedIn:

        data = Load_Dashboard(user.Id)

        return render_template('dashboard.html', data=data, type=user.Type)
    else:

        return render_template('login.html', msg='Login to your account')


@app.route("/contract/<Contract_Id>", methods=['GET', 'POST'])
def ContractDeet(Contract_Id):
    cursor.execute("SELECT * FROM contract WHERE id={};".format(Contract_Id))

    data = list(cursor.fetchall()[0])
    if data[5] == 0:
        data[5] = "No"
    else:
        data[5] = "Yes"
    if data[6] == 0:
        data[6] = "No"
    else:
        data[6] = "Yes"
    print(data)

    return render_template('ContractDeets.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(user.LoggedIn)
    Id = 0
    msg = 'Log in here'
    print(request.form)
    if user.LoggedIn:
        print('attempt to load dashboard')
        data = Load_Dashboard(user.Id)
        print('dashboard loaded ')
        return render_template('dashboard.html', data=data, type=user.Type)
    else:
        if request.method == 'POST' and 'password' in request.form and 'username' in request.form:

            password = request.form['password']
            username = request.form['username']
            cursor.execute("select id ,type from login where password = '{}' and username = '{}'".format(
                password, username))
            try:
                (Id, Type) = cursor.fetchone()
                print(Id, Type)
            except:
                msg = 'Incorrect Login'

            if Id:
                msg = 'Logged In'
                user.Login(Id, Type, password)
                print('attempt to load dashboard')
                data = Load_Dashboard(user.Id)
                print('dashboard loaded ')
                return render_template('dashboard.html', data=data, type=user.Type)

            else:
                msg = 'Incorrect Login'
        else:
            msg = "Login here"

        return render_template('login.html', msg=msg)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user.Logout()
    print(user.LoggedIn)
    return render_template('index.html', msg='You have succesfully logged out')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if user.LoggedIn:
        cursor.execute('select * from profiles;')
        data = cursor.fetchall()
        cursor.execute(
            'select type_of_art from profiles group by type_of_art;')
        options = cursor.fetchall()
        return render_template('profile.html', profile=data, options=options)
    else:
        return render_template('login.html', msg='Login here')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():

    msg = 'Please Fill up the Form'
    print(request.form)

    if request.method == 'POST' and 'password' in request.form and 'username' in request.form and 'email' in request.form and (request.form['type'] == 'creator' or request.form['type'] == 'customer'):

        password = request.form['password']
        username = request.form['username']
        password2 = request.form['password2']
        Type = request.form['type']
        if password2 == password:
            cursor.execute("insert into login values(NULL,'{}','{}','{}')".format(
                username, password, Type))
            cnx.commit()
            msg = "Sign up success"
            return render_template('login.html', msg=msg)
        else:
            msg = 'Please make sure both the passwords match'

    else:
        msg = "Please Fill up the Form"

    return render_template('sign_up.html', msg=msg)

# sidak functions


def msgsdr(name, messages, receiver, sender):
    uid = "idk"
    TBL1_NAME = "idk2"
    print("try")
    try:
        try:
            # query may need edit
            #cursor.execute("select UserId from {} where Name='{}';".format(TBL1_NAME,name))
            print("aaaaa")
        except:
            print("No such user exists")
        else:
            data = cursor.fetchone()
            (Rid,) = data
            # query needs edit
            cursor.execute("INSERT INTO `dims`.`chat_message` (`to_user_id`, `from_user_id`, `chat_message`, `status`) VALUES ({},{},{},'1');".format(
                receiver, sender, messages))
            cnx.commit()
    except:
        print("Oops! An error occured, try again later")


def recmsg(sender, receiver):
    cursor.execute("select chat_message,timestamp,from_user_id from chat_message where from_user_id = {} or from_user_id={}  order by timestamp".format(
        sender, receiver))
    data = cursor.fetchall()
    chat = []
    for i in data:
        tar = ["", ""]
        if i[-1] == int(sender):
            tar[0] = i[0]
        else:
            tar[1] = i[0]
        chat.append(tar)

    for i in range(len(chat)-2):
        if chat[i][0] and chat[i][1] == "":
            chat[i][1] = chat[i+1][1]
            chat.pop(i+1)
        if chat[i][1] and chat[i][0] == "":
            chat[i][0] = chat[i+1][0]
            chat.pop(i+1)
        if chat[i][0] == "" and chat[i+1][0] == "":
            chat[i][1] += " /n" + chat[i+1][1]
            chat.pop(i+1)
        if chat[i][1] == "" and chat[i+1][1] == "":
            chat[i][0] += " /n" + chat[i+1][0]
            chat.pop(i+1)
    return chat


@app.route('/chat', methods=['GET', 'POST'])
def chat(rid="2"):
    # get nm from html
    sender = "1"
    receiver = rid
    chat = recmsg(sender, receiver)
    print(chat)
    return render_template("chat.html", chat=chat)


if __name__ == "__main__":
    app.run()
