from os import times
import tkinter as tk
from tkinter import ttk, messagebox
from model.beneficiary_postgresql import create_table, delete_table
from model.beneficiary_postgresql import Beneficiary, save, edit, show, eliminate, export


def menu_bar(root):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar, width=300, height=300)

    # Options
    menu_bar.add_command(label='Crear Tabla', command=create_table)
    menu_bar.add_command(label='Eliminar Tabla', command=delete_table)
    menu_bar.add_command(label='Salir', command=root.destroy)



class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.bg_color = '#ced2cc'
        self.root = root
        self.pack()
        self.config(bg=self.bg_color)
        self.beneficiaries_fields()
        self.disable_fields()
        self.beneficiaries_table()


    def beneficiaries_fields(self):
        self.label_first_name = tk.Label(self, text='Nombre: ', anchor='e')
        self.label_first_name.config(font=('Arial', 12, 'bold'), bg=self.bg_color)
        self.label_first_name.grid(row=0, column=0, padx=10, pady=10, sticky='E')

        self.label_middle_name = tk.Label(self, text='Apellido paterno: ')
        self.label_middle_name.config(font=('Arial', 12, 'bold'), bg=self.bg_color)
        self.label_middle_name.grid(row=1, column=0, padx=10, pady=10, sticky='E')

        self.label_last_name = tk.Label(self, text='Apellido materno: ')
        self.label_last_name.config(font=('Arial', 12, 'bold'), bg=self.bg_color)
        self.label_last_name.grid(row=2, column=0, padx=10, pady=10, sticky='E')

        self.label_curp = tk.Label(self, text='Identificador: ')
        self.label_curp.config(font=('Arial', 12, 'bold'), bg=self.bg_color)
        self.label_curp.grid(row=3, column=0, padx=10, pady=10, sticky='E')

        # Entries
        self.first_name = tk.StringVar()
        self.entry_first_name = tk.Entry(self, textvariable=self.first_name)
        self.entry_first_name.config(width=50, font=('Arial', 12))
        self.entry_first_name.grid(row=0, column=1, padx=10, pady=10, columnspan=3)

        self.middle_name = tk.StringVar()
        self.entry_middle_name = tk.Entry(self, textvariable=self.middle_name)
        self.entry_middle_name.config(width=50, font=('Arial', 12))
        self.entry_middle_name.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        self.last_name = tk.StringVar()
        self.entry_last_name = tk.Entry(self, textvariable=self.last_name)
        self.entry_last_name.config(width=50, font=('Arial', 12))
        self.entry_last_name.grid(row=2, column=1, padx=10, pady=10, columnspan=3)

        self.curp = tk.StringVar()
        self.entry_curp = tk.Entry(self, textvariable=self.curp)
        self.entry_curp.config(width=50, font=('Arial', 12))
        self.entry_curp.grid(row=3, column=1, padx=10, pady=10, columnspan=3)

         # Buttons
        self.new_button = tk.Button(self, text="Nuevo", command=self.enable_fields)
        self.new_button.config(width=15, font=('Arial', 12, 'bold'), fg='white', bg='#407855',
                                cursor='hand2', activebackground='#35BD6F', border='2px')
        self.new_button.grid(row=0, column=4, padx=10, pady=10)

        self.save_button = tk.Button(self, text="Guardar", command=self.save_data)
        self.save_button.config(width=15, font=('Arial', 12, 'bold'), fg='white', bg='#4052ab',
                                cursor='hand2', activebackground='#3586DF', border='2px')
        self.save_button.grid(row=1, column=4, padx=10, pady=10)

        self.cancel_button = tk.Button(self, text="Cancelar", command=self.disable_fields)
        self.cancel_button.config(width=15, font=('Arial', 12, 'bold'), fg='white', bg='#a4262c',
                                cursor='hand2', activebackground='#E15370', border='2px')
        self.cancel_button.grid(row=3, column=4, padx=10, pady=10)


    def enable_fields(self):
        self.first_name.set('')
        self.middle_name.set('')
        self.last_name.set('')
        self.curp.set('')

        self.entry_first_name.config(state='normal')
        self.entry_middle_name.config(state='normal')
        self.entry_last_name.config(state='normal')
        self.entry_curp.config(state='normal')

        self.save_button.config(state='normal', bg='#4052ab')
        self.cancel_button.config(state='normal', bg='#a4262c')


    def disable_fields(self):
        self.id_beneficiary = None
        self.first_name.set('')
        self.middle_name.set('')
        self.last_name.set('')
        self.curp.set('')

        self.entry_first_name.config(state='disabled')
        self.entry_middle_name.config(state='disabled')
        self.entry_last_name.config(state='disabled')
        self.entry_curp.config(state='disabled')

        self.save_button.config(state='disabled', bg='#ccc')
        self.cancel_button.config(state='disabled', bg='#ccc')

    
    def save_data(self):
        beneficiary = Beneficiary(
            self.first_name.get(),
            self.middle_name.get(),
            self.last_name.get(),
            self.curp.get()
        )
        
        if self.id_beneficiary == None:
            save(beneficiary)
        else:
            edit(beneficiary, self.id_beneficiary)

        self.beneficiaries_table()
        self.disable_fields()

    
    def beneficiaries_table(self):
        # Retrieve the list of beneficiaries
        self.beneficiaries_list = show()
        self.beneficiaries_list.reverse()
        
        self.table = ttk.Treeview(self, column=('Nombre', 'A. paterno', 'A. materno', 'Identificador'))
        self.table.grid(row=5, column=0, padx=10, columnspan=5, sticky='nse')

        # Scrollbar for the table if it exceeds 10 records
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.table.yview)
        self.scroll.grid(row=5, column=4, sticky='nse')
        self.table.configure(yscrollcommand=self.scroll.set)

        
        self.table.heading('#0', text='NÚMERO')
        self.table.heading('#1', text='NOMBRE')
        self.table.heading('#2', text='A. PATERNO')
        self.table.heading('#3', text='A. MATERNO')
        self.table.heading('#4', text='IDENTIFICADOR')

        # Iterate the list of beneficiaries
        for p in self.beneficiaries_list:
            self.table.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4]))

        # Export button
        self.edit_button = tk.Button(self, text="Exportar datos", command=self.export_data)
        self.edit_button.config(width=15, font=('Arial', 12, 'bold'), fg='white', bg='#407855',
                                cursor='hand2', activebackground='#35BD6F', border='2px')
        self.edit_button.grid(row=6, column=0, padx=10, pady=10)

        # Edit button
        self.edit_button = tk.Button(self, text="Editar", command=self.edit_data)
        self.edit_button.config(width=15, font=('Arial', 12, 'bold'), fg='white', bg='#407855',
                                cursor='hand2', activebackground='#35BD6F', border='2px')
        self.edit_button.grid(row=6, column=3, padx=10, pady=10)

        # Delete button
        self.eliminate_button = tk.Button(self, text="Eliminar", command=self.eliminate_data)
        self.eliminate_button.config(width=15, font=('Arial', 12, 'bold'), fg='white', bg='#a4262c',
                                cursor='hand2', activebackground='#E15370', border='2px')
        self.eliminate_button.grid(row=6, column=4, padx=10, pady=10)


    def export_data(self):
        export()


    def edit_data(self):
        try:
            self.id_beneficiary = self.table.item(self.table.selection())['text']
            self.first_name_beneficiary = self.table.item(self.table.selection())['values'][0]
            self.middle_name_beneficiary = self.table.item(self.table.selection())['values'][1]
            self.last_name_beneficiary = self.table.item(self.table.selection())['values'][2]
            self.curp_beneficiary = self.table.item(self.table.selection())['values'][3]

            self.enable_fields()

            self.entry_first_name.insert(0, self.first_name_beneficiary)
            self.entry_middle_name.insert(0, self.middle_name_beneficiary)
            self.entry_last_name.insert(0, self.last_name_beneficiary)
            self.entry_curp.insert(0, self.curp_beneficiary)
        
        except:
            title = 'Edición de datos'
            menssage = 'No ha seleccionado ningún registro'
            messagebox.showerror(title, menssage)


    def eliminate_data(self):
        try:
            self.id_beneficiary = self.table.item(self.table.selection())['text']
            eliminate(self.id_beneficiary)

            self.beneficiaries_table()
            self.id_beneficiary = None

        except:
            title = 'Eliminar un registro'
            menssage = 'No ha seleccionado ningún registro'
            messagebox.showerror(title, menssage)
