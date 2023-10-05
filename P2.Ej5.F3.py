import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import math

class CapacitorCalculator:
    def __init__(self, root):
        
        # Estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TCheckbutton", font=("Arial", 12))

        self.root = root
        self.root.title("Calculadora de Capacitores")
        # self.root.iconbitmap('path_to_icon.ico')  # Descomenta esta línea si tienes un ícono para la ventana

        # Centrar contenido en la ventana
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Contenedor central para todos los widgets
        self.center_frame = ttk.Frame(root)
        self.center_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Etiqueta para seleccionar el tipo de capacitor
        self.label1 = ttk.Label(self.center_frame, text="Seleccione el tipo de capacitor:")
        self.label1.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

        # Variables para los Checkbuttons
        self.capacitor_type_var = tk.StringVar()

        # Checkbuttons para seleccionar el tipo de capacitor
        self.placas_checkbutton = ttk.Checkbutton(self.center_frame, text="Placas Paralelas", variable=self.capacitor_type_var, onvalue="Placas Paralelas", offvalue="", command=self.select_capacitor_type)
        self.placas_checkbutton.grid(row=1, column=0, pady=5, padx=10)

        self.esferico_checkbutton = ttk.Checkbutton(self.center_frame, text="Esférico", variable=self.capacitor_type_var, onvalue="Esférico", offvalue="", command=self.select_capacitor_type)
        self.esferico_checkbutton.grid(row=1, column=1, pady=5, padx=10)

        self.cilindrico_checkbutton = ttk.Checkbutton(self.center_frame, text="Cilíndrico", variable=self.capacitor_type_var, onvalue="Cilíndrico", offvalue="", command=self.select_capacitor_type)
        self.cilindrico_checkbutton.grid(row=1, column=2, pady=5, padx=10)

        # Cuadros de entrada de radios
        self.label2 = ttk.Label(self.center_frame, text="Radio A (m):")
        self.label2.grid(row=2, column=0, pady=5, padx=10)

        self.dimension_entry = ttk.Entry(self.center_frame)
        self.dimension_entry.grid(row=3, column=0, pady=5, padx=10)

        self.label3 = ttk.Label(self.center_frame, text="Radio B (m):")
        self.label3.grid(row=2, column=1, pady=5, padx=10)

        self.dimension_entry2 = ttk.Entry(self.center_frame)
        self.dimension_entry2.grid(row=3, column=1, pady=5, padx=10)

        # Cuadros de entrada de voltage
        self.label4 = ttk.Label(self.center_frame, text="Voltage (V):")
        self.label4.grid(row=2, column=2, pady=5, padx=10)

        self.voltage_entry = ttk.Entry(self.center_frame)
        self.voltage_entry.grid(row=3, column=2, pady=5, padx=10)

        # CheckBox para seleccionar si el capacitor contiene un dieléctrico
        self.dielectric_var = tk.IntVar()
        self.dielectric_checkbox = ttk.Checkbutton(self.center_frame, text="Contiene dieléctrico", variable=self.dielectric_var, command=self.toggle_dielectric_options)
        self.dielectric_checkbox.grid(row=4, column=0, pady=5, padx=10, columnspan=3)

        # Combobox para escoger si el dieléctrico cubre todo o solo la mitad del capacitor
        self.dielectric_coverage_var = tk.StringVar()
        self.dielectric_coverage_combobox = ttk.Combobox(self.center_frame, textvariable=self.dielectric_coverage_var, values=["Diélectrico completo", "Diélectrico a la mitad"])

        # Botón para calcular las propiedades del capacitor
        self.calculate_button = ttk.Button(self.center_frame, text="Calcular Propiedades", command=self.calculate_properties)
        self.calculate_button.grid(row=5, column=0, pady=10, padx=10, columnspan=3)

        # Etiqueta para mostrar el resultado del cálculo
        self.result_label = ttk.Label(self.center_frame, text="")
        self.result_label.grid(row=6, column=0, pady=10, padx=10, columnspan=3)

        # Creación del lienzo de Matplotlib (por ahora vacío, se llenará más adelante)
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title('Propiedades del Capacitor')
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.center_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=7, column=0, pady=10, padx=10, columnspan=3)

    def select_capacitor_type(self):
        # Desactivar los otros Checkbuttons cuando uno es seleccionado
        selected_type = self.capacitor_type_var.get()
        if selected_type == "Placas Paralelas":
            self.esferico_checkbutton.state(['!selected'])
            self.cilindrico_checkbutton.state(['!selected'])
        elif selected_type == "Esférico":
            self.placas_checkbutton.state(['!selected'])
            self.cilindrico_checkbutton.state(['!selected'])
        elif selected_type == "Cilíndrico":
            self.placas_checkbutton.state(['!selected'])
            self.esferico_checkbutton.state(['!selected'])

    def toggle_dielectric_options(self):
        # Mostrar u ocultar el Combobox de cobertura del dieléctrico según si se selecciona o no
        if self.dielectric_var.get() == 1:
            self.dielectric_coverage_combobox.grid(row=6, column=0, pady=5, padx=10, columnspan=3)
        else:
            self.dielectric_coverage_combobox.grid_forget()

    def spherical_capacitance(self, ra, rb):
        epsilon0 = 8.854e-12  # Permitividad del vacío (F/m)
        C = (4 * math.pi * epsilon0 * ra * rb) / (rb - ra)
        return C

    def calculate_properties(self):
        capacitor_type = self.capacitor_type_var.get()
        radioa = float(self.dimension_entry.get())
        radiob = float(self.dimension_entry2.get())
        voltage = float(self.voltage_entry.get())
        has_dielectric = self.dielectric_var.get()
        dielectric_coverage = self.dielectric_coverage_var.get()

        if capacitor_type == "Esférico":
            ra = radioa
            rb = radiob
            capacitance = self.spherical_capacitance(ra, rb)
            
            charge = capacitance * voltage
            energy = (charge*voltage)/2
            
            if has_dielectric:
                free_charge = 0.6 * charge
                bound_charge = 0.4 * charge
                self.result_label.config(text=f"Capacitancia: {capacitance:.4e} F\nCarga: {charge:.4e} C\nEnergía: {energy:.4e} J\nCarga Libre: {free_charge:.4e} C\nCarga Ligada: {bound_charge:.4e} C")
            else:
                self.result_label.config(text=f"Capacitancia: {capacitance:.4e} F\nCarga: {charge:.4e} C\nEnergía: {energy:.4e} J")
        else:
            self.result_label.config(text="Propiedades calculadas (esto es solo un mensaje de prueba).")

# Crear la ventana principal de la aplicación
root = tk.Tk()
# Iniciar la aplicación de la Calculadora de Capacitores
app = CapacitorCalculator(root)
# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
