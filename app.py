# Store this code in 'app.py' file
  
from flask import Flask, render_template, request, redirect, url_for, session,flash,Markup
import mysql.connector
import requests
import json
import re
from datetime import date
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
app = Flask(__name__)
app.secret_key = 'your secret key'


cnx = mysql.connector.connect(user='root', password='15w60ps',
                              host='localhost',
                              database='dims')  
cursor = cnx.cursor()

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
    cursor.execute('select * from profile;')
    data = cursor.fetchall()
    
    return render_template('listing.html',data = data)
  
@app.route('/CreateContract', methods =['GET', 'POST'])
def CreateContract():
    msg = 'Please Fill up the Form'
    array = ['ID1','ID2','ID3','ID4']
    if request.method == 'POST' and 'party1_Id' in request.form:
        party1_Id = request.form['party1_Id']
        party2_Id = request.form['party2_Id']
        party1_pledge = request.form['party1_pledge']
        party2_pledge = request.form['party2_pledge']
        array = (party1_Id,party2_Id,party1_pledge,party2_pledge)

        if '' in array or 'ID1' in array or 'ID2' in array or 'ID3' in array or 'ID4' in array:
            msg = 'Please fill the form correctly'
            print(msg)
        
        else:
            Make_Contract(party1_Id,party2_Id,party1_pledge,party2_pledge)
            array = ["","","","",""]


    return render_template('CreateContract.html', msg = msg,array = array)

@app.route('/ViewContract', methods =['GET', 'POST'])
def ViewContract():
    msg = ''
    if True :
        party1_Id = 36

        
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
        print('11111')
        print(data)

        return render_template('ViewContract.html', data = data, msg = msg)

    elif request.method == 'POST':
        msg = 'Please fill out the details !'
    return render_template('ViewContract.html', msg = msg)

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



if __name__ == "__main__":
    app.run()
    
