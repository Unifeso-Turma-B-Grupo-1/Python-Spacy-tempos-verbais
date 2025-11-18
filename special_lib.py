import sys, json, spacy
from translate import Translator

sys.stdout.reconfigure(encoding='utf-8'); #encoda caracteres especiais

#tradutor de string
tradutor = Translator(to_lang="pt-br")

def traduzir(frase):
    return tradutor.translate(frase)

# arrays para tempos verbais
g_Simple_present = []
g_Present_continuous = []
g_Simple_past = []
g_Past_participle = []

# array para valores ignorados
g_Ignored_values = []

#carregando json
try:
    with open("dicionarios.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print("Erro ao carregar 'dicionarios.json': " + e)
    
# func pra mostrar o conteudo do spacy doc
def show_content(doc):
    ignored_values = data["ignore"].values()
    ignorados = 0
    for c in doc:
        if c.text.lower() in ignored_values:
            ignorados+=1
    content = f"-> Foram encontradas {len(doc)-ignorados} palavras no seu texto!"
    i = 1
    for token in doc:
        tag = token.tag_
        tk = token.text
        # ignorar caracteres inuteis para a análise
        if tk.lower() in ignored_values:
            tk += '\n'
            g_Ignored_values.append(tk.lower())
            continue
        content += f"\nPalavra #{i}: {token.text}"
        i+=1
        # o "infinitivo" só deve ser mostrado caso seja um verbo,
        # caso seja outra classe de palavra, mostrar "Palavra sem declinação:"
        if token.pos_ == "VERB":
            content += f"\nInfinitivo: to {token.lemma_}"
        else:
            content += f"\nPalavra sem declinação/contração: {token.lemma_}"
        content += f"\nClasse gramatical: {spacy.explain(token.pos_)}" + f" -> {data["pos_pt"].get(token.pos_)}" if token.pos_ in data["pos_pt"] else "" + "\n" + f"Detalhes (tag): {spacy.explain(token.tag_)}" + f" -> {data["verbo_tempo"].get(token.tag_, spacy.explain(token.tag_))}" if token.tag_ in data["verbo_tempo"] else "" + "\n" f"Dependência sintática: {spacy.explain(token.dep_)}" + f" -> {data["dep_pt"].get(token.dep_, spacy.explain(token.dep_))}" if token.dep_ in data["dep_pt"] else "" + "\n" + "-"*60
        content += '\n' + '-'*65
        match tag:
            case ["VBZ", "VBP"]:
                g_Simple_present.append(tk)
            case "VBG":
                g_Present_continuous.append(tk)
            case "VBD":
                g_Simple_past.append(tk)
            case "VBN":
                g_Past_participle.append(tk)
    return content

def classify_verbs():
    frase = "Não houveram verbos no"
    content = ""
    content += "----- [VERBOS NO SIMPLE PRESENT] ----- (ex: runs)\n"
    if g_Simple_present:
        for word in g_Simple_present:
            content += " "*10 + "-"*5 + word + "-"*5
    else:
        content += f"{frase} simple present"

    content += "\n----- [VERBOS NO PRESENT CONTINUOUS] ----- (ex: running)\n"
    if g_Present_continuous:
        for word in g_Present_continuous:
            content += " "*10 + "-"*5 + word + "-"*5
    else:
        content += f"{frase} simple continuous"

    content += "\n----- [VERBOS NO SIMPLE PAST] ----- (ex: ran)\n"
    if g_Simple_past:
        for word in g_Simple_past:
            content += " "*10 + "-"*5 + word + "-"*5
    else:
        content += f"{frase} simple past"

    content += "\n----- [VERBOS NO PAST PARTICIPLE] ----- (ex: eaten)\n"
    if g_Past_participle:
        for word in g_Past_participle:
            content += " "*10 + "-"*5 + word + "-"*5
    else:
        content += f"{frase} simple participle"
    return content
