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
class Programa:

    def __init__(self):
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
        self.tabs.add(self.vista_mensual_frame,text=" Vista Mes Actual")
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

        # Boton que obtiene la fecha del calendario
        self.fecha_evento_button = tk.Button(contenedor_botones, text="Buscar Evento",
                                         font=("times new roman", 11, "bold"),command=self.buscar_fecha)

        self.fecha_evento_button.place(x=10,y=170)
        self.fecha_evento_button.config(fg="white")
        self.fecha_evento_button.config(bg="#000")
        tk.Label(text="Buscar por fecha",background="#BEBEBE").place(x=130,y=180)

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
        self.tabla.column("#1", width=80, anchor=CENTER)
        self.tabla.column("#2", width=80, anchor=CENTER)
        self.tabla.column("#3", width=80, anchor=CENTER)
        self.tabla.column("#4", width=45, anchor=CENTER)
        self.tabla.column("#5", width=45, anchor=CENTER)
        self.tabla.column("#6", width=85, anchor=CENTER)
        self.tabla.column("#7", width=110, anchor=CENTER)
        self.tabla.column("#8", width=80, anchor=CENTER)
        self.tabla.column("#9", width=70, anchor=CENTER)

        self.tabla["show"] = "headings"
        self.tabla.heading("#1", text="CREADO", anchor=CENTER)
        self.tabla.heading("#2", text="TITULO", anchor=CENTER)
        self.tabla.heading("#3", text="FECHA", anchor=CENTER)
        self.tabla.heading("#4", text="DESDE", anchor=CENTER)
        self.tabla.heading("#5", text="HASTA", anchor=CENTER)
        self.tabla.heading("#6", text="IMPORTANCIA", anchor=CENTER)
        self.tabla.heading("#7", text="DESCRIPCION", anchor=CENTER)
        self.tabla.heading("#8", text="ETIQUETAS", anchor=CENTER)
        self.tabla.heading("#9", text="CODIGO", anchor=CENTER)

    def tabla_treeview_general(self):
        """Tabla que muestra los datos de los eventos. Obtenidos desde el archivo agenda.csv"""
        self.tabla = ttk.Treeview(self.vista_general, height=15,
                                  columns=("#1","#2","#3","#4","#5","#6","#7","#8","#9"))
        self.tabla.place(x=0,y=0)

        self.columnas_treeview()
        # Aqui se insertan los datos del "agenda.csv" a la tabla

        with open("agenda.csv","r",newline="") as archivo_csv:
            cal = calendar.Calendar()
            now = datetime.now()
            self.mes = cal.monthdayscalendar(now.year, now.month)
            agenda = csv.DictReader(archivo_csv)
            rows = sorted(agenda, reverse=True, key=operator.itemgetter('Codigo')) #Sirve para ordenar la lista cronologicamente
            for linea in rows:
                #Las variables obtienen los valores de las columnas. REVISAR
                agendado = linea['Agendado']
                titulo = linea['Titulo']
                fecha = linea['Fecha']
                hora_inicio = linea['Hora Inicio']
                hora_fin = linea['Hora Fin']
                importancia = linea['Importancia']
                descripcion = linea['Descripcion']
                etiquetas = linea['Etiquetas']
                codigo = linea["Codigo"]

                # Si la importancia del evento es "Importante" se cambiará el color de celda. Las "Normal
                # se mantienen tal cual
                if importancia == "Importante":
                    self.tabla.insert('', 0, values=(agendado,titulo,fecha,hora_inicio,
                                                 hora_fin,importancia,descripcion,etiquetas,codigo),tags=("color",))
                    self.tabla.tag_configure("color",background="#99f1f8")
                else:
                    self.tabla.insert('', 0, values=(agendado, titulo, fecha, hora_inicio,
                                                     hora_fin, importancia, descripcion, etiquetas,codigo))


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
            self.titulo_entry.insert(0,self.valor2)

            ttk.Label(self.evento_ventana, text="Fecha (dd/mm/aaaa)*", font=("Helvetica", 10)).place(x=10, y=85)
            self.fecha_entry = ttk.Entry(self.evento_ventana)
            self.fecha_entry.place(x=10, y=105)
            self.fecha_entry.insert(0,self.valor3)

            ttk.Label(self.evento_ventana, text="Hora Inicio*", font=("Helvetica", 10)).place(x=10, y=130)
            self.hora_entry = ttk.Entry(self.evento_ventana)
            self.hora_entry.place(x=10, y=155)
            self.hora_entry.insert(0,self.valor4)

            ttk.Label(self.evento_ventana, text="Hora Finalizacion*", font=("Helvetica", 10)).place(x=10, y=180)
            self.hora_salida_entry = ttk.Entry(self.evento_ventana)
            self.hora_salida_entry.place(x=10, y=205)
            self.hora_salida_entry.insert(0,self.valor5)

            ttk.Label(self.evento_ventana, text="Importancia*", font=("Helvetica", 10)).place(x=10, y=230)
            self.importancia_entry = ttk.Combobox(self.evento_ventana, values=["Normal", "Importante"]
                                                  , state="readonly")
            self.importancia_entry.place(x=10, y=255)


            ttk.Label(self.evento_ventana, text="Descripcion(No usar comas',')", font=("Helvetica", 10)).place(x=10, y=280)
            self.descripcion_entry = ttk.Entry(self.evento_ventana)
            self.descripcion_entry.place(x=10, y=305)
            self.descripcion_entry.insert(0,self.valor7)

            ttk.Label(self.evento_ventana, text="Etiquetas*", font=("Helvetica", 10)).place(x=10, y=330)
            self.etiquetas_entry = ttk.Entry(self.evento_ventana)
            self.etiquetas_entry.place(x=10, y=355)
            self.etiquetas_entry.insert(0,self.valor8)

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
            codigo = "".join(auxiliar2)
            contenido = [fecha_hoy,self.titulo_entry.get(),self.fecha_entry.get(),
                         self.hora_entry.get(),self.hora_salida_entry.get(),
                         self.importancia_entry.get(),self.descripcion_entry.get(),
                         self.etiquetas_entry.get(),str(codigo)]
            # Todos los valores son pasado por parametro al metodo
            self.agregar_evento(contenido)
            messagebox.showinfo(message="Evento agregado correctamente")
            self.evento_ventana.destroy()
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()


    def agregar_evento(self,contenido):
        """Metodo que inserta los valores (pasados por parametros) en el archvio csv"""
        with open("agenda.csv", "a", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(contenido)

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
            auxiliar2 = f"{auxiliar[2]}{auxiliar[1]}{auxiliar[0]}"
            codigo = "".join(auxiliar2)
            # Se guardan las modificaciones que el usuario haya hecho a los datos
            self.contenido_nuevo = [fecha_hoy, self.titulo_entry.get(), self.fecha_entry.get(),
                                    self.hora_entry.get(), self.hora_salida_entry.get(),
                                    self.importancia_entry.get(), self.descripcion_entry.get(),
                                    self.etiquetas_entry.get(),str(codigo)]
            # Lista que guardara los datos del archivo csv
            csv_nuevo = []
            # Primero se lee el archivo csv, luego, cuando coincida los datos seleccionados
            # de la tabla (antes de la modificacion) se agregara la linea nueva, reemplazando
            # a la anterior. Luego se borra el archivo csv, y se vuelve a abrir para
            # agregar los datos nuevos, que fueron guardados en una lista
            with open("agenda.csv", "r", newline="") as archivo:
                lector = csv.reader(archivo)
                for linea in lector:
                    if linea == self.contenido_viejo: #Esta variable se encuentra en el metodo "modificar_evento_ventana"
                        csv_nuevo.append(self.contenido_nuevo)
                    else:
                        csv_nuevo.append(linea)
            file = open("agenda.csv","w")
            file.close()
            with open("agenda.csv", "a", newline="") as archivo_nuevo:
                for i in csv_nuevo:
                    escritor = csv.writer(archivo_nuevo)
                    escritor.writerow(i)
            messagebox.showinfo("Aviso","Datos actualizados correctamente")
            self.evento_ventana.destroy()
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()

    def elmininar_evento(self):
        """Metodo que elimina un evento que se haya seleccionado"""
        try:
            # Funciona de manera similar al metodo de modificar los datos, salvo, con la
            # excepcion de que, cuando encuentre la linea que quiera eliminar, se omitirá,
            # borrando asi el dato
            self.datos_treeview()
            contenido_viejo = [self.valor1, self.valor2, self.valor3, str(self.valor4),
                                str(self.valor5), self.valor6, self.valor7, self.valor8,str(self.valor9)]
            csv_nuevo = []
            with open("agenda.csv", "r", newline="") as archivo:
                lector = csv.reader(archivo)
                for linea in lector:
                    if linea == contenido_viejo:
                        continue
                    else:
                        csv_nuevo.append(linea)
            file = open("agenda.csv","w")
            file.close()
            with open("agenda.csv", "a", newline="") as archivo_nuevo:
                for i in csv_nuevo:
                    escritor = csv.writer(archivo_nuevo)
                    escritor.writerow(i)
            messagebox.showinfo(message="Evento eliminado correctamente")
            self.tabla.delete(*self.tabla.get_children())
            self.tabla_treeview_general()
            # self.tabla_treeview_mensual()

        except:
            messagebox.showerror("Aviso","Debe seleccionar un elemento de la tabla")

    def buscar_evento(self):
        """Metodo que busca en la lista aquellos que eventos que coincidan con las
        palabras puestas en el buscador"""
        resultados = []
        with open("agenda.csv","r") as archivo:
            agenda = csv.DictReader(archivo)
            rows = sorted(agenda, reverse=True, key=operator.itemgetter('Codigo')) #Sirve para ordenar la lista cronologicamente
            for evento in rows:
                etiquetas = evento['Etiquetas']
                titulo = evento["Titulo"]
                fecha = evento['Fecha']
                hora_inicio = evento['Hora Inicio']
                hora_fin = evento['Hora Fin']
                descripcion = evento["Descripcion"]
                if self.buscador_input.get() in etiquetas:
                    resultados.append(f"Evento: {titulo}\nFecha: {fecha} {hora_inicio}-{hora_fin} hs.\nDescripcion:\n{descripcion}\n------------------  ------------------")

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

    def buscar_fecha(self):
        """Metodo que busca eventos de acuerdo a la fecha seleccionada en el Calendario"""
        self.seleccion = self.cal.get_date()
        # Se lee el archivo csv, filtrando los eventos que coincidan con la fecha
        # seleccionada y guardandolo en una lista
        with open("agenda.csv","r") as archivo:
            next(archivo)
            agenda = []
            eventos = csv.reader(archivo)
            for linea in eventos:
                if linea != []:
                    auxiliar = linea[2]
                    auxiliar2 = auxiliar.split("/")
                    dia = f"{int(auxiliar2[0])}/{int(auxiliar2[1])}/{int(auxiliar2[2][-2:])}"
                    dia2 = str(dia)
                    print(dia2)
                    print((self.seleccion))
                    if dia2 == self.seleccion:
                        agenda.append(f"Evento: {linea[1]}\nFecha:{linea[2]} {linea[3]}-{linea[4]}hs.\nDescripcion:{linea[6]}\n------------------  ------------------")

        label = ""
        for i in agenda:
            a = f'{i}\n'
            label = label + a

        self.ventana_buscador = tk.Tk()
        self.ventana_buscador.geometry("300x310+190+175")
        self.ventana_buscador.title("Resultados")
        self.ventana_buscador.resizable(False,False)
        area = tk.Text(self.ventana_buscador)
        area.place(x=0, y=0, width=310, height=300)
        area.insert(0.0,f"Resultados Encontrados al {self.seleccion}:\n\n{label}")
        area.config(state="disabled")

        self.ventana_buscador.mainloop()

    def vista_semanal(self):
        """Metodo que abre una ventana y muestra los eventos de la semana actual"""
        show_week_events(datetime.today())

    def vista_mensual(self):
        """Metodo que muestra un calendario en el cual se resaltan
        los dias con algun evento"""
        show_calendar(self.vista_mensual_frame)

Programa()