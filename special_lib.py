import sys, json, spacy
from translate import Translator
import re

sys.stdout.reconfigure(encoding='utf-8'); 

tradutor = Translator(to_lang="pt-br")

def traduzir(frase):
    return tradutor.translate(frase)

g_Numerals = []
g_Pronouns = []

g_Simple_present = []
g_Present_continuous = []
g_Simple_past = []
g_Past_participle = []
g_Modal_Verbs = []

g_Ignored_values = []
g_Linking_words = []

try:
    with open("dicionarios.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print("Erro ao carregar 'dicionarios.json': " + str(e))


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
        if tk.lower() in ignored_values:
            tk += '\n'
            g_Ignored_values.append(tk.lower())
            continue
        content += f"\nPalavra #{i}: {token.text}"
        i+=1
        if token.pos_ == "VERB":
            content += f"\nInfinitivo: to {token.lemma_}"
        else:
            content += f"\nPalavra sem declinação/contração: {token.lemma_}"
        
        classe_pt = data.get("pos_pt", {}).get(token.pos_, "")
        detalhes_tag = data.get("verbo_tempo", {}).get(token.tag_, spacy.explain(token.tag_))
        dep_pt = data.get("dep_pt", {}).get(token.dep_, "")

        content += "\nClasse gramatical: " + str(spacy.explain(token.pos_))
        if classe_pt:
            content += " -> " + str(classe_pt)

        content += "\nDetalhes (tag): " + str(spacy.explain(token.tag_))
        if detalhes_tag:
            content += " -> " + str(detalhes_tag)

        content += "\nDependência sintática: " + str(spacy.explain(token.dep_))
        if dep_pt:
            content += " -> " + str(dep_pt)

        content += "\n" + "-" * 60
        content += '\n' + '-' * 60

        match tag:
            case "VBZ" | "VBP" | "VB":
                g_Simple_present.append(tk)
            case "VBG" | "UH":
                g_Present_continuous.append(tk)
            case "VBD":
                g_Simple_past.append(tk)
            case "VBN":
                g_Past_participle.append(tk)
            case "MD":
                g_Modal_Verbs.append(tk)
            case "CD":
                g_Numerals.append(tk)
            case "PRP":
                g_Pronouns.append(tk)

    return content

def clear_arrays() :
    g_Simple_present.clear()
    g_Present_continuous.clear()
    g_Simple_past.clear()
    g_Past_participle.clear()
    g_Modal_Verbs.clear()
    g_Numerals.clear()
    g_Pronouns.clear()
    g_Ignored_values.clear()

def classify_verbs():
    frase = "Não houveram verbos no"
    content = ""
    content += "----- [VERBOS NO SIMPLE PRESENT] ----- (ex: runs)\n"
    if g_Simple_present:
        for word in g_Simple_present:
            content += " "*10 + "-"*5 + word + "-"*5 + "\n"
    else:
        content += f"{frase} simple present\n"

    content += "\n----- [VERBOS MODAIS] ----- (ex: can, could...)\n"
    if g_Modal_Verbs:
        for modal in g_Modal_Verbs:
            content += " "*10 + "-"*5 + modal + "-"*5 + "\n"
    else:
        content += f"Não houveram verbos modais\n"

    content += "\n----- [VERBOS NO PRESENT CONTINUOUS] ----- (ex: running)\n"
    if g_Present_continuous:
        for word in g_Present_continuous:
            content += " "*10 + "-"*5 + word + "-"*5 + "\n"
    else:
        content += f"{frase} simple continuous\n"

    content += "\n----- [VERBOS NO SIMPLE PAST] ----- (ex: ran)\n"
    if g_Simple_past:
        for word in g_Simple_past:
            content += " "*10 + "-"*5 + word + "-"*5 + "\n"
    else:
        content += f"{frase} simple past\n"

    content += "\n----- [VERBOS NO PAST PARTICIPLE] ----- (ex: eaten)\n"
    if g_Past_participle:
        for word in g_Past_participle:
            content += " "*10 + "-"*5 + word + "-"*5 + "\n"
    else:
        content += f"{frase} simple participle\n"
    return content

def classify_rest(doc):
    frase = "Não houveram"
    content = "\n----- [NUMERAIS] ----- (ex: one, two, three...)\n"
    if g_Numerals:
        for numeral in g_Numerals:
            content += " "*10 + "-"*5 + numeral + "-"*5 + "\n"
    else :
        content += f"{frase} numerais\n"

    content += "\n----- [PRONOMES] ----- (ex: I, You, He...)\n"
    if g_Pronouns:
        for pron in g_Pronouns:
            content += " "*10 + "-"*5 + pron + "-"*5 + "\n"
    else:
        content += f"{frase} pronomes\n"

    content += "\n----- [LINKING WORDS] -----\n"
    found = False 

    for key in data['linking_words']:
        if  re.search(' '+ key+ ' ', doc.text, re.IGNORECASE):
            content += " "*10 + "-"*5 + key + "-"*5 + "\n"
            found = True
    
    if not found:
        content += f'{frase} linking words'

    return content