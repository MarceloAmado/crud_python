import sqlite3
import re
from tkinter import messagebox


class Modelo:
    def __init__(self):
        self.conexion = sqlite3.connect("Ventas.db")
        self.crear_tabla()

    def crear_tabla(self):
        cursor = self.conexion.cursor()
        sql = """CREATE TABLE IF NOT EXISTS productos
                 (codigo INTEGER PRIMARY KEY,
                 descripcion varchar(50) NOT NULL,
                 stock_m INTEGER,
                 precio REAL)
        """
        cursor.execute(sql)
        self.conexion.commit()

        def cargar_producto(self, codigo, descripcion, stock_m, precio):
            if not re.match(r"^[0-9\s]+$", codigo):
                messagebox.showerror(
                    "Error: No se puede cargar",
                    "El codigo solo admite números y no puede quedar vacío",
                )
                return

        if not re.match(r"^[A-Za-z0-9\s]+$", "descripcion"):
            messagebox.showerror(
                "Error: No se puede cargar",
                "Detalle no puede ser nulo ni contener caracteres especiales",
            )
            return

        if not re.match(r"^[0-9\s]+$", "stock_m"):
            messagebox.showerror(
                "Error: No se puede cargar",
                "El stock mínimo debe ser un número no nulo",
            )
            return

        if not re.match(r"^[0-9\.\s]+$", "precio"):
            messagebox.showerror(
                "Error: No se puede cargar", "Precio debe ser número no nulo"
            )
            return

        data = ("codigo", "descripcion", "stock_m", "precio")
        sql = "INSERT INTO productos (codigo, descripcion, stock_m, precio) VALUES(?, ?, ?, ?)"
        cursor = self.conexion.cursor()
        cursor.execute(sql, data)
        self.conexion.commit()
        messagebox.showinfo("Éxito", "Producto registrado")

    def eliminar_producto(self, codigo):
        data = (codigo,)
        sql = "DELETE FROM productos WHERE codigo = ?"
        cursor = self.conexion.cursor()
        cursor.execute(sql, data)
        self.conexion.commit()

    def obtener_productos(self):
        sql = "SELECT * FROM productos ORDER BY codigo ASC"
        cursor = self.conexion.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
