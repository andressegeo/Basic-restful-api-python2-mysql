#!/usr/bin/python
from flask import Flask, jsonify, request, json
import MySQLdb
import simplejson
app = Flask(__name__)
Templates = [
    {
        "id":1,
        "date":"2018-04-25",
        "text": "ceci est un test",
        "reccurence": "tous les jours",
        "manager_id": 2,
    },
    {
        "id":2,
        "date":"2018-04-25",
        "text": "ceci est un test",
        "reccurence": "Une seule fois",
        "manager_id": 1,

    },
    {
        "id":3,
        "date":"2018-05-05",
        "text": "ceci est un test",
        "reccurence": "tous les Mois",
        "manager_id": 2,
    }
]

con = MySQLdb.connect(host="localhost",    
                     user="root",         
                     passwd="yr_pass",           
                     db="yr_db")
                    
"""
As her name indicates, this method allow to get all mail templates in database
"""
@app.route('/templates', methods=['GET'])
def get_all_mail_templates():         
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Form")
        items = []
        for row in cursor.fetchall():
            print(row)
            items.append({
                'id' : row[0],
                'date' : row[1],
                'text' : row[2],
                'reccurence' : row[3],
                'manager_id' : row[4]
            })
        con.commit()     
    except:
        con.rollback()
    con.close()
    return jsonify({"mail templates" : items})    


"""
Help to retrieve all users in db
"""
@app.route('/users', methods = ['GET'])    
def get_all_users():
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Manager")
        items = []
        for row in cursor.fetchall():
            print(row)
            items.append({
                'id' : row[0],
                'email' : row[1]
            })
        con.commit()     
    except:
        con.rollback()
    con.close()
    return jsonify({"Users" : items}) 
    


"""
This method help to add one mail template in the Form's table
"""
@app.route('/mail', methods=['POST'])
def add_one_mail_template():
    #print(request.data)
    mail_template = json.loads(request.data)
    print("test Form: ", mail_template['text'])
    #id = mail_template['id']
    date = mail_template['date']
    text = mail_template['text']
    reccurence = mail_template['reccurence']
    manager_id = mail_template['manager_id']
    try:
        cursor = con.cursor()
        Form = """
        INSERT INTO Form
        VALUES
            (%s, %s, %s, %s)
         """
        cursor.execute(Form, (date, text, reccurence, manager_id))
        con.commit()
    except:
        con.rollback()
    con.close()
    
    Templates.append(mail_template)
    return jsonify({"mail Templates":Templates})


"""
This method help to add one user in the database
"""
@app.route('/user', methods=['POST'])
def add_one_user():
    manager_account = json.loads(request.data)
    print("test Form: ", manager_account['email'])
    id_manager = manager_account['id']
    email = manager_account['email']
    try:
        cursor = con.cursor()
        Manager = """
        INSERT INTO Manager
        VALUES
            (%s, %s)
         """
        cursor.execute(Manager, (id_manager, email))
        con.commit()
    except:
        con.rollback()
    con.close()
    treat = []
    treat = get_all_users()
    return treat

if(__name__) == "__main__":
    app.run(debug=True, port=5003)