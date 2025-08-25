import sys, json, spacy, time;
import tkinter as tk;
from tkinter import filedialog;
from translate import Translator
sys.stdout.reconfigure(encoding='utf-8'); #encoda caracteres especiais

#tradutor de string
tradutor = Translator(to_lang="pt-br")
def traduzir(frase):
    print(f"\n-----> A tradução do inglês para o PT-BR: <-----\n-----> {tradutor.translate(frase)} <-----\n")
    


# arrays para tempos verbais
g_Simple_present = []
g_Present_continuous = []
g_Simple_past = []
g_Past_participle = []

#carregando json
try:
    with open("dicionarios.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print("Erro ao carregar 'dicionarios.json': " + e)
    
# função __init__ indica construtor: função que é chamada sempre que o programa for iniciado.
def __init__():
    nlp = spacy.load("en_core_web_sm")
    type_pick = str(input("Você quer digitar uma frase ou escolher um arquivo .txt neste computador? ([e]scolher/[d]igitar)\n"))
    if type_pick in "dD":
        conteudo = str(input("Digite a frase: \n"))
    elif type_pick in "eE":
        root = tk.Tk()
        root.withdraw()
        find_file = filedialog.askopenfilename(
            title="Selecione um arquivo .txt",
            filetypes=[("Arquivos de texto", "*.txt")]
        )
        if find_file:
            with open(find_file, "r", encoding="utf-8") as f:
                conteudo = f.read()
            print(find_file)
            for c in find_file.split('/'):
                if ".txt" in c:
                    print(f"-> Arquivo encontrado: {c}")
        else:
            print("Não foi possível acessar o arquivo.")
            sys.exit()
    
    traduzir(conteudo)
    doc = nlp(conteudo)
    if show_content(doc):
        classify_verbs()
        input("Pressione qualquer tecla para terminar o programa...")
    else:
        print("Erro ao mostrar conteúdo.")

# func pra mostrar o conteudo do spacy doc
def show_content(doc):
    ignored_values = data["ignore"].values()
    ignorados = 0
    for c in doc:
        if c.text.lower() in ignored_values:
            ignorados+=1
    time.sleep(1.5)
    print(f"-> Foram encontradas {len(doc)-ignorados} palavras no seu texto!")
    for token in doc:
        tag = token.tag_
        tk = token.text
        # ignorar caracteres inuteis para a análise
        if tk.lower() in ignored_values:
            print(f"found ignored value -> {tk.lower()}")
            continue
        print('-'*60)
        print(f"Palavra: {token.text}")
        # o "infinitivo" só deve ser mostrado caso seja um verbo,
        # caso seja outra classe de palavra, mostrar "Palavra sem declinação:"
        if token.pos_ == "VERB":
            print(f"Infinitivo: to {token.lemma_}")
        else:
            print(f"Palavra sem declinação/contração: {token.lemma_}")
        print(
            f"Classe gramatical: {spacy.explain(token.pos_)}" +
            (f" -> {data["pos_pt"].get(token.pos_)}" if token.pos_ in data["pos_pt"] else "") + "\n"
            f"Detalhes (tag): {spacy.explain(token.tag_)}" +
            (f" -> {data["verbo_tempo"].get(token.tag_, spacy.explain(token.tag_))}" if token.tag_ in data["verbo_tempo"] else "") + "\n"
            f"Dependência sintática: {spacy.explain(token.dep_)}" +
            (f" -> {data["dep_pt"].get(token.dep_, spacy.explain(token.dep_))}" if token.dep_ in data["dep_pt"] else "") + "\n" +
            "-"*60
        )
        match tag:
            case ["VBZ", "VBP"]:
                g_Simple_present.append(tk)
            case "VBG":
                g_Present_continuous.append(tk)
            case "VBD":
                g_Simple_past.append(tk)
            case "VBN":
                g_Past_participle.append(tk)
        time.sleep(1)
    return True

def classify_verbs():
    frase = "Não houveram verbos no"
     
    print("----- [VERBOS NO SIMPLE PRESENT] ----- (ex: runs)")
    if g_Simple_present:
        for word in g_Simple_present:
            print(" "*10 + "-"*5 + word + "-"*5)
    else:
        print(f"{frase} simple present")

    print("\n----- [VERBOS NO PRESENT CONTINUOUS] ----- (ex: running)")
    if g_Present_continuous:
        for word in g_Present_continuous:
            print(" "*10 + "-"*5 + word + "-"*5)
    else:
        print(f"{frase} simple continuous")

    print("\n----- [VERBOS NO SIMPLE PAST] ----- (ex: ran)")
    if g_Simple_past:
        for word in g_Simple_past:
            print(" "*10 + "-"*5 + word + "-"*5)
    else:
        print(f"{frase} simple past")

    print("\n----- [VERBOS NO PAST PARTICIPLE] ----- (ex: eaten)")
    if g_Past_participle:
        for word in g_Past_participle:
            print(" "*10 + "-"*5 + word + "-"*5)
    else:
        print(f"{frase} simple participle")
__init__()