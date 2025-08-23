import sys
sys.stdout.reconfigure(encoding='utf-8') #encoda caracteres especiais


import spacy
from dic import pos_pt, dep_pt, tag_pt, verbo_tempo #importa lib que eu fiz com as palavras traduzidas pra pt br

simple_present = []
present_continuous = []
simple_past = []
past_participle = []

with open("texto_a_ser_lido.txt", "r", encoding="utf-8") as f: 
    conteudo = f.read()


nlp = spacy.load("en_core_web_sm")
doc = nlp(conteudo)

for token in doc:
    tag = token.tag_
    tk = token.text
    
    print(
    f"Palavra: {token.text}\n"
    f"Infinitivo: {token.lemma_}\n"
    f"Classe gramatical: {spacy.explain(token.pos_)}" +
        (f" -> {pos_pt.get(token.pos_)}" if token.pos_ in pos_pt else "") + "\n"
    f"Detalhes (tag): {spacy.explain(token.tag_)}" +
        (f" -> {verbo_tempo.get(token.tag_, spacy.explain(token.tag_))}" if token.tag_ in verbo_tempo else "") + "\n"
    f"Dependência sintática: {spacy.explain(token.dep_)}" +
        (f" -> {dep_pt.get(token.dep_, spacy.explain(token.dep_))}" if token.dep_ in dep_pt else "") + "\n"
    "----------------------------------------"
)

    if tag in ["VBZ", "VBP"]:
        simple_present.append(tk)
    elif tag == "VBG":
        present_continuous.append(tk)
    elif tag == "VBD":
        simple_past.append(tk)
    elif tag == "VBN":
        past_participle.append(tk)

frase = "Não houveram palavras no"

print("Quais palavras estão no Simple Present? (ex: runs)")
if simple_present:
    print(simple_present)
else:
    print(f"{frase} simple present")

print("\nQuais palavras estão no Present Continuous? (ex: running)")
if present_continuous:
    print(present_continuous)
else:
    print(f"{frase} simple continuous")

print("\nQuais palavras estão no Simple Past? (ex: ran)")
if simple_past:
    print(simple_past)
else:
    print(f"{frase} simple past")

print("\nQuais palavras estão no Past Participle? (ex: eaten)")
if past_participle:
    print(past_participle)
else:
    print(f"{frase} simple participle")

