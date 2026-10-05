import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import json
import os
from PIL import Image, ImageDraw, ImageFont

class SistemaCobranzaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cobranza con IVA 16%")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configuración
        self.iva_porcentaje = 16
        self.facturas = []
        self.clientes = []
        
        # Cargar datos existentes
        self.cargar_datos()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def cargar_datos(self):
        """Cargar datos desde archivo JSON"""
        try:
            if os.path.exists('facturas.json'):
                with open('facturas.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.facturas = data.get('facturas', [])
                    self.clientes = data.get('clientes', [])
        except Exception as e:
            print(f"Error cargando datos: {e}")
    
    def guardar_datos(self):
        """Guardar datos en archivo JSON"""
        try:
            data = {
                'facturas': self.facturas,
                'clientes': self.clientes
            }
            with open('facturas.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando datos: {e}")
    
    def crear_interfaz(self):
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Crear Factura
        self.crear_pestana_factura(notebook)
        
        # Pestaña 2: Lista de Facturas
        self.crear_pestana_lista(notebook)
        
        # Pestaña 3: Clientes
        self.crear_pestana_clientes(notebook)
        
        # Pestaña 4: Reportes
        self.crear_pestana_reportes(notebook)
    
    def crear_pestana_factura(self, notebook):
        """Crear pestaña para generar facturas"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Crear Factura")
        
        # Título
        titulo = tk.Label(frame, text="GENERAR NUEVA FACTURA", 
                         font=('Arial', 16, 'bold'), fg='#2c3e50')
        titulo.pack(pady=10)
        
        # Frame de datos del cliente
        frame_cliente = tk.LabelFrame(frame, text="Datos del Cliente", 
                                    font=('Arial', 10, 'bold'), bg='#f8f9fa')
        frame_cliente.pack(fill='x', padx=10, pady=5)
        
        # Campos del cliente
        tk.Label(frame_cliente, text="Cedula:", bg='#f8f9fa').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.rfc = tk.Entry(frame_cliente, width=20)
        self.rfc.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_cliente, text="Nombre:", bg='#f8f9fa').grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.nombre_cliente = tk.Entry(frame_cliente, width=30)
        self.nombre_cliente.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_cliente, text="Dirección:", bg='#f8f9fa').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.direccion = tk.Entry(frame_cliente, width=30)
        self.direccion.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='we')
        
        # Frame de conceptos
        frame_conceptos = tk.LabelFrame(frame, text="Conceptos de la Factura", 
                                      font=('Arial', 10, 'bold'), bg='#f8f9fa')
        frame_conceptos.pack(fill='x', padx=10, pady=5)
        
        # Tabla de conceptos
        columns = ('descripcion', 'cantidad', 'precio', 'importe')
        self.tree_conceptos = ttk.Treeview(frame_conceptos, columns=columns, show='headings', height=6)
        
        self.tree_conceptos.heading('descripcion', text='Descripción')
        self.tree_conceptos.heading('cantidad', text='Cantidad')
        self.tree_conceptos.heading('precio', text='Precio Unitario')
        self.tree_conceptos.heading('importe', text='Importe')
        
        self.tree_conceptos.column('descripcion', width=300)
        self.tree_conceptos.column('cantidad', width=80)
        self.tree_conceptos.column('precio', width=120)
        self.tree_conceptos.column('importe', width=120)
        
        self.tree_conceptos.pack(fill='x', padx=5, pady=5)
        
        # Frame para agregar conceptos
        frame_agregar = tk.Frame(frame_conceptos, bg='#f8f9fa')
        frame_agregar.pack(fill='x', padx=5, pady=5)
        
        tk.Label(frame_agregar, text="Descripción:", bg='#f8f9fa').pack(side='left', padx=2)
        self.descripcion = tk.Entry(frame_agregar, width=30)
        self.descripcion.pack(side='left', padx=2)
        
        tk.Label(frame_agregar, text="Cantidad:", bg='#f8f9fa').pack(side='left', padx=2)
        self.cantidad = tk.Entry(frame_agregar, width=8)
        self.cantidad.pack(side='left', padx=2)
        self.cantidad.insert(0, "1")
        
        tk.Label(frame_agregar, text="Precio:", bg='#f8f9fa').pack(side='left', padx=2)
        self.precio = tk.Entry(frame_agregar, width=10)
        self.precio.pack(side='left', padx=2)
        
        btn_agregar = tk.Button(frame_agregar, text="Agregar Concepto", 
                               command=self.agregar_concepto, bg='#3498db', fg='white')
        btn_agregar.pack(side='left', padx=10)
        
        btn_eliminar = tk.Button(frame_agregar, text="Eliminar Seleccionado", 
                                command=self.eliminar_concepto, bg='#e74c3c', fg='white')
        btn_eliminar.pack(side='left', padx=5)
        
        # Frame de totales
        frame_totales = tk.Frame(frame, bg='#f8f9fa')
        frame_totales.pack(fill='x', padx=10, pady=5)
        
        self.label_subtotal = tk.Label(frame_totales, text="Subtotal: $0.00", 
                                      font=('Arial', 12, 'bold'), bg='#f8f9fa')
        self.label_subtotal.pack(side='left', padx=10)
        
        self.label_iva = tk.Label(frame_totales, text="IVA (16%): $0.00", 
                                 font=('Arial', 12, 'bold'), bg='#f8f9fa')
        self.label_iva.pack(side='left', padx=10)
        
        self.label_total = tk.Label(frame_totales, text="TOTAL: $0.00", 
                                   font=('Arial', 14, 'bold'), fg='#c0392b', bg='#f8f9fa')
        self.label_total.pack(side='left', padx=10)
        
        # Botones
        frame_botones = tk.Frame(frame, bg='#f0f0f0')
        frame_botones.pack(pady=10)
        
        btn_generar = tk.Button(frame_botones, text="Generar Factura", 
                               command=self.generar_factura, 
                               font=('Arial', 12, 'bold'),
                               bg='#27ae60', fg='white', width=15, height=2)
        btn_generar.pack(side='left', padx=10)
        
        btn_limpiar = tk.Button(frame_botones, text="Limpiar Formulario", 
                               command=self.limpiar_formulario,
                               bg='#f39c12', fg='white', width=15, height=2)
        btn_limpiar.pack(side='left', padx=10)
        
        # Inicializar variables
        self.conceptos = []
        self.actualizar_totales()
    
    def agregar_concepto(self):
        """Agregar un concepto a la tabla"""
        try:
            descripcion = self.descripcion.get().strip()
            cantidad = float(self.cantidad.get())
            precio = float(self.precio.get())
            
            if not descripcion:
                messagebox.showwarning("Advertencia", "La descripción es obligatoria")
                return
            
            importe = cantidad * precio
            
            # Agregar a la tabla
            self.tree_conceptos.insert('', 'end', values=(
                descripcion, f"{cantidad:.2f}", f"${precio:.2f}", f"${importe:.2f}"
            ))
            
            # Agregar a la lista de conceptos
            self.conceptos.append({
                'descripcion': descripcion,
                'cantidad': cantidad,
                'precio': precio,
                'importe': importe
            })
            
            # Limpiar campos
            self.descripcion.delete(0, tk.END)
            self.cantidad.delete(0, tk.END)
            self.cantidad.insert(0, "1")
            self.precio.delete(0, tk.END)
            
            # Actualizar totales
            self.actualizar_totales()
            
        except ValueError:
            messagebox.showerror("Error", "Cantidad y Precio deben ser números válidos")
    
    def eliminar_concepto(self):
        """Eliminar concepto seleccionado"""
        seleccion = self.tree_conceptos.selection()
        if seleccion:
            item = seleccion[0]
            index = self.tree_conceptos.index(item)
            self.tree_conceptos.delete(item)
            self.conceptos.pop(index)
            self.actualizar_totales()
    
    def actualizar_totales(self):
        """Actualizar los totales en tiempo real"""
        subtotal = sum(item['importe'] for item in self.conceptos)
        iva = subtotal * (self.iva_porcentaje / 100)
        total = subtotal + iva
        
        self.label_subtotal.config(text=f"Subtotal: ${subtotal:.2f}")
        self.label_iva.config(text=f"IVA ({self.iva_porcentaje}%): ${iva:.2f}")
        self.label_total.config(text=f"TOTAL: ${total:.2f}")
    
    def generar_factura(self):
        """Generar la factura completa"""
        if not self.conceptos:
            messagebox.showwarning("Advertencia", "Debe agregar al menos un concepto")
            return
        
        if not self.rfc.get() or not self.nombre_cliente.get():
            messagebox.showwarning("Advertencia", "Los datos del cliente son obligatorios")
            return
        
        # Calcular totales
        subtotal = sum(item['importe'] for item in self.conceptos)
        iva = subtotal * (self.iva_porcentaje / 100)
        total = subtotal + iva
        
        # Crear factura
        factura = {
            'folio': f"FAC-{len(self.facturas) + 1:04d}",
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cliente': {
                'rfc': self.rfc.get(),
                'nombre': self.nombre_cliente.get(),
                'direccion': self.direccion.get()
            },
            'conceptos': self.conceptos.copy(),
            'subtotal': subtotal,
            'iva': iva,
            'total': total,
            'iva_porcentaje': self.iva_porcentaje
        }
        
        # Agregar a la lista
        self.facturas.append(factura)
        
        # Guardar cliente si no existe
        cliente_existente = any(c['rfc'] == self.rfc.get() for c in self.clientes)
        if not cliente_existente:
            self.clientes.append({
                'rfc': self.rfc.get(),
                'nombre': self.nombre_cliente.get(),
                'direccion': self.direccion.get()
            })
        
        # Guardar datos
        self.guardar_datos()
        
        # Mostrar opciones para la factura
        self.mostrar_opciones_factura(factura)
        
        # Limpiar formulario
        self.limpiar_formulario()
        
        messagebox.showinfo("Éxito", f"Factura {factura['folio']} generada correctamente")
    
    def mostrar_opciones_factura(self, factura):
        """Mostrar opciones para ver o guardar la factura"""
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Opciones Factura {factura['folio']}")
        ventana.geometry("400x200")
        
        tk.Label(ventana, text=f"Factura {factura['folio']} Generada", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=20)
        
        btn_ver = tk.Button(frame_botones, text="Ver Factura en Pantalla", 
                          command=lambda: self.mostrar_factura_generada(factura),
                          bg='#3498db', fg='white', width=20, height=2)
        btn_ver.pack(pady=5)
        
        btn_imagen = tk.Button(frame_botones, text="Guardar como JPEG", 
                             command=lambda: self.guardar_factura_jpeg(factura),
                             bg='#27ae60', fg='white', width=20, height=2)
        btn_imagen.pack(pady=5)
        
        btn_ambos = tk.Button(frame_botones, text="Ambas Opciones", 
                            command=lambda: self.ambas_opciones(factura, ventana),
                            bg='#9b59b6', fg='white', width=20, height=2)
        btn_ambos.pack(pady=5)
    
    def ambas_opciones(self, factura, ventana):
        """Ejecutar ambas opciones y cerrar ventana"""
        self.mostrar_factura_generada(factura)
        self.guardar_factura_jpeg(factura)
        ventana.destroy()
    
    def guardar_factura_jpeg(self, factura):
        """Guardar la factura como imagen JPEG"""
        try:
            # Crear imagen
            width, height = 800, 1000
            image = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(image)
            
            # Cargar fuentes (usar fuentes por defecto o descargar una)
            try:
                title_font = ImageFont.truetype("arialbd.ttf", 24)
                header_font = ImageFont.truetype("arialbd.ttf", 18)
                normal_font = ImageFont.truetype("arial.ttf", 12)
                bold_font = ImageFont.truetype("arialbd.ttf", 12)
            except:
                # Fuentes por defecto si no se encuentran las especificadas
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                normal_font = ImageFont.load_default()
                bold_font = ImageFont.load_default()
            
            y_position = 50
            
            # Título
            draw.text((width//2, y_position), "FACTURA ELECTRÓNICA", fill='black', font=title_font, anchor="mm")
            y_position += 40
            
            # Línea separadora
            draw.line([(50, y_position), (width-50, y_position)], fill='black', width=2)
            y_position += 30
            
            # Folio y Fecha
            draw.text((50, y_position), f"Folio: {factura['folio']}", fill='black', font=bold_font)
            draw.text((width-50, y_position), f"Fecha: {factura['fecha']}", fill='black', font=bold_font, anchor="ra")
            y_position += 40
            
            # Datos del cliente
            draw.text((50, y_position), "DATOS DEL CLIENTE:", fill='black', font=header_font)
            y_position += 30
            draw.text((70, y_position), f"RFC: {factura['cliente']['rfc']}", fill='black', font=normal_font)
            y_position += 25
            draw.text((70, y_position), f"Nombre: {factura['cliente']['nombre']}", fill='black', font=normal_font)
            y_position += 25
            draw.text((70, y_position), f"Dirección: {factura['cliente']['direccion']}", fill='black', font=normal_font)
            y_position += 40
            
            # Línea separadora
            draw.line([(50, y_position), (width-50, y_position)], fill='black', width=1)
            y_position += 20
            
            # Encabezado de conceptos
            draw.text((50, y_position), "CONCEPTOS", fill='black', font=header_font, anchor="mm")
            y_position += 30
            
            # Encabezados de tabla
            draw.text((50, y_position), "Descripción", fill='black', font=bold_font)
            draw.text((400, y_position), "Cantidad", fill='black', font=bold_font)
            draw.text((500, y_position), "P.Unitario", fill='black', font=bold_font)
            draw.text((650, y_position), "Importe", fill='black', font=bold_font)
            y_position += 30
            
            # Línea bajo encabezados
            draw.line([(50, y_position), (width-50, y_position)], fill='black', width=1)
            y_position += 20
            
            # Conceptos
            for concepto in factura['conceptos']:
                # Descripción (con salto de línea si es muy larga)
                desc_lines = self.wrap_text(concepto['descripcion'], 35)
                for line in desc_lines:
                    draw.text((50, y_position), line, fill='black', font=normal_font)
                    y_position += 20
                
                # Datos numéricos
                draw.text((400, y_position-20), f"{concepto['cantidad']:.2f}", fill='black', font=normal_font)
                draw.text((500, y_position-20), f"${concepto['precio']:.2f}", fill='black', font=normal_font)
                draw.text((650, y_position-20), f"${concepto['importe']:.2f}", fill='black', font=normal_font)
                y_position += 10
            
            y_position += 20
            
            # Línea separadora
            draw.line([(50, y_position), (width-50, y_position)], fill='black', width=1)
            y_position += 30
            
            # Totales
            draw.text((500, y_position), "SUBTOTAL:", fill='black', font=bold_font)
            draw.text((650, y_position), f"${factura['subtotal']:.2f}", fill='black', font=bold_font)
            y_position += 30
            
            draw.text((500, y_position), f"IVA ({factura['iva_porcentaje']}%):", fill='black', font=bold_font)
            draw.text((650, y_position), f"${factura['iva']:.2f}", fill='black', font=bold_font)
            y_position += 30
            
            # Línea doble para total
            draw.line([(500, y_position), (width-50, y_position)], fill='black', width=2)
            y_position += 10
            
            draw.text((500, y_position), "TOTAL:", fill='black', font=header_font)
            draw.text((650, y_position), f"${factura['total']:.2f}", fill='black', font=header_font)
            y_position += 20
            
            draw.line([(500, y_position), (width-50, y_position)], fill='black', width=2)
            y_position += 40
            
            # Pie de página
            draw.text((width//2, y_position), "¡Gracias por su compra!", fill='black', font=header_font, anchor="mm")
            
            # Guardar imagen
            filename = f"factura_{factura['folio']}.jpg"
            image.save(filename, "JPEG", quality=95)
            
            messagebox.showinfo("Éxito", f"Factura guardada como:\n{filename}\n\nLista para imprimir!")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {str(e)}")
    
    def wrap_text(self, text, max_length):
        """Dividir texto en líneas si es muy largo"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_length:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                if len(current_line) > max_length:
                    # Si una palabra es muy larga, dividirla
                    while len(current_line) > max_length:
                        lines.append(current_line[:max_length])
                        current_line = current_line[max_length:]
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def mostrar_factura_generada(self, factura):
        """Mostrar factura generada en una nueva ventana"""
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Factura {factura['folio']}")
        ventana.geometry("600x800")
        
        # Contenido de la factura
        texto = scrolledtext.ScrolledText(ventana, width=70, height=40, font=('Courier', 10))
        texto.pack(padx=10, pady=10)
        
        # Formatear factura
        contenido = self.formatear_factura(factura)
        texto.insert(tk.END, contenido)
        texto.config(state=tk.DISABLED)
        
        # Botón para guardar como JPEG
        btn_guardar = tk.Button(ventana, text="Guardar como JPEG", 
                              command=lambda: self.guardar_factura_jpeg(factura),
                              bg='#27ae60', fg='white')
        btn_guardar.pack(pady=10)
    
    def formatear_factura(self, factura):
        """Formatear la factura para mostrar"""
        contenido = f"""
{'='*50}
{'FACTURA ELECTRÓNICA':^50}
{'='*50}
Folio: {factura['folio']}
Fecha: {factura['fecha']}

DATOS DEL CLIENTE:
RFC: {factura['cliente']['rfc']}
Nombre: {factura['cliente']['nombre']}
Dirección: {factura['cliente']['direccion']}

{'='*50}
{'CONCEPTOS':^50}
{'='*50}
{'Descripción':<30} {'Cant':>6} {'P.Unit':>8} {'Importe':>10}
{'-'*50}
"""
        
        for concepto in factura['conceptos']:
            contenido += f"{concepto['descripcion'][:29]:<30} {concepto['cantidad']:>6.2f} ${concepto['precio']:>7.2f} ${concepto['importe']:>9.2f}\n"
        
        contenido += f"""
{'-'*50}
{'SUBTOTAL:':<46} ${factura['subtotal']:>9.2f}
{'IVA (16%):':<46} ${factura['iva']:>9.2f}
{'='*50}
{'TOTAL:':<46} ${factura['total']:>9.2f}
{'='*50}

¡Gracias por su compra!
"""
        return contenido
    
    def limpiar_formulario(self):
        """Limpiar todo el formulario"""
        self.rfc.delete(0, tk.END)
        self.nombre_cliente.delete(0, tk.END)
        self.direccion.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.cantidad.insert(0, "1")
        self.precio.delete(0, tk.END)
        
        # Limpiar tabla de conceptos
        for item in self.tree_conceptos.get_children():
            self.tree_conceptos.delete(item)
        
        self.conceptos.clear()
        self.actualizar_totales()
    
    def crear_pestana_lista(self, notebook):
        """Crear pestaña para listar facturas"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Lista de Facturas")
        
        # Título
        tk.Label(frame, text="FACTURAS GENERADAS", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(frame)
        frame_busqueda.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_busqueda, text="Buscar:").pack(side='left')
        self.busqueda = tk.Entry(frame_busqueda, width=30)
        self.busqueda.pack(side='left', padx=5)
        self.busqueda.bind('<KeyRelease>', self.buscar_facturas)
        
        # Tabla de facturas
        columns = ('folio', 'fecha', 'cliente', 'subtotal', 'iva', 'total')
        self.tree_facturas = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        self.tree_facturas.heading('folio', text='Folio')
        self.tree_facturas.heading('fecha', text='Fecha')
        self.tree_facturas.heading('cliente', text='Cliente')
        self.tree_facturas.heading('subtotal', text='Subtotal')
        self.tree_facturas.heading('iva', text='IVA')
        self.tree_facturas.heading('total', text='Total')
        
        self.tree_facturas.column('folio', width=100)
        self.tree_facturas.column('fecha', width=150)
        self.tree_facturas.column('cliente', width=200)
        self.tree_facturas.column('subtotal', width=100)
        self.tree_facturas.column('iva', width=100)
        self.tree_facturas.column('total', width=100)
        
        self.tree_facturas.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Frame de botones
        frame_botones = tk.Frame(frame)
        frame_botones.pack(pady=5)
        
        btn_ver = tk.Button(frame_botones, text="Ver Factura Seleccionada", 
                           command=self.ver_factura_seleccionada,
                           bg='#3498db', fg='white')
        btn_ver.pack(side='left', padx=5)
        
        btn_imprimir = tk.Button(frame_botones, text="Guardar JPEG de Factura", 
                               command=self.guardar_jpeg_seleccionada,
                               bg='#27ae60', fg='white')
        btn_imprimir.pack(side='left', padx=5)
        
        # Cargar facturas
        self.actualizar_lista_facturas()
    
    def guardar_jpeg_seleccionada(self):
        """Guardar como JPEG la factura seleccionada"""
        seleccion = self.tree_facturas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una factura para guardar como JPEG")
            return
        
        item = seleccion[0]
        folio = self.tree_facturas.item(item)['values'][0]
        
        factura = next((f for f in self.facturas if f['folio'] == folio), None)
        if factura:
            self.guardar_factura_jpeg(factura)
    
    def actualizar_lista_facturas(self):
        """Actualizar la lista de facturas"""
        for item in self.tree_facturas.get_children():
            self.tree_facturas.delete(item)
        
        for factura in self.facturas:
            self.tree_facturas.insert('', 'end', values=(
                factura['folio'],
                factura['fecha'],
                factura['cliente']['nombre'],
                f"${factura['subtotal']:.2f}",
                f"${factura['iva']:.2f}",
                f"${factura['total']:.2f}"
            ))
    
    def buscar_facturas(self, event=None):
        """Buscar facturas en la lista"""
        query = self.busqueda.get().lower()
        
        for item in self.tree_facturas.get_children():
            self.tree_facturas.delete(item)
        
        for factura in self.facturas:
            if (query in factura['folio'].lower() or 
                query in factura['cliente']['nombre'].lower() or
                query in factura['cliente']['rfc'].lower()):
                
                self.tree_facturas.insert('', 'end', values=(
                    factura['folio'],
                    factura['fecha'],
                    factura['cliente']['nombre'],
                    f"${factura['subtotal']:.2f}",
                    f"${factura['iva']:.2f}",
                    f"${factura['total']:.2f}"
                ))
    
    def ver_factura_seleccionada(self):
        """Ver la factura seleccionada"""
        seleccion = self.tree_facturas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una factura para ver")
            return
        
        item = seleccion[0]
        folio = self.tree_facturas.item(item)['values'][0]
        
        factura = next((f for f in self.facturas if f['folio'] == folio), None)
        if factura:
            self.mostrar_factura_generada(factura)
    
    def crear_pestana_clientes(self, notebook):
        """Crear pestaña para gestionar clientes"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Clientes")
        
        tk.Label(frame, text="LISTA DE CLIENTES", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Tabla de clientes
        columns = ('rfc', 'nombre', 'direccion')
        self.tree_clientes = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        self.tree_clientes.heading('rfc', text='RFC')
        self.tree_clientes.heading('nombre', text='Nombre')
        self.tree_clientes.heading('direccion', text='Dirección')
        
        self.tree_clientes.column('rfc', width=120)
        self.tree_clientes.column('nombre', width=200)
        self.tree_clientes.column('direccion', width=250)
        
        self.tree_clientes.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Cargar clientes
        self.actualizar_lista_clientes()
    
    def actualizar_lista_clientes(self):
        """Actualizar la lista de clientes"""
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        for cliente in self.clientes:
            self.tree_clientes.insert('', 'end', values=(
                cliente['rfc'],
                cliente['nombre'],
                cliente['direccion']
            ))
    
    def crear_pestana_reportes(self, notebook):
        """Crear pestaña para reportes"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Reportes")
        
        tk.Label(frame, text="REPORTES Y ESTADÍSTICAS", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Frame de estadísticas
        frame_stats = tk.LabelFrame(frame, text="Estadísticas Generales", font=('Arial', 10, 'bold'))
        frame_stats.pack(fill='x', padx=10, pady=5)
        
        self.label_total_facturas = tk.Label(frame_stats, text="Total de Facturas: 0", 
                                           font=('Arial', 12), justify='left')
        self.label_total_facturas.pack(anchor='w', padx=10, pady=2)
        
        self.label_total_ventas = tk.Label(frame_stats, text="Total en Ventas: $0.00", 
                                         font=('Arial', 12), justify='left')
        self.label_total_ventas.pack(anchor='w', padx=10, pady=2)
        
        self.label_total_iva = tk.Label(frame_stats, text="Total IVA Recaudado: $0.00", 
                                      font=('Arial', 12), justify='left')
        self.label_total_iva.pack(anchor='w', padx=10, pady=2)
        
        self.label_clientes = tk.Label(frame_stats, text="Total de Clientes: 0", 
                                     font=('Arial', 12), justify='left')
        self.label_clientes.pack(anchor='w', padx=10, pady=2)
        
        # Botón para actualizar reportes
        btn_actualizar = tk.Button(frame, text="Actualizar Reportes", 
                                 command=self.actualizar_reportes,
                                 bg='#9b59b6', fg='white')
        btn_actualizar.pack(pady=10)
        
        # Actualizar reportes inicialmente
        self.actualizar_reportes()
    
    def actualizar_reportes(self):
        """Actualizar los reportes"""
        total_facturas = len(self.facturas)
        total_ventas = sum(f['total'] for f in self.facturas)
        total_iva = sum(f['iva'] for f in self.facturas)
        total_clientes = len(self.clientes)
        
        self.label_total_facturas.config(text=f"Total de Facturas: {total_facturas}")
        self.label_total_ventas.config(text=f"Total en Ventas: ${total_ventas:.2f}")
        self.label_total_iva.config(text=f"Total IVA Recaudado: ${total_iva:.2f}")
        self.label_clientes.config(text=f"Total de Clientes: {total_clientes}")

def main():
    root = tk.Tk()
    app = SistemaCobranzaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()