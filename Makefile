all: checkable/luke.conllu

checkable/%.conllu: extract.py
	mkdir -p checkable
	python3 extract.py % | udapy -s ud.FixPunct > $@
