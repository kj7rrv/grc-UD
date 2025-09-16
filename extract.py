import os
import csv
import traceback
from lxml import etree

def get_head(node):
    '''Return the index of the child that is the head of this phrase.'''
    if False: # add checks that modify the default structure here
        return 0
    # by default, keep what's already there
    return int(node.attrib.get('Head', 0))

def get_id(node):
    xml_id = '{http://www.w3.org/XML/1998/namespace}id'
    return node.attrib.get('nodeId', node.attrib.get(xml_id))

def propagate_heads(node):
    for ch in node:
        propagate_heads(ch)
    if len(node) == 0:
        node.attrib['PhraseHead'] = get_id(node)
    else:
        head = get_head(node)
        node.attrib['PhraseHeadIndex'] = str(head)
        node.attrib['PhraseHead'] = node[head].attrib['PhraseHead']

def distribute_heads(node, headword):
    if len(node) == 0:
        if headword == get_id(node):
            node.attrib['headword'] = '0'
        else:
            node.attrib['headword'] = headword
    else:
        head = int(node.attrib['PhraseHeadIndex'])
        for i, ch in enumerate(node):
            if i == head:
                distribute_heads(ch, headword)
            else:
                distribute_heads(ch, node.attrib['PhraseHead'])

def iter_words(node):
    if len(node) == 0:
        yield node
    else:
        for ch in node:
            yield from iter_words(ch)

FEAT_MAP = {
    'Case': ('Case', {
        'Nominative': 'Nom',
        'Accusative': 'Acc',
        'Dative': 'Dat',
        'Genitive': 'Gen',
        'Vocative': 'Voc',
    }),
    'Gender': ('Gender', {
        'Masculine': 'Masc',
        'Feminine': 'Fem',
        'Neuter': 'Neut',
    }),
    'Number': ('Number', {
        'Singular': 'Sing',
        'Plural': 'Plur',
    }),
}

def get_feats(node):
    ret = {}
    for key in FEAT_MAP:
        if key in node.attrib:
            ret[FEAT_MAP[key][0]] = FEAT_MAP[key][1].get(node.attrib[key])
    return ret

def get_misc(node):
    ret = {}
    if 'Gloss' in node.attrib:
        ret['Gloss'] = node.attrib['Gloss']
    return ret

def split_crasis(word):
    # if `word` is crasis, return a list of pieces with morph info
    # put the ID (field 0) on the one that should be the head
    # the HEAD (field 6) of the other word will presumably have the
    # same value
    return None

def process_sentence(sent, file):
    propagate_heads(sent)
    distribute_heads(sent, sent.attrib['PhraseHead'])
    xml_words = sorted(iter_words(sent), key=get_id)
    conllu_words = []
    for word in xml_words:
        line = [
            get_id(word),                     # ID
            word.text,                        # FORM
            word.attrib.get('UnicodeLemma'),  # LEMMA
            word.attrib.get('upos', '_'),     # UPOS
            word.attrib.get('Cat', '_'),      # XPOS
            get_feats(word),                  # FEATS
            word.attrib.get('headword', '_'), # HEAD
            word.attrib.get('deprel', '_'),   # DEPREL
            '_',                              # DEPS
            get_misc(word),                   # MISC
        ]
        punct = None
        if line[1][-1] in ',.':
            punct = line[1][-1]
            line[1] = line[1][:-1]
            line[9]['SpaceAfter'] = 'No'
        cr = split_crasis(line)
        if cr:
            for w in cr:
                if 'SpaceAfter' in w[9]:
                    del w[9]['SpaceAfter']
            gp = [len(cr), line[1], '_', '_', '_', {}, '_', '_', '_', {}]
            if punct:
                gp[9]['SpaceAfter'] = 'No'
            conllu_words.append(gp)
            conllu_words += cr
        else:
            conllu_words.append(line)
        if punct:
            conllu_words.append(['_', punct, punct, 'PUNCT', '_',
                                 {}, get_id(word), 'punct', '_', {}])
    id2idx = {'0': '0'}
    n = 0
    for word in conllu_words:
        if isinstance(word[0], int):
            word[0] = f'{n+1}-{n+word[0]}'
        else:
            n += 1
            if word[0] != '_':
                id2idx[word[0]] = str(n)
            word[0] = str(n)
    for word in conllu_words:
        word[6] = id2idx.get(word[6], '_')
    ref = sent.attrib['ref']
    book, verses = ref.split()
    start, end = verses.split('-')
    v1 = start.split('!')[0]
    v2 = end.split('!')[0]
    sent_id = book + '-' + v1
    if start != v1 + '!1':
        sent_id += '_' + start.split('!')[1] # TODO
    if v1 != v2:
        sent_id += '-' + v2
    print('# sent_id =', sent_id, file=file)
    for word in conllu_words:
        pieces = []
        for piece in word:
            if isinstance(piece, dict):
                srt = sorted(piece.items(), key=lambda t: t[0].lower())
                pieces.append('|'.join(f'{k}={v}' for k, v in srt) or '_')
            else:
                pieces.append(str(piece))
        print('\t'.join(pieces), file=file)
    print('', file=file)

if __name__ == '__main__':
    for fname in sorted(os.listdir('macula-greek/SBLGNT/nodes/')):
        print(fname, end=" ")
        path = "macula-greek/SBLGNT/nodes/" + fname
        tree = etree.parse(path)
        # TODO: merge sentences that are part of the same verse
        try:
            with open("conv-macula/" + fname.replace(".xml", ".conllu"), "w", encoding="utf-8") as f:
                for sent in tree.getroot().iter('Sentence'):
                    process_sentence(sent, f)
            print("OK")
        except Exception:
            print("FAILED (traceback below)")
            print(traceback.format_exc())
            print("END TRACEBACK")
