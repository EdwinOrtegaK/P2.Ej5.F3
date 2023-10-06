import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
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
        self.label1.grid(row=0, column=1, pady=10, padx=10, columnspan=3)

        # Variables para los Checkbuttons
        self.capacitor_type_var = tk.StringVar()

        # Checkbuttons para seleccionar el tipo de capacitor
        self.placas_checkbutton = ttk.Checkbutton(self.center_frame, text="Placas Paralelas", variable=self.capacitor_type_var, onvalue="Placas Paralelas", offvalue="", command=self.select_capacitor_type)
        self.placas_checkbutton.grid(row=1, column=1, pady=5, padx=10)

        self.esferico_checkbutton = ttk.Checkbutton(self.center_frame, text="Esférico", variable=self.capacitor_type_var, onvalue="Esférico", offvalue="", command=self.select_capacitor_type)
        self.esferico_checkbutton.grid(row=1, column=2, pady=5, padx=10)

        self.cilindrico_checkbutton = ttk.Checkbutton(self.center_frame, text="Cilíndrico", variable=self.capacitor_type_var, onvalue="Cilíndrico", offvalue="", command=self.select_capacitor_type)
        self.cilindrico_checkbutton.grid(row=1, column=3, pady=5, padx=10)

        # Cuadros de entrada de radios
        self.label2 = ttk.Label(self.center_frame, text="Radio A / Largo (m):")
        self.label2.grid(row=2, column=0, pady=5, padx=10)

        self.dimension_entry = ttk.Entry(self.center_frame)
        self.dimension_entry.grid(row=3, column=0, pady=5, padx=10)

        self.label3 = ttk.Label(self.center_frame, text="Radio B / Ancho (m):")
        self.label3.grid(row=2, column=1, pady=5, padx=10)

        self.dimension_entry2 = ttk.Entry(self.center_frame)
        self.dimension_entry2.grid(row=3, column=1, pady=5, padx=10)

        # Cuadros de entrada de voltage
        self.label4 = ttk.Label(self.center_frame, text="Voltage (V):")
        self.label4.grid(row=2, column=2, pady=5, padx=10)

        self.voltage_entry = ttk.Entry(self.center_frame)
        self.voltage_entry.grid(row=3, column=2, pady=5, padx=10)

        # Cuadros de entrada de DISTANCIA ENTRE PLACAS
        self.label5 = ttk.Label(self.center_frame, text="Distancia entre placas (m):")
        self.label5.grid(row=2, column=3, pady=5, padx=10)

        self.distance_entry = ttk.Entry(self.center_frame)
        self.distance_entry.grid(row=3, column=3, pady=5, padx=10)

        # Cuadros de entrada de LONGITUD
        self.label5 = ttk.Label(self.center_frame, text="Longitud (m):")
        self.label5.grid(row=2, column=4, pady=5, padx=10)

        self.longitud_entry = ttk.Entry(self.center_frame)
        self.longitud_entry.grid(row=3, column=4, pady=5, padx=10)

        # CheckBox para seleccionar si el capacitor contiene un dieléctrico
        self.dielectric_var = tk.IntVar()
        self.dielectric_checkbox = ttk.Checkbutton(self.center_frame, text="Contiene dieléctrico", variable=self.dielectric_var, command=self.toggle_dielectric_options)
        self.dielectric_checkbox.grid(row=4, column=1, pady=5, padx=10, columnspan=3)

        # Combobox para escoger si el dieléctrico cubre todo o solo la mitad del capacitor
        self.dielectric_coverage_var = tk.StringVar()
        self.dielectric_coverage_combobox = ttk.Combobox(self.center_frame, textvariable=self.dielectric_coverage_var, values=["Diélectrico completo", "Diélectrico a la mitad"])

        # Botón para calcular las propiedades del capacitor
        self.calculate_button = ttk.Button(self.center_frame, text="Calcular Propiedades", command=self.calculate_properties)
        self.calculate_button.grid(row=5, column=1, pady=10, padx=10, columnspan=3)

        # Etiqueta para mostrar el resultado del cálculo
        self.result_label = ttk.Label(self.center_frame, text="")
        self.result_label.grid(row=6, column=1, pady=10, padx=10, columnspan=3)

        # Creación del lienzo de Matplotlib (por ahora vacío, se llenará más adelante)
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title('Propiedades del Capacitor')
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.center_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=7, column=1, pady=10, padx=10, columnspan=3)

    def select_capacitor_type(self):
        # Desactivar los otros Checkbuttons cuando uno es seleccionado
        selected_type = self.capacitor_type_var.get()
        if selected_type == "Placas Paralelas":
            self.esferico_checkbutton.state(['!selected'])
            self.cilindrico_checkbutton.state(['!selected'])
            self.draw_placas_paralelas()
        elif selected_type == "Esférico":
            self.placas_checkbutton.state(['!selected'])
            self.cilindrico_checkbutton.state(['!selected'])
            self.draw_esferico()
        elif selected_type == "Cilíndrico":
            self.placas_checkbutton.state(['!selected'])
            self.esferico_checkbutton.state(['!selected'])
            self.draw_cilindrico()

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
    
    def plaques_capacitance(self, largo, ancho, distancia):
        epsilon0 = 8.854e-12  # Permitividad del vacío (F/m)
        C = (epsilon0 * largo * ancho) / (distancia)
        return C
    
    def cylinder_capacitance(self, ra, rb, longitud):
        epsilon0 = 8.854e-12  # Permitividad del vacío (F/m)
        C = (2 * math.pi * epsilon0 * longitud) / math.log(rb / ra)
        return C

    def calculate_properties(self):
        capacitor_type = self.capacitor_type_var.get()
        radioa = float(self.dimension_entry.get())
        radiob = float(self.dimension_entry2.get())
        largo2 = float(self.dimension_entry.get())
        ancho2 = float(self.dimension_entry2.get())
        voltage = float(self.voltage_entry.get())
        dist = float(self.distance_entry.get())
        long = float(self.longitud_entry.get())
        has_dielectric = self.dielectric_var.get()
        dielectric_coverage = self.dielectric_coverage_var.get()

        #SI EL CAPACITOR ES ESFERICO
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

        #SI EL CAPACITOR ES DE PLACAS PARALELAS
        if capacitor_type == "Placas Paralelas":
            largo = largo2
            ancho = ancho2
            distancia = dist
            capacitance = self.plaques_capacitance(largo, ancho, distancia)
            
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

        
        #SI EL CAPACITOR ES DE PLACAS PARALELAS
        if capacitor_type == "Cilíndrico":
            ra = radioa
            rb = radiob
            longitud = long
            capacitance = self.cylinder_capacitance(ra, rb, longitud)
            
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

    def draw_placas_paralelas(self):
        self.ax.clear()
        self.ax.set_title('Capacitor de Placas Paralelas')
        
        try:
            # Obtener valores de los campos de entrada
            largo = float(self.dimension_entry.get())
            ancho = float(self.dimension_entry2.get())  # Este será el grosor de las placas
            distancia = float(self.distance_entry.get())
            
            # Dibujar las placas paralelas como rectángulos
            upper_rect = plt.Rectangle((-largo/2, distancia/2), largo, ancho, color='blue')
            lower_rect = plt.Rectangle((-largo/2, -distancia/2-ancho), largo, ancho, color='blue')
            
            self.ax.add_patch(upper_rect)
            self.ax.add_patch(lower_rect)
            
            # Configurar límites del gráfico
            self.ax.set_xlim(-largo, largo)
            self.ax.set_ylim(-distancia-0.5-ancho, distancia+0.5+ancho)

            if self.dielectric_var.get() == 1:
                choice = self.dielectric_coverage_combobox.get()  # Obtener la selección del usuario
                if choice == "Diélectrico a la mitad":
                    # Rellenar solo la mitad izquierda del espacio entre las placas con dieléctrico
                    self.ax.fill_between([-largo/2, 0], -distancia/2, distancia/2, color='lightblue')
                elif choice == "Diélectrico completo":
                    # Rellenar todo el espacio entre las placas con dieléctrico
                    self.ax.fill_between([-largo/2, largo/2], -distancia/2, distancia/2, color='lightblue')

            self.canvas.draw()
        except ValueError:
            self.result_label.config(text="Por favor, ingrese valores valores válidos.")


    def draw_esferico(self):
        # Obtener valores de los campos de entrada
        try:
            ra = float(self.dimension_entry.get())
            rb = float(self.dimension_entry2.get())
        except ValueError:
            self.result_label.config(text="Por favor, ingrese valores válidos.")
            return

        self.ax.clear()
        self.ax.set_title('Capacitor Esférico')
        circle1 = plt.Circle((0, 0), ra, color='blue', fill=False, lw=2)
        circle2 = plt.Circle((0, 0), rb, color='blue', fill=False, lw=2)
        self.ax.add_artist(circle1)
        self.ax.add_artist(circle2)
        self.ax.set_xlim(-rb-0.5, rb+0.5)
        self.ax.set_ylim(-rb-0.5, rb+0.5)

        if self.dielectric_var.get() == 1:
            choice = self.dielectric_coverage_combobox.get()  # Obtener la selección del usuario
            if choice == "Diélectrico a la mitad":
                # Rellenar solo mitad del area entre radios
                wedge = patches.Wedge(center=(0,0), r=rb, theta1=180, theta2=360, width=rb-ra, color='lightblue')
                self.ax.add_patch(wedge)
            elif choice == "Diélectrico completo":
                # Rellenar todo el espacio entre los radios
                full_wedge = patches.Wedge(center=(0,0), r=rb, theta1=0, theta2=360, width=rb-ra, color='lightblue')
                self.ax.add_patch(full_wedge)

        self.canvas.draw()

    def draw_cilindrico(self):
        # Obtener valores de los campos de entrada
        try:
            ra = float(self.dimension_entry.get())
            rb = float(self.dimension_entry2.get())
        except ValueError:
            self.result_label.config(text="Por favor, ingrese valores válidos.")
            return

        self.ax.clear()
        self.ax.set_title('Capacitor Esférico')
        circle1 = plt.Circle((0, 0), ra, color='blue', fill=False, lw=2)
        circle2 = plt.Circle((0, 0), rb, color='blue', fill=False, lw=2)
        self.ax.add_artist(circle1)
        self.ax.add_artist(circle2)
        self.ax.set_xlim(-rb-0.5, rb+0.5)
        self.ax.set_ylim(-rb-0.5, rb+0.5)

        if self.dielectric_var.get() == 1:
            choice = self.dielectric_coverage_combobox.get()  # Obtener la selección del usuario
            if choice == "Diélectrico a la mitad":
                # Rellenar solo mitad del area entre radios
                wedge = patches.Wedge(center=(0,0), r=rb, theta1=180, theta2=360, width=rb-ra, color='lightblue')
                self.ax.add_patch(wedge)
            elif choice == "Diélectrico completo":
                # Rellenar todo el espacio entre los radios
                full_wedge = patches.Wedge(center=(0,0), r=rb, theta1=0, theta2=360, width=rb-ra, color='lightblue')
                self.ax.add_patch(full_wedge)

        self.canvas.draw()

# Crear la ventana principal de la aplicación
root = tk.Tk()
# Iniciar la aplicación de la Calculadora de Capacitores
app = CapacitorCalculator(root)
# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()