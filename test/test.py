#!/usr/bin/env python3

import mysql.connector
from mysql.connector import errorcode
import sys
import cgi
import mariadb
from string import Template

print("Content-Type:text/html")
print()

print("<h1>Welcome to Python</h1>")
print("<hr/>")
print("<h1>Using input tag</h1>")
print("<body bgcolor='blue'>")

form=cgi.FieldStorage() 
fields = {"nombre": form.getvalue("nombre"),
            "apellido1" : form.getvalue("apellido1"),
            "apellido2" : form.getvalue("apellido2"),
            "rfc" : form.getvalue("rfc"),
            "calle" : form.getvalue("calle"),
            "numero" : form.getvalue("numero"),
            "colonia" : form.getvalue("colonia"),
            "cp" : form.getvalue("cp")}

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

    def TP(tipo,fields=fields):
        def mark_fields(field):
            if fields[field] == None: 
                fields.pop(field)
        for key in fields:
            mark_fields(key)
        
        if tipo=="SELECT":
            llaves = fields.keys()
            valores = fields.values()
            query = ("SELECT * FROM cliente WHERE " + str(llaves[0])+"="+str(valores[0]))
            return(query)
        elif tipo=="INSTERT":
            llaves = fields.keys()
            valores = fields.values()
            query1 = ("INSERT INTO clientes(nombre, apellido1, apellido2, rfc) VALUES(%s, %s, %s, %s)")
            ids1 = list(cur1.excecute("SELECT id_cliente FROM cliente"))
            ids2 = list(cur2.excecute("SELECT id_cliente FROM cliente"))
            cur1.commit()
            cur2.coomit()
            ids = max(ids1+ids2)
            valores.append(ids)
            vals1 = valores[0:4]
            vals2 = valores[4:]
            query2 = ("INSERT INTO direcciones(calle,numero,colonia,cp,id_cliente) VALUES(%s, %s, %s,%i)") 
            return(query1, vals1, query2, vals2)
        return()

    def DP(tipo):#en sucursal1-->impares en sucursal2-->pares
        if tipo=="SELECT":
            query = TP("SELECT")
            sucursal1 = cur1.excecute(query)
            sucursal2 = cur2.excecute(query)
            cur1.commit()
            cur2.commit()
            print("<h3>Para la sucursal de Morelia: </h3")
            print(sucursal1)
            print("<h3>Para la sucursal de Pátzcuaro: </h3")
            print(sucursal2)
            print("<a href='http://localhost/testing/index.php'>Da click para regresar al inicio</a>")
            
        elif tipo=="INSERT":
            query1,valores1,query2,valores2 = TP("INSERT")
            ids1 = list(cur1.excecute("SELECT id_cliente FROM cliente"))
            ids2 = list(cur2.excecute("SELECT id_cliente FROM cliente"))
            if len(ids1) > len(ids2):
                cur2.excecute(query1,valores1)
                cur2.excecute(query2,valores2)
                cur2.commit()
            else:
                cur1.excecute(query1,valores1)
                cur1.excecute(query2,valores2)
                cur1.commit()
    
    if form['submit_button'] == 'BUSCAR':
        DP("SELECT")
    elif form['submit_button'] == "CREAR CLIENTE":
        DP("INSERT")
        print("<h3>record inserted successfully<h3>")
        print("<a href='http://localhost/testing/index.php'>Da click para regresar al inicio</a>")


#query_create_table= ("INSERT INTO events(id, title, description) VALUES(%s, %s, %s)")
#query_create_database = ("INSERT INTO events(id, title, description) VALUES(%s, %s, %s)")

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
