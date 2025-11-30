import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from special_lib import * 

class App:
    def __init__(self, root: tb.Window):
        self.root = root
        self.root.title("Analyzer")
        self.root.geometry("1000x700")

        self.style = tb.Style("superhero")  

        # -----------------------------
        #        FRAME SUPERIOR
        # -----------------------------
        top_frame = tb.Frame(self.root, padding=10)
        top_frame.pack(fill=X)

        # Botão para carregar arquivo
        self.bt_load = tb.Button(
            top_frame,
            text="📂 Carregar arquivo .txt",
            bootstyle=INFO,
            command=self.load_file
        )
        self.bt_load.pack(side=LEFT, padx=5)

        # Botão para executar análise
        self.bt_run = tb.Button(
            top_frame,
            text="▶ Rodar análise",
            bootstyle=SUCCESS,
            command=self.run_analysis
        )
        self.bt_run.pack(side=LEFT, padx=5)

        # -----------------------------
        #   FRAME PRINCIPAL (LEFT/RIGHT)
        # -----------------------------
        main_frame = tb.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # =============================
        #     LEFT SIDE – Entrada
        # =============================
        left = tb.Labelframe(main_frame, text="Frase em inglês", padding=10)
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        self.input_text = tk.Text(left, height=4, wrap="word")
        self.input_text.pack(fill=BOTH, expand=False)

        # =============================
        #   RIGHT SIDE – RESULTADOS
        # =============================
        right = tb.Frame(main_frame)
        right.pack(side=LEFT, fill=BOTH, expand=True)

        # --- área da tradução ---
        self.frame_trans = tb.Labelframe(right, text="Tradução (PT-BR)", padding=10)
        self.frame_trans.pack(fill=BOTH, expand=True, padx=5)
        
        self.output_trans = tk.Text(self.frame_trans, height=5, wrap="word")
        self.output_trans.pack(fill=BOTH, expand=True)

        # --- ignored values ---
        self.ignored_values = tb.Labelframe(right, text="Ignored values", padding=10)
        self.ignored_values.pack(fill=BOTH, expand=True, padx=5)

        self.output_ignored_values = tk.Text(self.ignored_values, height=5, wrap="word")
        self.output_ignored_values.pack(fill=BOTH, expand=True)

        # --- área da análise sintática ---
        self.frame_analysis = tb.Labelframe(left, text="Análise sintática", padding=10)
        self.frame_analysis.pack(fill=BOTH, expand=True, padx=5)

        self.output_analysis = tk.Text(self.frame_analysis, height=10, wrap="word")
        self.output_analysis.pack(fill=BOTH, expand=True)

        # --- área dos verbos ---
        self.frame_verbs = tb.Labelframe(left, text="Classificações encontradas", padding=10)
        self.frame_verbs.pack(fill=BOTH, expand=True, padx=5)

        self.output_verbs = tk.Text(self.frame_verbs, height=8, wrap="word")
        self.output_verbs.pack(fill=BOTH, expand=True)

    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione um arquivo .txt",
            filetypes=[("Arquivos de texto", "*.txt")]
        )
        if not filename:
            return

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        self.input_text.delete("1.0", END)
        self.input_text.insert(END, content)

    def insert_info(self, frase, doc):
        self.output_trans.insert(END, traduzir(frase))
        self.output_analysis.insert(END, show_content(doc))
        for v in g_Ignored_values:
            self.output_ignored_values.insert(END, f"-> {v}")
        self.output_verbs.insert(END, classify_verbs())
        self.output_verbs.insert(END, classify_rest(doc))

    def clear_fields(self) :
        self.output_trans.delete("1.0", END)
        self.output_analysis.delete("1.0", END)
        self.output_verbs.delete("1.0", END)
        self.output_ignored_values.delete("1.0", END)
        clear_arrays()

    def run_analysis(self):
        nlp = spacy.load("en_core_web_sm")
        frase = self.input_text.get("1.0", END).strip()
        if not frase:
            return
        doc = nlp(frase)
        self.clear_fields()
        self.insert_info(frase, doc)

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    if sys.platform == 'linux':
        root.style.configure('.', font=('Ubuntu Mono', 12))
    if sys.platform == 'win32':
        root.style.configure('.', font=('Consolas', 12))
    app = App(root)

    root.mainloop()
