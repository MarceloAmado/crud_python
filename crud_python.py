from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re


# ##############################################
# MODELO
# ##############################################
def conexion():
    con = sqlite3.connect("mibase.db")
    return con


def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE productos
             (codigoproducto INTEGER PRIMARY KEY,
             descripcion varchar(20) NOT NULL,
             stock real,
             stockmin real,
             precio real)
    """
    cursor.execute(sql)
    con.commit()


try:
    conexion()
    crear_tabla()
except:
    print("No se puede conectar a DB")


def alta(codigoproducto, descripcion, stock, stockmin, precio, tree):
    print(codigoproducto, descripcion, stock, stockmin, precio)
    con = conexion()
    cursor = con.cursor()
    data = (codigoproducto, descripcion, stock, stockmin, precio)
    sql = "INSERT INTO productos(codigoproducto, descripcion, stock, stockmin, precio) VALUES(?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()
    print("Producto cargado con éxito")
    actualizar_treeview(tree)


def consultar():
    global compra
    print(compra)


def borrar(tree):
    valor = tree.selection()
    print(valor)  # ('I005',)
    item = tree.item(valor)
    print(
        item
    )  # {'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open':0, 'tags': ''}
    print(item["text"])
    mi_id = item["text"]

    con = conexion()
    cursor = con.cursor()
    # mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM productos WHERE codigoproducto = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)


def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM productos ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))


# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("Mercado Negro")

titulo = Label(
    root,
    text="Sistema de Stock y Ventas",
    bg="#417E9B",
    fg="black",
    height=2,
    width=80,
)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W + E)
producto = Label(root, text="Producto")
producto.grid(row=1, column=0, sticky=W)
stock = Label(root, text="Cantidad")
stock.grid(row=2, column=0, sticky=W)
precio = Label(root, text="Precio")
precio.grid(row=3, column=0, sticky=W)

# Defino variables para tomar valores de campos de entrada
a_val, b_val, c_val = StringVar(), DoubleVar(), DoubleVar()
w_ancho = 20

entrada1 = Entry(root, textvariable=a_val, width=w_ancho)
entrada1.grid(row=1, column=1)
entrada2 = Entry(root, textvariable=b_val, width=w_ancho)
entrada2.grid(row=2, column=1)
entrada3 = Entry(root, textvariable=c_val, width=w_ancho)
entrada3.grid(row=3, column=1)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Producto")
tree.heading("col2", text="cantidad")
tree.heading("col3", text="precio")
tree.grid(row=10, column=0, columnspan=4)

boton_alta = Button(
    root, text="Alta", command=lambda: alta(a_val.get(), b_val.get(), c_val.get(), tree)
)
boton_alta.grid(row=6, column=1)

boton_consulta = Button(root, text="Consultar", command=lambda: consultar())
boton_consulta.grid(row=7, column=1)

boton_borrar = Button(root, text="Borrar", command=lambda: borrar(tree))
boton_borrar.grid(row=8, column=1)
root.mainloop()
