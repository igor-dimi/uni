VOCAB_IN ?= anki_export.tsv

vocab:
	python scripts/normalize_vocab.py --input $(VOCAB_IN) --csvout data/vocab.csv --jsonout data/vocab.json

# usage: make vocab VOCAB_IN=anki_export_2025-10-26.tsv
