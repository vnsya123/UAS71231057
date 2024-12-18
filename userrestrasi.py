from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)

@app.route('/success/<name>', methods=['GET'] )
def success(name):
    return 'Proses data user : %s berhasil' % name

@app.route('/userlist')
def userList():
    users = getAllUser()
    print(users)
    return render_template('userlist.html', title='Daftar User', listuser=users)

@app.route("/login", methods=['POST']) 
def login():
    pass

@app.route("/registeruser", methods=['POST']) 
def registeruser():
    pass    

def getAllUser():
    # Open database connection
    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()
    # Execute the query
    cursor.execute("SELECT realname, pob, username, password FROM user;")    

    # convert it into dictionary
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]
    # Close the connection
    connection.close()
    return data

if __name__ == '__main__':
    app.run()




#Login: http://127.0.0.1:5000/login
#c:\Users\ASUS\Downloads\loginform(4).html
#Registrasi: http://127.0.0.1:5000/registeruser
