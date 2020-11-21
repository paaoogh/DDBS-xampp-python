#!/usr/bin python3

import mysql.connector
from mysql.connector import errorcode
import sys
import cgi
import mariadb

print("Content-Type:text/html")
print()

print("<h1>Welcome to Python</h1>")
print("<hr/>")
print("<h1>Using input tag</h1>")
print("<body bgcolor='blue'>")

form=cgi.FieldStorage() 

class TP:
    fields = {}
    def __init__():
        nombre = form.getvalue("nombre")
        apellido1 = form.getvalue("apellido1")
        apellido2 = form.getvalue("apellido2")
        rfc = form.getvalue("rfc")
        calle = form.getvalue("calle")
        numero = form.getvalue("numero")
        colonia = form.getvalue("colonia")
        cp = form.getvalue("cp")
    def mark_fields(self, field):
        if field != None: 
            self.field.append(field)
    mark_fields(nombre)
    mark_fields(apellido1)
    mark_fields(apellido2)
    mark_fields(rfc)
    mark_fields(calle)
    mark_fields(numero)
    mark_fields(colonia)
    mark_fields(cp)

    

    
    

#Possible queries
query_select = ("INSERT INTO events(id, title, description) VALUES(%s, %s, %s)")
query_insert = ("INSERT INTO events(id, title, description) VALUES(%s, %s, %s)")
query_create_table= ("INSERT INTO events(id, title, description) VALUES(%s, %s, %s)")
query_create_database = ("INSERT INTO events(id, title, description) VALUES(%s, %s, %s)")

# Connect to Database
try:
    conn1 = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="sucursal1"
    )
    conn2 = mysql.connector.connect(
        user ="root",
        password="",
        host="localhost",
        database="sucursal2"
    )
# Get Cursor
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("<h2>Something is wrong with your username or password, ask for a user</h2>")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("<h1>Database does not exist</h1>")
    else:
            print(err)

else:
    cur1.close()
    cur2.close()
    conn1.close()
    conn2.close()

print("<h3>record inserted successfully<h3>")
print("<a href='http://localhost/testing/index.php'>click here to go back</a>")