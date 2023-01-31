import csv
import uuid

from .connection_postgresql import ConnectionDB
from tkinter import messagebox

def create_table():
    connection = ConnectionDB()

    sql = ''' CREATE TABLE beneficiaries (
                id_beneficiary SERIAL,
                first_name VARCHAR(100),
                middle_name VARCHAR(100),
                last_name VARCHAR(100),
                curp VARCHAR(100),
                PRIMARY KEY(id_beneficiary)) '''
    
    try:
        connection.cursor.execute(sql)
        connection.close_connection()
        title = 'Crear Registro'
        menssage = 'Se creó la tabla en la base de datos'
        messagebox.showinfo(title, menssage)
    except:
        title = 'Crear Registro'
        menssage = 'La tabla ya está creada'
        messagebox.showwarning(title, menssage)


def delete_table():
    connection = ConnectionDB()
    sql = 'DROP TABLE beneficiaries'

    del_table = messagebox.askyesnocancel("Borrar Tabla", "¿Deseas borrar la tabla?\nLa tabla se eliminará permanentemente.")
    
    if del_table == True:
        try:
            connection.cursor.execute(sql)
            connection.close_connection()
            title = 'Borrar Registro'
            menssage = 'La tabla de la base de datos se borró con éxito'
            messagebox.showinfo(title, menssage)
        except:
            title = 'Borrar Registro'
            menssage = 'No hay tabla para borrar'
            messagebox.showerror(title, menssage)


class Beneficiary:
    def __init__(self, first_name, middle_name, last_name, curp):
        self.id_beneficiary = None
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.curp = curp

    def __str__(self):
        return f'Beneficiario[{self.first_name}, {self.middle_name}, {self.last_name}, {self.curp}]'


def save(beneficiary):
    connection = ConnectionDB()

    sql = f"""INSERT INTO beneficiaries(first_name, middle_name, last_name, curp)
    VALUES('{beneficiary.first_name}', '{beneficiary.middle_name}', '{beneficiary.last_name}', '{beneficiary.curp}')"""

    try:
        connection.cursor.execute(sql)
        connection.close_connection()
    except:
        title = 'Conexión al registro'
        menssage = 'La tabla peliculas no está creada en la base de datos'
        messagebox.showerror(title, menssage)


def show():
    connection = ConnectionDB()

    beneficiaries_list = []
    sql = 'SELECT * FROM beneficiaries'

    try:
        connection.cursor.execute(sql)
        beneficiaries_list = connection.cursor.fetchall()
        connection.close_connection()
    except:
        title = 'Conexión al registro'
        menssage = 'Crea la tabla en la base de datos'
        messagebox.showwarning(title, menssage)

    return beneficiaries_list


def edit(beneficiary, id_beneficiary):
    connection = ConnectionDB()

    sql = f"""UPDATE beneficiaries
    SET first_name = '{beneficiary.first_name}',
    middle_name = '{beneficiary.middle_name}',
    last_name = '{beneficiary.last_name}',
    curp = '{beneficiary.curp}'
    WHERE id_beneficiary = {id_beneficiary}"""

    try:
        connection.cursor.execute(sql)
        connection.close_connection()
    except:
        title = 'Edición de datos'
        menssage = 'No se ha podido editar este registro'
        messagebox.showerror(title, menssage)


def eliminate(id_beneficiary):
    connection = ConnectionDB()
    sql = f'DELETE FROM beneficiaries WHERE id_beneficiary = {id_beneficiary}'

    try:
        connection.cursor.execute(sql)
        connection.close_connection()
    except:
        title = 'Eliminar datos'
        menssage = 'No se pudo eliminar el registro'
        messagebox.showerror(title, menssage)


def export():
    export_data = messagebox.askyesno("Exportar Datos", "¿Deseas continuar?")
    if export_data == True:
        data = show()
        filename = str(uuid.uuid4()) + ".csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'NOMBRE', 'A. PATERNO', 'A MATERNO', 'CURP'])
            writer.writerows(data)