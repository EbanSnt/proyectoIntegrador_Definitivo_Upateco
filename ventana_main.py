import calendar
import csv
import operator
import sys
import time
import tkinter as tk
from tkinter import ttk, CENTER, messagebox, RIGHT
from datetime import datetime
from tkcalendar import *
from PIL import Image, ImageTk
from vista_semanal1 import *
from vista_mensual import *
import mysql.connector
class Programa:

    def __init__(self):
        self.conn = mysql.connector.connect(user='root',
                password='123456',
                host='127.0.0.1',
                database='agenda_proyecto')
        
        consulta = """  
                        CREATE TABLE IF NOT EXISTS calendario(
                        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        fecha_creacion VARCHAR(20),
                        titulo VARCHAR(30),
                        fecha VARCHAR(20),
                        hora_inicio VARCHAR(10),
                        hora_fin VARCHAR(10),
                        importancia VARCHAR(15),
                        descripcion VARCHAR(80),
                        etiquetas VARCHAR(80)
                        )ENGINE=InnoDB;"""
        
        #consulta_prueba = """
        #SELECT * FROM calendario;
        #                            """
        
        self.cur = self.conn.cursor()
        self.cur.execute(consulta)
        #self.cur.execute(consulta_prueba)
        resultado = self.cur.fetchall()

        print(resultado)
        self.conn.commit()
        self.cur.close()
        #self.conn.close()

        self.principal()

    def label_fecha(self):
        """"Metodo que fija un reloj (como un label) en tiempo real, en la
        ventana principal"""
        dia = time.strftime("%d")
        mes = time.strftime("%m")
        year = time.strftime("%Y")
        hora = time.strftime("%H")
        minutos = time.strftime("%M")
        segundos = time.strftime("%S")
        self.label_reloj.config(text=f"{dia}/{mes}/{year} {hora}:{minutos}:{segundos}",font=("Helvetica",10))
        self.label_reloj.after(1000, self.label_fecha)

    def principal(self):
        self.root = tk.Tk()
        self.root.geometry("910x500+100+100")
        self.root.config(background="#000")
        self.root.resizable(False,False)
        self.root.title("Gestor de Eventos")
        icono = tk.PhotoImage(file="./images/icono.png")
        self.root.iconphoto(True, icono)
        self.imagen = Image.open("./images/imagen2.png")
        self.imagen = self.imagen.resize((90, 90))
        self.imagen_inicio = ImageTk.PhotoImage(self.imagen)
        tk.Label(self.root, image=self.imagen_inicio,background="#000").place(x=240, y=5)
        tk.Label(self.root,text="AGENDA DE EVENTOS",font=("times new roman", 35, "bold","underline"),
                 foreground="#fff",background="#000").place(x=350,y=15)

        contenedor_botones = tk.Frame(self.root,background="#BEBEBE",highlightbackground="white",
                                      highlightthickness=2)
        contenedor_botones.place(x=0,y=0,width=230,height=500)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.place(x=231, y=100, width=680, height=400)
        self.vista_mensual_frame = tk.Frame(self.tabs,background="#BEBEBE")
        self.vista_general = tk.Frame(self.tabs,background="#BEBEBE")
        ttk.Label(self.vista_general,text="Los eventos resaltados son importantes",background="#BEBEBE",
                  font=("times new roman", 11)).place(x=20,y=340)
        self.tabs.add(self.vista_general, text="   General ")
        #self.tabs.add(self.vista_mensual_frame,text=" Vista Mes Actual")
        ttk.Label(self.vista_mensual_frame,text="La vista se actualiza cada vez\nque se inicia el programa").place(x=100,y=330)


        # Calendario y sus configuraciones
        self.now = datetime.now()
        self.cal = Calendar(contenedor_botones, selectmode="day", year=self.now.year, month=self.now.month, day=self.now.day, locale="es",
                       background="black", disabledbackground="black", bordercolor="black",
                       headersbackground="black", normalbackground="black", foreground='white',
                       normalforeground='white', headersforeground='white',showweeknumbers=False,
                       showothermonthdays=False,weekendbackground = "Black",weekendforeground="white"

                       )
        self.cal.place(x=5,y=5,width=210,height=150)


        self.buscador_button = tk.Button(contenedor_botones, text="Buscar", command=self.buscar_evento,
                                         font=("times new roman", 11, "bold"))
        self.buscador_button.place(x=160,y=215)
        self.buscador_button.config(fg="white")
        self.buscador_button.config(bg="#000")

        self.buscador_input = ttk.Entry(self.root)
        self.buscador_input.place(x=20,y=220,height=27)
        tk.Label(text="Buscar por Etiquetas",background="#BEBEBE").place(x=25,y=250)

        self.vista_semanal_button = tk.Button(self.root, text="Vista\nSemanal", command=self.vista_semanal,
                                               font=("times new roman", 11, "bold"),height=4)
        self.vista_semanal_button.config(fg="#fff")
        self.vista_semanal_button.config(bg="blue")
        self.vista_semanal_button.place(x=155,y=285)

        # Boton que abre una ventana para agregar un evento
        self.agregar_evento_button = tk.Button(self.root, text="Agregar Evento", command=self.agregar_evento_ventana,
                                               font=("times new roman", 11, "bold"))
        self.agregar_evento_button.config(fg="white")
        self.agregar_evento_button.config(bg="#000")
        self.agregar_evento_button.place(x=20,y=285)

        # Boton que abre ventana para modificar los datos de un evento. Se insertan los
        # datos automaticamente, obtenidos de lo que se haya seleccionado en el TreeView
        self.modificar_evento_button = tk.Button(self.root, text="Modificar Evento",
                                                 command=self.modificar_evento_ventana
                                                 , font=("times new roman", 11, "bold"))
        self.modificar_evento_button.config(fg="white")
        self.modificar_evento_button.config(bg="#000")
        self.modificar_evento_button.place(x=20,y=325)
        # Boton que elmina un evento seleccionado del TreeView **
        self.eliminar_evento_button = tk.Button(self.root, text="Eliminar Evento", command=self.elmininar_evento
                                                , font=("times new roman", 11, "bold"))
        self.eliminar_evento_button.config(fg="white")
        self.eliminar_evento_button.config(bg="#000")
        self.eliminar_evento_button.place(x=20,y=365)
        # Boton que cierra el programa ***
        self.salir_button = tk.Button(self.root, text="Salir", command=lambda: sys.exit(),
                                      font=("times new roman", 11, "bold"))
        self.salir_button.config(fg="white")
        self.salir_button.config(bg="#d63031")
        self.salir_button.place(x=20,y=440)

        self.tabla_treeview_general()

        self.label_reloj = ttk.Label(self.root,text=f"Bienvenido",font=("Helvetica",10))
        self.label_reloj.place(x=90, y=445)
        self.label_reloj.after(1000,self.label_fecha)

        self.vista_mensual()
        self.eventos_del_mes()
        self.root.mainloop()

    def columnas_treeview(self):
        # Configuraciones de la tabla (Ancho de las columnas, titulo, centrado
        self.tabla.column("#1", width=40, anchor=CENTER)
        self.tabla.column("#2", width=80, anchor=CENTER)
        self.tabla.column("#3", width=80, anchor=CENTER)
        self.tabla.column("#4", width=45, anchor=CENTER)
        self.tabla.column("#5", width=45, anchor=CENTER)
        self.tabla.column("#6", width=85, anchor=CENTER)
        self.tabla.column("#7", width=110, anchor=CENTER)
        self.tabla.column("#8", width=80, anchor=CENTER)
        self.tabla.column("#9", width=70, anchor=CENTER)

        self.tabla["show"] = "headings"
        self.tabla.heading("#1", text="ID", anchor=CENTER)
        self.tabla.heading("#2", text="CREADO", anchor=CENTER)
        self.tabla.heading("#3", text="TITULO", anchor=CENTER)
        self.tabla.heading("#4", text="FECHA", anchor=CENTER)
        self.tabla.heading("#5", text="DESDE", anchor=CENTER)
        self.tabla.heading("#6", text="HASTA", anchor=CENTER)
        self.tabla.heading("#7", text="IMPORTANCIA", anchor=CENTER)
        self.tabla.heading("#8", text="DESCRIPCION", anchor=CENTER)
        self.tabla.heading("#9", text="ETIQUETAS", anchor=CENTER)

    def tabla_treeview_general(self):
        """Tabla que muestra los datos de los eventos. Obtenidos desde la tabla de MySQL"""
        self.tabla = ttk.Treeview(self.vista_general, height=15,
                                  columns=("#1","#2","#3","#4","#5","#6","#7","#8","#9"))
        self.tabla.place(x=0,y=0)
        cur = self.conn.cursor()
        consulta = """SELECT * FROM calendario;"""
        cur.execute(consulta)
        datos = cur.fetchall()

        self.columnas_treeview()
        for dato in datos:
                # Si la importancia del evento es "Importante" se cambiará el color de celda. Las "Normal
                # se mantienen tal cual
                if dato[6] == "Importante":
                    self.tabla.insert('', 0, values=(dato[0],dato[1],
                                                     dato[2],dato[3],dato[4],dato[5],
                                                     dato[6],dato[7],
                                                     dato[8]),tags=("color",))
                    self.tabla.tag_configure("color",background="#99f1f8")
                else:
                    self.tabla.insert('', 0, values=(dato[0],dato[1],
                                                     dato[2],dato[3],dato[4],dato[5],
                                                     dato[6],dato[7],
                                                     dato[8]))


    def eventos_del_mes(self):
        """Tabla que muestra los datos de los eventos del mes actual. Obtenidos desde el archivo agenda.csv"""
        with open("agenda.csv", "r") as archivo:
            agenda = []
            eventos = csv.reader(archivo)
            for linea in eventos:
                # Se omiten las lineas en blanco y las cabeceras
                if linea != [] and linea !=['Agendado', 'Titulo', 'Fecha', 'Hora Inicio', 'Hora Fin', 'Importancia', 'Descripcion', 'Etiquetas', 'Codigo']:
                    auxiliar = linea[2]
                    auxiliar2 = auxiliar.split("/")
                    dia = f"{int(auxiliar2[1])}"
                    mes_actual = f"{int(auxiliar2[1])}"
                    mes_actual_casteado = int(mes_actual)
                    year_actual = f"{int(auxiliar2[2])}"
                    if int(mes_actual_casteado) == int(self.now.month) and int(year_actual) == int(self.now.year):
                        agenda.append(linea)

        label = ""
        for i in agenda:
            a = f'Evento:{i[1]}\nFecha:{i[2]} {i[3]}-{i[4]} hs\nDescripcion:{i[6]}\n\n'
            label = label + a

        area = tk.Text(self.vista_mensual_frame)
        area.place(x=350, y=30, width=300, height=300)
        area.insert(0.0, f"Eventos del mes actual:\n\n{label}")
        area.config(state="disabled")


    def agregar_evento_ventana(self):
        """Metodo que abre una ventana para ingresar los datos de un nuevo evento"""
        dia = time.strftime("%d")
        mes = time.strftime("%m")
        year = time.strftime("%Y")
        hora = time.strftime("%H")
        minutos = time.strftime("%M")
        segundos = time.strftime("%S")
        self.evento_ventana = tk.Tk()
        self.evento_ventana.geometry("254x440+190+175")
        self.evento_ventana.resizable(False, False)
        self.evento_ventana.title("Agregar Evento")
        # Aqui estan todos los Entry con sus respectivos Label
        ttk.Label(self.evento_ventana,text="Agregar un Nuevo Evento",font=("Helvetica", 11, "underline"),justify="center").place(x=10,y=10)
        ttk.Label(self.evento_ventana,text="Titulo*",font=("Helvetica",10)).place(x=10,y=40)
        self.titulo_entry = ttk.Entry(self.evento_ventana)
        self.titulo_entry.place(x=10,y=60)

        ttk.Label(self.evento_ventana,text="Fecha (dd/mm/aaaa)*",font=("Helvetica",10)).place(x=10,y=85)
        self.fecha_entry = ttk.Entry(self.evento_ventana)
        self.fecha_entry.place(x=10,y=105)
        self.fecha_entry.insert(0,f"{dia}/{mes}/{year}")

        ttk.Label(self.evento_ventana,text="Hora Inicio*",font=("Helvetica",10)).place(x=10,y=130)
        self.hora_entry = ttk.Entry(self.evento_ventana)
        self.hora_entry.place(x=10,y=155)
        self.hora_entry.insert(0,f"{self.now.hour}:{minutos}")

        ttk.Label(self.evento_ventana,text="Hora Finalizacion*",font=("Helvetica",10)).place(x=10,y=180)
        self.hora_salida_entry = ttk.Entry(self.evento_ventana)
        self.hora_salida_entry.place(x=10,y=205)
        self.hora_salida_entry.insert(0,f"{self.now.hour + 1}:{minutos}")

        ttk.Label(self.evento_ventana, text="Importancia*",font=("Helvetica",10)).place(x=10,y=230)
        self.importancia_entry = ttk.Combobox(self.evento_ventana,values=["Normal","Importante"]
                                              ,state="readonly")
        self.importancia_entry.place(x=10,y=255)

        ttk.Label(self.evento_ventana, text="Descripcion(No usar comas',')",font=("Helvetica",10)).place(x=10,y=280)
        self.descripcion_entry = ttk.Entry(self.evento_ventana)
        self.descripcion_entry.place(x=10,y=305)

        ttk.Label(self.evento_ventana, text="Etiquetas*",font=("Helvetica",10)).place(x=10,y=330)
        self.etiquetas_entry = ttk.Entry(self.evento_ventana)
        self.etiquetas_entry.place(x=10,y=355)

        self.cancelar_button = tk.Button(self.evento_ventana,text="Cancelar",command=lambda: self.evento_ventana.destroy())
        self.cancelar_button.place(x=20,y=400)
        self.cancelar_button.config(fg="white",font=("times new roman", 11, "bold"))
        self.cancelar_button.config(bg="#000")

        self.aceptar_button = tk.Button(self.evento_ventana, text="Aceptar", command=self.enviar_datos)
        self.aceptar_button.place(x=110,y=400)
        self.aceptar_button.config(fg="white", font=("times new roman", 11, "bold"))
        self.aceptar_button.config(bg="#000")

        self.evento_ventana.mainloop()

    def datos_treeview(self):
        """Metodo que toma los valores de acuerdo al elemento seleccionado en la tabla"""
        self.seleccion = self.tabla.focus()
        self.detalles = self.tabla.item(self.seleccion)
        self.valor1 = self.detalles.get("values")[0]
        self.valor2 = self.detalles.get("values")[1]
        self.valor3 = self.detalles.get("values")[2]
        self.valor4 = self.detalles.get("values")[3]
        self.valor5 = self.detalles.get("values")[4]
        self.valor6 = self.detalles.get("values")[5]
        self.valor7 = self.detalles.get("values")[6]
        self.valor8 = self.detalles.get("values")[7]
        self.valor9 = self.detalles.get("values")[8]
    def modificar_evento_ventana(self):
        """Metodo que abre una ventana para modificar los datos de un evento"""
        try:
            self.evento_ventana = tk.Tk()
            self.evento_ventana.geometry("254x440+190+175")
            self.evento_ventana.resizable(False, False)
            self.evento_ventana.title("Modificar")
            self.datos_treeview()
            # Es igual que la ventana de agregar evento, solo que aqui
            # se insertan los valores de la tabla a los entry
            ttk.Label(self.evento_ventana, text="Modificar un Evento Existente", font=("Helvetica", 11, "underline"),
                      justify="center").place(x=10, y=10)
            ttk.Label(self.evento_ventana, text="Titulo*", font=("Helvetica", 10)).place(x=10, y=40)
            self.titulo_entry = ttk.Entry(self.evento_ventana)
            self.titulo_entry.place(x=10, y=60)
            self.titulo_entry.insert(0,self.valor3)

            ttk.Label(self.evento_ventana, text="Fecha (dd/mm/aaaa)*", font=("Helvetica", 10)).place(x=10, y=85)
            self.fecha_entry = ttk.Entry(self.evento_ventana)
            self.fecha_entry.place(x=10, y=105)
            self.fecha_entry.insert(0,self.valor4)

            ttk.Label(self.evento_ventana, text="Hora Inicio*", font=("Helvetica", 10)).place(x=10, y=130)
            self.hora_entry = ttk.Entry(self.evento_ventana)
            self.hora_entry.place(x=10, y=155)
            self.hora_entry.insert(0,self.valor5)

            ttk.Label(self.evento_ventana, text="Hora Finalizacion*", font=("Helvetica", 10)).place(x=10, y=180)
            self.hora_salida_entry = ttk.Entry(self.evento_ventana)
            self.hora_salida_entry.place(x=10, y=205)
            self.hora_salida_entry.insert(0,self.valor6)

            ttk.Label(self.evento_ventana, text="Importancia*", font=("Helvetica", 10)).place(x=10, y=230)
            self.importancia_entry = ttk.Combobox(self.evento_ventana, values=["Normal", "Importante"]
                                                  , state="readonly")
            self.importancia_entry.place(x=10, y=255)


            ttk.Label(self.evento_ventana, text="Descripcion(No usar comas',')", font=("Helvetica", 10)).place(x=10, y=280)
            self.descripcion_entry = ttk.Entry(self.evento_ventana)
            self.descripcion_entry.place(x=10, y=305)
            self.descripcion_entry.insert(0,self.valor8)

            ttk.Label(self.evento_ventana, text="Etiquetas*", font=("Helvetica", 10)).place(x=10, y=330)
            self.etiquetas_entry = ttk.Entry(self.evento_ventana)
            self.etiquetas_entry.place(x=10, y=355)
            self.etiquetas_entry.insert(0,self.valor)

            self.cancelar_button = tk.Button(self.evento_ventana, text="Cancelar",
                                             command=lambda: self.evento_ventana.destroy())
            self.cancelar_button.place(x=20, y=400)
            self.cancelar_button.config(fg="white", font=("times new roman", 11, "bold"))
            self.cancelar_button.config(bg="#000")


            # Aqui se almacenan los valores originales que el usuario haya
            # seleccionado de la tabla. Son los valores antes de ser modificados
            self.contenido_viejo = [self.valor1, self.valor2, self.valor3, str(self.valor4),
                                    str(self.valor5), self.valor6, self.valor7, self.valor8,str(self.valor9)]

            self.aceptar_button = tk.Button(self.evento_ventana, text="Aceptar", command=self.modificar_evento)
            self.aceptar_button.place(x=110, y=400)
            self.aceptar_button.config(fg="white", font=("times new roman", 11, "bold"))
            self.aceptar_button.config(bg="#000")



            self.evento_ventana.mainloop()
        except:
            # Si el usuario se olvida de seleccionar un elemento de la tabla antes de presionar
            # el boton, le mostrar este mensaje
            self.evento_ventana.destroy()
            messagebox.showerror("Aviso","Debe seleccionar un elemento de la tabla")


    def validacion_datos(self):
        """Metodo que verifica que, al momento de agregar o modificar un evento, los entry
        no se encuentren vacios o incompletos"""
        return not self.titulo_entry.get() or not self.fecha_entry.get() or not self.hora_entry.get() \
            or self.importancia_entry.get() == "" or not self.hora_salida_entry.get() or not self.etiquetas_entry.get()

    def enviar_datos(self):
        """Metodo que toma los valores de los entry, y los prepara para insertarlos en el archivo csv"""
        if self.validacion_datos() == True:
            # No debe dejar campos vacios al momento de enviar los datos,
            # Salvo el de "Descripcion" que es opcional
            ttk.Label(self.evento_ventana,text="No debe dejar\ncampos vacios",foreground="red").place(x=150,y=100)
        else:
            dia = time.strftime("%d")
            mes = time.strftime("%m")
            year = time.strftime("%Y")
            # fecha = datetime.now()
            fecha_hoy = f"{dia}/{mes}/{year}"
            auxiliar = self.fecha_entry.get().split("/")
            auxiliar2 = f"{auxiliar[2]}{auxiliar[1]}{auxiliar[0]}"
            contenido = [fecha_hoy,
                         self.titulo_entry.get(),
                         self.fecha_entry.get(),
                         self.hora_entry.get(),
                         self.hora_salida_entry.get(),
                         self.importancia_entry.get(),
                         self.descripcion_entry.get(),
                         self.etiquetas_entry.get()]
            # Todos los valores son pasado por parametro al metodo
            self.agregar_evento(contenido)
            messagebox.showinfo(message="Evento agregado correctamente")
            self.evento_ventana.destroy()
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()


    def agregar_evento(self,contenido):
        """Metodo que inserta los valores (pasados por parametros) en la tabla mysql"""
        cur = self.conn.cursor()
        consulta = """INSERT INTO calendario (fecha_creacion,titulo,
        fecha,hora_inicio,hora_fin,importancia,descripcion,etiquetas)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

        cur.execute(consulta, (contenido[0],contenido[1],contenido[2],
                               contenido[3],contenido[4],contenido[5],
                               contenido[6],contenido[7]))
        
        cur.close()
        self.conn.commit()

    def modificar_evento(self):
        """Metodo que modifica los datos de algun evento"""
        if self.validacion_datos() == True:
            ttk.Label(self.evento_ventana,text="No debe dejar\ncampos vacios",foreground="red").place(x=150,y=100)
        else:
            dia = time.strftime("%d")
            mes = time.strftime("%m")
            year = time.strftime("%Y")
            # self.now = datetime.now()
            fecha_hoy = f"{dia}/{mes}/{year}"
            auxiliar = self.fecha_entry.get().split("/")
            print(auxiliar)
            auxiliar2 = f"{auxiliar[2]}{auxiliar[1]}{auxiliar[0]}"
    
            self.contenido_nuevo = [fecha_hoy,
                                    self.titulo_entry.get(),                     
                                    self.fecha_entry.get(),
                                    self.hora_entry.get(), 
                                    self.hora_salida_entry.get(),
                                    self.importancia_entry.get(),
                                    self.descripcion_entry.get(),
                                    self.etiquetas_entry.get()]
            cur = self.conn.cursor()

            consulta = """UPDATE calendario SET fecha_creacion = %s,
            titulo = %s,fecha = %s,hora_inicio = %s,hora_fin = %s,
            importancia = %s,descripcion = %s,etiquetas = %s 
            WHERE id = %s;"""
            
            cur.execute(consulta, (self.contenido_nuevo[0],
                                   self.contenido_nuevo[1],
                                   self.contenido_nuevo[2],
                                   self.contenido_nuevo[3],
                                   self.contenido_nuevo[4],
                                   self.contenido_nuevo[5],
                                   self.contenido_nuevo[6],
                                   self.contenido_nuevo[7],
                                   self.valor1)) # Self.valor1 es el id, tomado del treeview
        
            cur.close()
            self.conn.commit()
            messagebox.showinfo("Aviso","Datos actualizados correctamente")
            self.evento_ventana.destroy()
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()

    def elmininar_evento(self):
        """Metodo que elimina un evento que se haya seleccionado"""
        try:
           self.datos_treeview()
           cur = self.conn.cursor()
           consulta = """DELETE FROM calendario WHERE id = %s;"""
            
           cur.execute(consulta, (self.valor1,)) # Self.valor1 es el id, tomado del treeview
        
           cur.close()
           self.conn.commit()
           

           messagebox.showinfo(message="Evento eliminado correctamente")
           self.tabla.delete(*self.tabla.get_children())
           self.tabla_treeview_general()
            # self.tabla_treeview_mensual()

        except:
            messagebox.showerror("Aviso","Debe seleccionar un elemento de la tabla")

    def buscar_evento(self):
        """Metodo que busca en la lista aquellos que eventos que coincidan con las
        palabras puestas en el buscador"""
        cur = self.conn.cursor()
        consulta = """SELECT * FROM calendario WHERE etiquetas LIKE %s;"""
        
        etiqueta = f"%{self.buscador_input.get()}%"

        cur.execute(consulta, (etiqueta,))
        
        
        datos = cur.fetchall()
        resultados = []
        for dato in datos:
                    
            resultados.append(f"Evento: {dato[2]}\nFecha: {dato[3]} {dato[4]}-{dato[5]} hs.\nDescripcion:\n{dato[7]}\n------------------  ------------------")

        label = ""
        
        for i in resultados:
            a = f'{i}\n'
            label = label + a
        self.ventana_buscador = tk.Tk()
        self.ventana_buscador.geometry("300x310+190+175")
        self.ventana_buscador.title("Resultados")
        self.ventana_buscador.resizable(False,False)
        area = tk.Text(self.ventana_buscador)
        area.place(x=0,y=0,width=310,height=300)
        area.insert(0.0, f"Resultados Encontrados:\n\n{label}")
        area.config(state="disabled")

        
        self.ventana_buscador.mainloop()
        cur.close()

    def vista_semanal(self):
        """Metodo que abre una ventana y muestra los eventos de la semana actual"""
        show_week_events(datetime.today())

    def vista_mensual(self):
        """Metodo que muestra un calendario en el cual se resaltan
        los dias con algun evento"""
        show_calendar(self.vista_mensual_frame)

Programa()