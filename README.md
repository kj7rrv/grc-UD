# grc-UD

Conversion of MACULA Greek NT data to UD/ConLL-U format

`extract.py` will extract the treebank from the MACULA XML files and store the
extracted data in ConLL-U files under `conv-macula/`.

Currently, most dependency relationships are not converted. My plan is to
convert them from the MACULA data, but this is not yet implemented; it will
take some work because of the different format used. MACULA groups words
together into nodes and relates these multi-word nodes together; UD relates
each word to one other word. The relationships that are tagged in the current
output are determined using rules based on parts of speech.

Also, many conjunctions are tagged as `?CONJ` rather than the correct `CCONJ`
(coordinating) or `SCONJ` (subordinating). This is because the MACULA data does
not consider them separate parts of speech, but UD does, and the extraction
script must disambiguate them using a dictionary of conjunctions. The current
disambiguated entries in the dictionary are extracted from the UD PROIEL
treebank using the script in `data_gathering/conj_pos.py`.
