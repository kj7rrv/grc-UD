import conllu

proiel_pos = {}

for name in ["dev", "test", "train"]:
    with open(f"UD_Ancient_Greek-PROIEL/grc_proiel-ud-{name}.conllu") as f:
        data = conllu.parse(f.read())

    for sentence in data:
        for word in sentence:
            pos = word["upos"]
            lemma = word["lemma"]
            if pos in ["CCONJ", "SCONJ"]:
                if lemma in proiel_pos:
                    if pos != proiel_pos[lemma]:
                        proiel_pos[lemma] = "?CONJ"
                else:
                    proiel_pos[lemma] = pos

macula_conjunctions = [
    "ἀλλά",
    "ἄρα",
    "ἆρα",
    "ἄχρι",
    "γάρ",
    "δέ",
    "δέ",
    "διό",
    "διόπερ",
    "διότι",
    "ἐάν",
    "ἐάνπερ",
    "εἰ",
    "εἴπερ",
    "εἴτε",
    "ἐπάν",
    "ἐπεί",
    "ἐπειδή",
    "ἐπειδήπερ",
    "ἕως",
    "ἤ",
    "ἡνίκα",
    "ἤπερ",
    "ἤτοι",
    "ἵνα",
    "καθά",
    "καθάπερ",
    "καθό",
    "καθότι",
    "καθώς",
    "καθώσπερ",
    "καί",
    "καί",
    "καίπερ",
    "καίτοι",
    "καίτοιγε",
    "κἀκεῖ",
    "κἀκεῖθεν",
    "κἄν",
    "μέν",
    "μέντοι",
    "μέχρι(ς)",
    "μή",
    "μηδέ",
    "μήποτε",
    "μήτε",
    "ὅθεν",
    "ὁπότε",
    "ὅπου",
    "ὅπως",
    "ὁσάκις",
    "ὅταν",
    "ὅτε",
    "ὅτι",
    "οὗ",
    "οὐδέ",
    "οὐκοῦν",
    "οὖν",
    "οὔτε",
    "πλήν",
    "πρίν",
    "πῶς",
    "τέ",
    "τοιγαροῦν",
    "τοίνυν",
    "ὡς",
    "ὡσεί",
    "ὥσπερ",
    "ὡσπερεί",
    "ὥστε",
]

macula_pos = {
    conjunction: proiel_pos.get(conjunction, "?CONJ")
    for conjunction in macula_conjunctions
}

print(macula_pos)
