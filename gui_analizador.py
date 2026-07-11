import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import sys
from io import StringIO

# Importar los analizadores
from Analisis_Lexico import analizar, analizar_reservadas, lexer
from Analisis_Sintactico import parser, ERRORS, generar_log_sintactico
import Analisis_Semantico as sem
parser = None

class AnalizadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico, Sintáctico y Semántico - Lua")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Analizador de Código Lua", 
                              font=("Arial", 18, "bold"), foreground="#1a73e8")
        title_label.pack(pady=10)
        
        # Área de entrada de código
        input_frame = ttk.LabelFrame(main_frame, text="Código Lua de Entrada", padding="8")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        
        self.codigo_text = scrolledtext.ScrolledText(input_frame, height=14, 
                                                    font=("Consolas", 11), undo=True)
        self.codigo_text.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=12)
        
        ttk.Button(button_frame, text="🔍 Analizar Todo", command=self.analizar_todo).pack(side=tk.LEFT, padx=6)
        ttk.Button(button_frame, text="🧹 Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=6)
        ttk.Button(button_frame, text="📌 Sintactico", command=self.cargar_ejemplo1).pack(side=tk.LEFT, padx=6)
        ttk.Button(button_frame, text="📌 Semantico", command=self.cargar_ejemplo2).pack(side=tk.LEFT, padx=6)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados y Errores", padding="8")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=22, 
                                                    font=("Consolas", 10), bg="#f8f9fa")
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="✅ Listo - Ingresa código y presiona Analizar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=5)
    
    def analizar_todo(self):
        codigo = self.codigo_text.get("1.0", tk.END).strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Por favor ingresa código Lua para analizar.")
            return

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "🚀 INICIANDO ANÁLISIS COMPLETO...\n\n")
        self.status_var.set("Analizando...")
        self.root.update()

        try:
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

            # Reseteos (igual que main.py)
            ERRORS.clear()
            sem.reset_semantico()

            # === ANÁLISIS SINTÁCTICO ===
            self.result_text.insert(tk.END, "📋 --- ANÁLISIS SINTÁCTICO ---\n")
            parser.parse(codigo, lexer=lexer)

            if ERRORS:
                self.result_text.insert(tk.END, f"❌ Errores Sintácticos encontrados: {len(ERRORS)}\n")
                for e in ERRORS:
                    self.result_text.insert(tk.END, f"   {e}\n")
            else:
                self.result_text.insert(tk.END, "✅ Sintaxis correcta\n")

            # === ANÁLISIS SEMÁNTICO ===
            self.result_text.insert(tk.END, "\n🔍 --- ANÁLISIS SEMÁNTICO ---\n")
            sem.generar_log_semantico(codigo, usuario="gui_usuario")

            if sem.SEMANTIC_ERRORS:
                self.result_text.insert(tk.END, f"⚠️ Errores Semánticos encontrados: {len(sem.SEMANTIC_ERRORS)}\n")
                for e in sem.SEMANTIC_ERRORS:
                    self.result_text.insert(tk.END, f"   {e}\n")
            else:
                self.result_text.insert(tk.END, "✅ Semántica correcta\n")

            sys.stdout = old_stdout
            output = mystdout.getvalue()
            if output.strip():
                self.result_text.insert(tk.END, f"\n📄 --- SALIDA ADICIONAL ---\n{output}")

            self.result_text.insert(tk.END, "\n🎉 === ANÁLISIS FINALIZADO ===\n")
            generar_log_sintactico(codigo, usuario="gui")

            messagebox.showinfo("Éxito", "Análisis completado correctamente.")

        except Exception as e:
            self.result_text.insert(tk.END, f"\n❌ Error durante el análisis: {str(e)}\n")
            import traceback
            self.result_text.insert(tk.END, traceback.format_exc())
        finally:
            sys.stdout = old_stdout
            self.status_var.set("✅ Listo")
    
    def limpiar(self):
        self.codigo_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
    
    def cargar_ejemplo1(self):
        try:
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            #ruta = os.path.join(script_dir, "algoritmo_sintactico_EspinozaNahin.lua")
            ruta = os.path.join(script_dir, "algoritmo_sintactico_RuizJul.lua")
            with open(ruta, "r", encoding="utf-8") as f:
                self.codigo_text.delete("1.0", tk.END)
                self.codigo_text.insert(tk.END, f.read())
            self.status_var.set("Ejemplo 1 cargado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar algoritmo_sintactico_EspinozaNahin.lua\n\n{e}")

    def cargar_ejemplo2(self):
        try:
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            #ruta = os.path.join(script_dir, "algoritmo_semantico_EspinozaNahin.lua")
            ruta = os.path.join(script_dir, "algoritmo_semantico_RuizJul.lua")
            with open(ruta, "r", encoding="utf-8") as f:
                self.codigo_text.delete("1.0", tk.END)
                self.codigo_text.insert(tk.END, f.read())
            self.status_var.set("Ejemplo 2 cargado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar algoritmo_semantico_EspinozaNahin.lua\n\n{e}")


if __name__ == "__main__":
    from Analisis_Lexico import lexer
    from Analisis_Sintactico import parser
    root = tk.Tk()
    app = AnalizadorGUI(root)
    root.mainloop()