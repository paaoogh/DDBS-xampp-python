#!/usr/local/bin python3.9
# -*- coding: utf-8 -*-

import mariadb
import tkinter as tk
from tkinter import *
import PIL
import json
import time

#________________________GENERAL QUERIES____________________
with open("queries.json") as json_file:
        que = json.load(json_file)

def CREATE_DB(usuario, passw, ciudad): #en caso de que no exista la base de datos
    conn = mariadb.connect(user=usuario,password=passw,host="localhost")
    curs = conn.cursor()
    curs.execute(que["creation"]+ciudad+";")
    conn.close()
    return

def CREATE_TABLES(usuario,passw,database): #en caso de que no exista la base de datos
    conn = mariadb.connect(host="localhost", user=usuario,password=passw)
    curs = conn.cursor()
    curs.execute("USE "+database+";")
    curs.execute(que["clientes"])
    curs.execute(que["direcciones"])
    conn.close()
    return


#____________________INSTALACIÓN________________
print("BIENVENIDO A LA INSTALACIÓN DEL SISTEMA PARA SUCURSALES:")
s = input("¿Cuenta ya con la base de datos[S/N]: ")
if s=="N" or s=="n":
    print("Asegúrece de tener el usuario y contraseña del equipo de TI.")
    usuario = str(input("Usuario: "))
    passw = str(input("Contraseña: "))
    print("Un momento...")
    time.sleep(2)
    print("Creando base de datos...")
    time.sleep(4)
    CREATE_DB(usuario,passw," Morelia")
    CREATE_DB(usuario,passw," Patzcuaro")
    print("Generando tablas...")
    time.sleep(5)
    CREATE_TABLES(usuario,passw,"Morelia")
    CREATE_TABLES(usuario,passw,"Patzcuaro")
    print("Accedediendo al sistema...")
    time.sleep(6)
    print("Bienvenido")
    time.sleep(3)
elif s=="S" or s=="s":
    print("Bienvenido.")
    time.sleep(3)

def submitact(): 
    user = Username.get() 
    passw = password.get() 
    print(f"Ingresó el usuario {user} {passw} para la base de datos") 
    logintodb(user, passw)

#____________________LOGIN_____________________
def logintodb(user, passw):
    usuario = user
    contra = passw

    def limpiar_db(): #delete input of form
        dn= n.delete('0',END)
        da1= a1.delete('0',END)
        da2= a2.delete('0',END)
        dr= r.delete('0',END)
        dca= ca.delete('0',END)
        dnum= num.delete('0',END)
        dcol= col.delete('0',END)
        dcp= cp.delete('0',END)

    def dest1():
        consulta.destroy()
    
    def get_tables(): #Get all the tables in the distributed system
        conector = mariadb.connect(host="localhost",user=usuario,password=contra,database="information_schema")
        cur = conector.cursor()
        query_m = "SELECT table_schema, table_name, column_name, column_key FROM COLUMNS WHERE table_schema='Morelia' or table_schema='Patzcuaro';"
        cur.execute(query_m)
        datos = cur.fetchall()
        tablas = {}
        for i in datos:
            if i[1] not in tablas.keys():
                tablas[i[1]] = [i[2]]
            elif i[1] in tablas.keys() and i[2] not in tablas.get(i[1]):
                lista = tablas.get(i[1])
                lista.append(i[2])
                tablas[i[1]] = lista
        return tablas

    def buscar_DP(): #fragmentation of query for select
        nom = n.get()
        apellido1 = a1.get()
        apellido2 = a2.get()
        RFC = r.get()
        calle = ca.get()
        numero = num.get()
        colonia = col.get()
        CP = cp.get()
        datos = [nom,apellido1,apellido2,RFC,calle,numero,colonia,CP]
        try:
            if int(CP) >=61000:
                buscar_TP("Patzcuaro",datos)
            elif int(CP)<61000:
                buscar_TP("Morelia",datos)
        except: 
            buscar_TP("ambos",datos)
        return

    def buscar_TP(datab,datos): #
        cnx = mariadb.connect(host="localhost",user=usuario,password=contra,database="Morelia")
        cnx2 = mariadb.connect(host="localhost",user=usuario,password=contra,database="Patzcuaro")
        conn = cnx.cursor()
        conn2 = cnx2.cursor()
        datitos = [datos[0],datos[3],datos[4],datos[5],datos[6]]

        query = "SELECT * FROM cliente LEFT JOIN direcciones ON cliente.rfc=direcciones.rfc WHERE cliente.nombre=%s or cliente.rfc=%s UNION SELECT * FROM direcciones RIGHT JOIN cliente ON direcciones.rfc=cliente.rfc where direcciones.calle=%s or direcciones.numero=%s or direcciones.colonia=%s;"
        if datab== "Morelia":
            conn.execute(query,datitos)
            filas = conn.fetchall()

            class Table: #made for displaying in table form all the registries
                def __init__(self,root): 
                    for i in range(total_rows): 
                        for j in range(total_columns):    
                            self.e = Entry(root, width=20, fg='blue', 
                                        font=('Arial',16,'bold')) 
                            self.e.grid(row=i, column=j) 
                            self.e.insert(END, filas[i][j])  
            total_rows = len(filas) 
            total_columns = len(filas[0]) 
            consulta = Tk()
            t = Table(consulta) 
            consulta.mainloop()
            
        elif datab=="Patzcuaro":
            conn2.execute(query,datitos)
            filas = conn2.fetchall()

            class Table: 
                def __init__(self,root): 
                    for i in range(total_rows): 
                        for j in range(total_columns):    
                            self.e = Entry(root, width=20, fg='blue', 
                                        font=('Arial',16,'bold')) 
                            self.e.grid(row=i, column=j) 
                            self.e.insert(END, filas[i][j])  
            total_rows = len(filas) 
            total_columns = len(filas[0]) 
            consulta = Tk() 
            t = Table(consulta) 
            consulta.mainloop()
        elif datab=="ambos": #in case no ZIP CODE is provided
            conn.execute(query,datitos)
            conn2.execute(query,datitos)
            filas1 = conn.fetchall()
            filas2 = conn2.fetchall()
            filas = filas1+filas2
            print(filas)

            class Table: 
                def __init__(self,root): 
                    for i in range(total_rows): 
                        for j in range(total_columns):    
                            self.e = Entry(root, width=20, fg='blue', 
                                        font=('Arial',16,'bold')) 
                            self.e.grid(row=i, column=j) 
                            self.e.insert(END, filas[i][j])  
            total_rows = len(filas) 
            total_columns = len(filas[0]) 
            consulta = Tk() 
            t = Table(consulta) 
            consulta.mainloop()

        cnx.close()
        cnx2.close()
        return

    def insertar_DP(): #fragmentation of query for Insert
        nom = n.get()
        apellido1 = a1.get()
        apellido2 = a2.get()
        RFC = r.get()
        calle = ca.get()
        numero = num.get()
        colonia = col.get()
        CP = int(cp.get())
        datos = [nom,apellido1,apellido2,RFC,calle,numero,colonia,CP]
        if CP>=61000:
            insertar_TP("Patzcuaro",datos)
        else:
            insertar_TP("Morelia",datos)
        return

    def insertar_TP(datab,datos):
        datos1 = (datos[0],datos[1],datos[2],datos[3])
        datos2 = (datos[4],datos[5],datos[6],datos[7],datos[3])
        cnx = mariadb.connect(host="localhost",user=usuario,password=contra,database=datab)
        conn = cnx.cursor()
        query1 = "INSERT INTO cliente VALUES(%s,%s,%s,%s)"
        query2 = "INSERT INTO direcciones(calle,numero,colonia,cp,rfc) VALUES(%s,%s,%s,%s,%s)"
        conn.execute(query1,datos1)
        conn.execute(query2,datos2)
        cnx.commit()
        cnx.close()

        return

    def cambiar_DP(): #fragmentation for update registries
        nom = n.get()
        apellido1 = a1.get()
        apellido2 = a2.get()
        RFC = r.get()
        calle = ca.get()
        numero = num.get()
        colonia = col.get()
        CP = cp.get()
        datos = [nom,apellido1,apellido2,RFC,calle,numero,colonia,CP]
        datos1 = (datos[0],datos[1],datos[2],datos[3])
        datos2 = (datos[4],datos[5],datos[6],datos[7],datos [3])
        query_up = "UPDATE cliente SET nombre = %s , apellido1 = %s ,apellido2 = %s WHERE rfc = %s ;"
        queryD = "UPDATE direcciones SET calle = %s, numero = %s, colonia = %s, cp = %s WHERE rfc = %s"
 
        if int(CP) >= 61000:
            cambiar_TP("Patzcuaro",query_up, queryD, datos1, datos2)
        elif int(CP) < 61000:
            cambiar_TP("Morelia",query_up, queryD, datos1, datos2)
        return
    
    def cambiar_TP(datab, q1, q2, d1, d2):
        cnx = mariadb.connect(host="localhost",user=usuario,password=contra,database=datab)
        conn = cnx.cursor()
        conn.execute(q1,d1)
        conn.execute(q2,d2)
        cnx.commit()
        cnx.close()
        return   
    
    def crear_ventana(): #Creating a table for up to 4 new columns (plus the keys)
        def crear_DP(): #creation of real query based on the form bellow
            nombre_tabla = name.get()
            uno = one.get()
            t1 = tipo1.get()
            dos = two.get()
            t2 = tipo2.get()
            tres = three.get()
            t3 = tipo3.get()
            cuatro = four.get()
            t4 = tipo4.get()
            data = [uno,t1,dos,t2,tres,t3,cuatro,t4]
            datos = {}

            for i in range(len(data)): 
                if data[i] =="1" or data[i]=="2" or data[i]=="3" or data[i]=="": #adding datatype
                    continue
                elif i!= len(data)-1:
                    if data[i+1] == "1":
                        datos[data[i]] = " INTEGER,"
                    elif data[i+1] == "2":
                        datos[data[i]] = " FLOAT,"
                    elif data[i+1] == "3":
                        datos[data[i]] = " VARCHAR(21800) CHARACTER SET utf8 COLLATE utf8_spanish_ci,"

            #This part is for query construction
            Query = "CREATE TABLE "+ str(nombre_tabla)+" (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, rfc VARCHAR(13) NOT NULL, "
            foreign = "FOREIGN KEY (rfc) REFERENCES cliente(rfc));"
            for i in range(len(datos.keys())): #cre
                cad = list(datos.keys())
                cad = str(cad[i]) + datos[cad[i]]
                Query += cad
            Query += foreign

            crear_TP(Query)     
            return

        def crear_TP(Query):
            cnx = mariadb.connect(host="localhost",user=usuario,password=contra,database="Morelia")
            cnx2 = mariadb.connect(host="localhost",user=usuario,password=contra,database="Patzcuaro")
            conn = cnx.cursor()
            conn2 = cnx2.cursor()
            conn.execute(Query)
            conn2.execute(Query)
            cnx.commit()
            cnx2.commit()
            cnx.close()
            cnx2.close()

            #This part is for the user as they have to refresh the system
            def dest():
                warning.destroy()
                dest2()
                dest1()
            
            warning = tk.Tk()
            warning.geometry("700x150")
            T = tk.Text(warning, height=10)
            T.insert(tk.END, "CIERRE E INICIE EL SISTEMA PARA REFLEJAR LOS CAMBIOS")
            T.place(x=50, y=30)
            yes = tk.Button(warning, text="Aceptar",
                                bg ='peach puff', command=dest)
            yes.place(x=200, y=115, width=100)
            warning.mainloop()

            return
        def dest2():
            new_table.destroy()
            return
        #Form of the new table about to be created
        new_table = tk.Tk()
        new_table.geometry("800x400")
        F = tk.Canvas(new_table, bg="blue", height=550,width=600)

        nemu = tk.Label(new_table, text="NOMBRE DE LA TABLA NUEVA: *")
        nemu.place(x=30, y = 150)
        name = tk.Entry(new_table, width=100)
        name.place(x = 255, y=150, width=100 )
        
        first = tk.Label(new_table, text="Nuevo campo: *")
        first.place(x=30, y = 20)
        one = tk.Entry(new_table, width=100)
        one.place(x = 135, y=20, width=100 )
        caja = tk.Label(new_table, text="Tipo de dato: *")
        caja.place(x=250, y=20, width=100)
        tipo1 = tk.Entry(new_table, width=100)
        tipo1.place(x=350, y=20, width=100)

        second = tk.Label(new_table, text="Nuevo campo: *")
        second.place(x=30, y = 50)
        two = tk.Entry(new_table, width=100)
        two.place(x = 135, y=50, width=100 )
        caja2 = tk.Label(new_table, text="Tipo de dato: *")
        caja2.place(x=250, y=50, width=100)
        tipo2 = tk.Entry(new_table, width=100)
        tipo2.place(x=350, y=50, width=100)

        third = tk.Label(new_table, text="Nuevo campo: *")
        third.place(x=30, y = 80)
        three = tk.Entry(new_table, width=100)
        three.place(x = 135, y=80, width=100 )
        caja3 = tk.Label(new_table, text="Tipo de dato: *")
        caja3.place(x=250, y=80, width=100)
        tipo3 = tk.Entry(new_table, width=100)
        tipo3.place(x=350, y=80, width=100)

        fourth = tk.Label(new_table, text="Nuevo campo: *")
        fourth.place(x=30, y = 110)
        four = tk.Entry(new_table, width=100)
        four.place(x = 135, y=110, width=100 )
        caja4 = tk.Label(new_table, text="Tipo de dato: *")
        caja4.place(x=250, y=110, width=100)
        tipo4 = tk.Entry(new_table, width=100)
        tipo4.place(x=350, y=110, width=100)

        T = tk.Text(new_table, height=10, width=100)
        T.insert(tk.END, "Los nuevos datos pueden ser de tipo 1 (números enteros), 2 (decimales) y 3 (texto)")
        T.place(x=30, y=200)

        creacion= tk.Button(new_table, text="Crear",
                        bg ='peach puff', command=crear_DP)
        creacion.place(x=130, y=305, width=250)
        new_table.mainloop()

        return 
    
    tablas = get_tables() #need this in orther to know what interface to display
    if len(list(tablas.keys()))==2: #This is the original interface: without new tables introduced by user
        try:
            consulta = tk.Tk()
            root.destroy()
            consulta.geometry("800x500")
            consulta.title("Ingreso de datos")
            D = tk.Canvas(consulta, bg ="blue", height = 550, width = 600)

            lblfrstrow = tk.Label(consulta, text ="Nombre:" ) 
            lblfrstrow.place(x = 30, y = 20) 
            n = tk.Entry(consulta, width = 100) 
            n.place(x = 105, y = 20, width = 100)

            second = tk.Label(consulta, text ="Apellido paterno: " ) 
            second.place(x = 250, y = 20) 
            a1 = tk.Entry(consulta, width = 200) 
            a1.place(x = 360, y = 20, width = 100)

            second = tk.Label(consulta, text ="Apellido materno: " ) 
            second.place(x = 480, y = 20) 
            a2 = tk.Entry(consulta, width = 100) 
            a2.place(x = 600, y = 20, width = 100)

            third = tk.Label(consulta, text ="RFC: " ) 
            third.place(x = 30, y = 50) 
            r = tk.Entry(consulta, width = 35) 
            r.place(x = 105, y = 50, width = 100)

            fourth = tk.Label(consulta, text ="Calle: " ) 
            fourth.place(x = 30, y = 100) 
            ca = tk.Entry(consulta, width = 50) 
            ca.place(x = 100, y = 100, width = 100)

            fifth = tk.Label(consulta, text ="Número: " ) 
            fifth.place(x = 260, y = 100) 
            num = tk.Entry(consulta, width = 100) 
            num.place(x = 320, y = 100, width = 50)

            sixth = tk.Label(consulta, text ="Colonia: " ) 
            sixth.place(x = 400, y = 100) 
            col = tk.Entry(consulta, width = 200) 
            col.place(x = 460, y = 100, width = 150)

            seven = tk.Label(consulta, text ="Código Postal: " ) 
            seven.place(x = 30, y = 140) 
            cp = tk.Entry(consulta, width = 100) 
            cp.place(x = 150, y = 140, width =50)

            #Botones..........................

            buscar = tk.Button(consulta, text ="Buscar",  
                        bg ='peach puff', command = buscar_DP) 
            buscar.place(x = 190, y = 385, width = 100)

            insertar = tk.Button(consulta, text ="Insertar",  
                        bg ='peach puff', command = insertar_DP) 
            insertar.place(x = 465, y = 385, width = 100) 

            actualizar = tk.Button(consulta, text ="Actualizar datos",  
                        bg ='peach puff', command = cambiar_DP) 
            actualizar.place(x = 390, y = 425, width = 250) 

            limpiar= tk.Button(consulta, text ="Limpiar datos",  
                            bg ='peach puff', command=limpiar_db)
            limpiar.place(x = 115, y = 425, width = 250)

            crear_tabla = tk.Button(consulta, text="Crear tabla",
                            bg ='peach puff', command=crear_ventana)
            crear_tabla.place(x=253, y=465, width=250)


            consulta.mainloop()
        except:
            print("An error ocurred...")

    else: #Once user has interacted with interface
        if len(tablas[list(tablas.keys())[-1]])==6: #four columns
            ultima = list(tablas.keys())[-1]
            valores = tablas[ultima]
            try:
                consulta = tk.Tk()
                root.destroy()
                consulta.geometry("800x500")
                consulta.title("Ingreso de datos")
                D = tk.Canvas(consulta, bg ="blue", height = 550, width = 600)

                lblfrstrow = tk.Label(consulta, text ="Nombre:" ) 
                lblfrstrow.place(x = 30, y = 20) 
                n = tk.Entry(consulta, width = 100) 
                n.place(x = 105, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido paterno: " ) 
                second.place(x = 250, y = 20) 
                a1 = tk.Entry(consulta, width = 200) 
                a1.place(x = 360, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido materno: " ) 
                second.place(x = 480, y = 20) 
                a2 = tk.Entry(consulta, width = 100) 
                a2.place(x = 600, y = 20, width = 100)

                third = tk.Label(consulta, text ="RFC: " ) 
                third.place(x = 30, y = 50) 
                r = tk.Entry(consulta, width = 35) 
                r.place(x = 105, y = 50, width = 100)

                fourth = tk.Label(consulta, text ="Calle: " ) 
                fourth.place(x = 30, y = 100) 
                ca = tk.Entry(consulta, width = 50) 
                ca.place(x = 100, y = 100, width = 100)

                fifth = tk.Label(consulta, text ="Número: " ) 
                fifth.place(x = 260, y = 100) 
                num = tk.Entry(consulta, width = 100) 
                num.place(x = 320, y = 100, width = 50)

                sixth = tk.Label(consulta, text ="Colonia: " ) 
                sixth.place(x = 400, y = 100) 
                col = tk.Entry(consulta, width = 200) 
                col.place(x = 460, y = 100, width = 150)

                seven = tk.Label(consulta, text ="Código Postal: " ) 
                seven.place(x = 30, y = 140) 
                cp = tk.Entry(consulta, width = 100) 
                cp.place(x = 150, y = 140, width =50)

                eight = tk.Label(consulta, text =valores[2] ) 
                eight.place(x = 30, y = 180) 
                t8 = tk.Entry(consulta, width = 100) 
                t8.place(x = 150, y = 180, width =50)

                nine = tk.Label(consulta, text =valores[3] ) 
                nine.place(x = 30, y = 210) 
                t9 = tk.Entry(consulta, width = 100) 
                t9.place(x = 150, y = 210, width =50)

                ten = tk.Label(consulta, text =valores[4] ) 
                ten.place(x = 30, y = 230) 
                t10 = tk.Entry(consulta, width = 100) 
                t10.place(x = 150, y = 230, width =50)

                eleven = tk.Label(consulta, text =valores[5] ) 
                eleven.place(x = 30, y = 250) 
                t11 = tk.Entry(consulta, width = 100) 
                t11.place(x = 150, y = 250, width =50)


                #Botones..........................

                buscar = tk.Button(consulta, text ="Buscar",  
                            bg ='peach puff', command = buscar_DP) 
                buscar.place(x = 190, y = 385, width = 100)

                insertar = tk.Button(consulta, text ="Insertar",  
                            bg ='peach puff', command = insertar_DP) 
                insertar.place(x = 465, y = 385, width = 100) 

                actualizar = tk.Button(consulta, text ="Actualizar datos",  
                            bg ='peach puff', command = cambiar_DP) 
                actualizar.place(x = 390, y = 425, width = 250) 

                limpiar= tk.Button(consulta, text ="Limpiar datos",  
                                bg ='peach puff', command=limpiar_db)
                limpiar.place(x = 115, y = 425, width = 250)

                crear_tabla = tk.Button(consulta, text="Crear tabla",
                                bg ='peach puff', command=crear_ventana)
                crear_tabla.place(x=253, y=465, width=250)


                consulta.mainloop()
            except:
                print("An error ocurred: 1")

        elif len(tablas[list(tablas.keys())[-1]])==5: #3 columns
            ultima = list(tablas.keys())[-1]
            valores = tablas[ultima]
            try:
                consulta = tk.Tk()
                root.destroy()
                consulta.geometry("800x500")
                consulta.title("Ingreso de datos")
                D = tk.Canvas(consulta, bg ="blue", height = 550, width = 600)

                lblfrstrow = tk.Label(consulta, text ="Nombre:" ) 
                lblfrstrow.place(x = 30, y = 20) 
                n = tk.Entry(consulta, width = 100) 
                n.place(x = 105, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido paterno: " ) 
                second.place(x = 250, y = 20) 
                a1 = tk.Entry(consulta, width = 200) 
                a1.place(x = 360, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido materno: " ) 
                second.place(x = 480, y = 20) 
                a2 = tk.Entry(consulta, width = 100) 
                a2.place(x = 600, y = 20, width = 100)

                third = tk.Label(consulta, text ="RFC: " ) 
                third.place(x = 30, y = 50) 
                r = tk.Entry(consulta, width = 35) 
                r.place(x = 105, y = 50, width = 100)

                fourth = tk.Label(consulta, text ="Calle: " ) 
                fourth.place(x = 30, y = 100) 
                ca = tk.Entry(consulta, width = 50) 
                ca.place(x = 100, y = 100, width = 100)

                fifth = tk.Label(consulta, text ="Número: " ) 
                fifth.place(x = 260, y = 100) 
                num = tk.Entry(consulta, width = 100) 
                num.place(x = 320, y = 100, width = 50)

                sixth = tk.Label(consulta, text ="Colonia: " ) 
                sixth.place(x = 400, y = 100) 
                col = tk.Entry(consulta, width = 200) 
                col.place(x = 460, y = 100, width = 150)

                seven = tk.Label(consulta, text ="Código Postal: " ) 
                seven.place(x = 30, y = 140) 
                cp = tk.Entry(consulta, width = 100) 
                cp.place(x = 150, y = 140, width =50)

                eight = tk.Label(consulta, text =valores[2] ) 
                eight.place(x = 30, y = 180) 
                t8 = tk.Entry(consulta, width = 100) 
                t8.place(x = 150, y = 180, width =50)

                nine = tk.Label(consulta, text =valores[3] ) 
                nine.place(x = 30, y = 210) 
                t9 = tk.Entry(consulta, width = 100) 
                t9.place(x = 150, y = 210, width =50)

                ten = tk.Label(consulta, text =valores[4] ) 
                ten.place(x = 30, y = 230) 
                t10 = tk.Entry(consulta, width = 100) 
                t10.place(x = 150, y = 230, width =50)

                #Botones..........................

                buscar = tk.Button(consulta, text ="Buscar",  
                            bg ='peach puff', command = buscar_DP) 
                buscar.place(x = 190, y = 385, width = 100)

                insertar = tk.Button(consulta, text ="Insertar",  
                            bg ='peach puff', command = insertar_DP) 
                insertar.place(x = 465, y = 385, width = 100) 

                actualizar = tk.Button(consulta, text ="Actualizar datos",  
                            bg ='peach puff', command = cambiar_DP) 
                actualizar.place(x = 390, y = 425, width = 250) 

                limpiar= tk.Button(consulta, text ="Limpiar datos",  
                                bg ='peach puff', command=limpiar_db)
                limpiar.place(x = 115, y = 425, width = 250)

                crear_tabla = tk.Button(consulta, text="Crear tabla",
                                bg ='peach puff', command=crear_ventana)
                crear_tabla.place(x=253, y=465, width=250)


                consulta.mainloop()
            except:
                print("An error ocurred: 1")

        elif len(tablas[list(tablas.keys())[-1]])==4: #2 columns
            ultima = list(tablas.keys())[-1]
            valores = tablas[ultima]
            try:
                consulta = tk.Tk()
                root.destroy()
                consulta.geometry("800x500")
                consulta.title("Ingreso de datos")
                D = tk.Canvas(consulta, bg ="blue", height = 550, width = 600)

                lblfrstrow = tk.Label(consulta, text ="Nombre:" ) 
                lblfrstrow.place(x = 30, y = 20) 
                n = tk.Entry(consulta, width = 100) 
                n.place(x = 105, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido paterno: " ) 
                second.place(x = 250, y = 20) 
                a1 = tk.Entry(consulta, width = 200) 
                a1.place(x = 360, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido materno: " ) 
                second.place(x = 480, y = 20) 
                a2 = tk.Entry(consulta, width = 100) 
                a2.place(x = 600, y = 20, width = 100)

                third = tk.Label(consulta, text ="RFC: " ) 
                third.place(x = 30, y = 50) 
                r = tk.Entry(consulta, width = 35) 
                r.place(x = 105, y = 50, width = 100)

                fourth = tk.Label(consulta, text ="Calle: " ) 
                fourth.place(x = 30, y = 100) 
                ca = tk.Entry(consulta, width = 50) 
                ca.place(x = 100, y = 100, width = 100)

                fifth = tk.Label(consulta, text ="Número: " ) 
                fifth.place(x = 260, y = 100) 
                num = tk.Entry(consulta, width = 100) 
                num.place(x = 320, y = 100, width = 50)

                sixth = tk.Label(consulta, text ="Colonia: " ) 
                sixth.place(x = 400, y = 100) 
                col = tk.Entry(consulta, width = 200) 
                col.place(x = 460, y = 100, width = 150)

                seven = tk.Label(consulta, text ="Código Postal: " ) 
                seven.place(x = 30, y = 140) 
                cp = tk.Entry(consulta, width = 100) 
                cp.place(x = 150, y = 140, width =50)

                eight = tk.Label(consulta, text =valores[2] ) 
                eight.place(x = 30, y = 180) 
                t8 = tk.Entry(consulta, width = 100) 
                t8.place(x = 150, y = 180, width =50)

                nine = tk.Label(consulta, text =valores[3] ) 
                nine.place(x = 30, y = 210) 
                t9 = tk.Entry(consulta, width = 100) 
                t9.place(x = 150, y = 210, width =50)

                #Botones..........................

                buscar = tk.Button(consulta, text ="Buscar",  
                            bg ='peach puff', command = buscar_DP) 
                buscar.place(x = 190, y = 385, width = 100)

                insertar = tk.Button(consulta, text ="Insertar",  
                            bg ='peach puff', command = insertar_DP) 
                insertar.place(x = 465, y = 385, width = 100) 

                actualizar = tk.Button(consulta, text ="Actualizar datos",  
                            bg ='peach puff', command = cambiar_DP) 
                actualizar.place(x = 390, y = 425, width = 250) 

                limpiar= tk.Button(consulta, text ="Limpiar datos",  
                                bg ='peach puff', command=limpiar_db)
                limpiar.place(x = 115, y = 425, width = 250)

                crear_tabla = tk.Button(consulta, text="Crear tabla",
                                bg ='peach puff', command=crear_ventana)
                crear_tabla.place(x=253, y=465, width=250)


                consulta.mainloop()
            except:
                print("An error ocurred: 2")

        elif len(tablas[list(tablas.keys())[-1]])==3:#1 column
            ultima = list(tablas.keys())[-1]
            valores = tablas[ultima]
            try:
                consulta = tk.Tk()
                root.destroy()
                consulta.geometry("800x500")
                consulta.title("Ingreso de datos")
                D = tk.Canvas(consulta, bg ="blue", height = 550, width = 600)

                lblfrstrow = tk.Label(consulta, text ="Nombre:" ) 
                lblfrstrow.place(x = 30, y = 20) 
                n = tk.Entry(consulta, width = 100) 
                n.place(x = 105, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido paterno: " ) 
                second.place(x = 250, y = 20) 
                a1 = tk.Entry(consulta, width = 200) 
                a1.place(x = 360, y = 20, width = 100)

                second = tk.Label(consulta, text ="Apellido materno: " ) 
                second.place(x = 480, y = 20) 
                a2 = tk.Entry(consulta, width = 100) 
                a2.place(x = 600, y = 20, width = 100)

                third = tk.Label(consulta, text ="RFC: " ) 
                third.place(x = 30, y = 50) 
                r = tk.Entry(consulta, width = 35) 
                r.place(x = 105, y = 50, width = 100)

                fourth = tk.Label(consulta, text ="Calle: " ) 
                fourth.place(x = 30, y = 100) 
                ca = tk.Entry(consulta, width = 50) 
                ca.place(x = 100, y = 100, width = 100)

                fifth = tk.Label(consulta, text ="Número: " ) 
                fifth.place(x = 260, y = 100) 
                num = tk.Entry(consulta, width = 100) 
                num.place(x = 320, y = 100, width = 50)

                sixth = tk.Label(consulta, text ="Colonia: " ) 
                sixth.place(x = 400, y = 100) 
                col = tk.Entry(consulta, width = 200) 
                col.place(x = 460, y = 100, width = 150)

                seven = tk.Label(consulta, text ="Código Postal: " ) 
                seven.place(x = 30, y = 140) 
                cp = tk.Entry(consulta, width = 100) 
                cp.place(x = 150, y = 140, width =50)

                eight = tk.Label(consulta, text =valores[2] ) 
                eight.place(x = 30, y = 180) 
                t8 = tk.Entry(consulta, width = 100) 
                t8.place(x = 150, y = 180, width =50)

                #Botones..........................

                buscar = tk.Button(consulta, text ="Buscar",  
                            bg ='peach puff', command = buscar_DP) 
                buscar.place(x = 190, y = 385, width = 100)

                insertar = tk.Button(consulta, text ="Insertar",  
                            bg ='peach puff', command = insertar_DP) 
                insertar.place(x = 465, y = 385, width = 100) 

                actualizar = tk.Button(consulta, text ="Actualizar datos",  
                            bg ='peach puff', command = cambiar_DP) 
                actualizar.place(x = 390, y = 425, width = 250) 

                limpiar= tk.Button(consulta, text ="Limpiar datos",  
                                bg ='peach puff', command=limpiar_db)
                limpiar.place(x = 115, y = 425, width = 250)

                crear_tabla = tk.Button(consulta, text="Crear tabla",
                                bg ='peach puff', command=crear_ventana)
                crear_tabla.place(x=253, y=465, width=250)


                consulta.mainloop()
            except:
                print("An error ocurred: 3")
               


#Inicial interface
root = tk.Tk() 
root.geometry("300x300") 
root.title("Registro a Base de Datos")

C = tk.Canvas(root, bg ="blue", height = 250, width = 300)
lblfrstrow = tk.Label(root, text ="Username -", ) 
lblfrstrow.place(x = 50, y = 20) 
Username = tk.Entry(root, width = 35) 
Username.place(x = 150, y = 20, width = 100) 

lblsecrow = tk.Label(root, text ="Contaseña -") 
lblsecrow.place(x = 50, y = 50)  
password = tk.Entry(root, width = 35) 
password.place(x = 150, y = 50, width = 100)

submitbtn = tk.Button(root, text ="Login",  
                      bg ='blue', command = submitact) 
submitbtn.place(x = 150, y = 135, width = 55) 

root.mainloop() 