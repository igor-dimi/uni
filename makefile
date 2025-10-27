# ===== Root Makefile (placed at repo root) =====
# Usage examples:
#   make vocab                     # rebuild CSV/JSON for current semester course
#   make render                    # render the whole site
#   make publish                   # rebuild + render + publish to gh-pages
#   make SEM=ss25 COURSE=spn vocab # switch semester/course on the fly

# ---------- config (override on CLI if needed) ----------
SEM        ?= ws25-26
COURSE     ?= spn
VOCAB_DIR   = $(SEM)/$(COURSE)/vocab
DATA_DIR    = $(VOCAB_DIR)/data
SCRIPTS_DIR = $(VOCAB_DIR)/scripts

PYTHON     ?= python
QUARTO     ?= quarto

# Source + outputs
VOCAB_IN   ?= $(DATA_DIR)/anki_export.tsv
CSV         = $(DATA_DIR)/vocab.csv
JSON        = $(DATA_DIR)/vocab.json
NORMALIZER  = $(SCRIPTS_DIR)/normalize_vocab.py

# ---------- phony targets ----------
.PHONY: all vocab render preview clean publish checktools

all: vocab render

checktools:
	@command -v $(PYTHON) >/dev/null || { echo "Error: python not found"; exit 1; }
	@command -v $(QUARTO) >/dev/null || { echo "Error: quarto not found"; exit 1; }

# ---------- vocab build pipeline ----------
vocab: $(CSV) $(JSON)

$(CSV) $(JSON): $(VOCAB_IN) $(NORMALIZER) | checktools
	$(PYTHON) $(NORMALIZER) --input $(VOCAB_IN) --csvout $(CSV) --jsonout $(JSON)
	@echo "Vocab normalized → $(CSV) and $(JSON)"

# ---------- site lifecycle ----------
render: | checktools
	$(QUARTO) render

preview: | checktools
	$(QUARTO) preview

clean: | checktools
	$(QUARTO) clean

publish: vocab render | checktools
	# Publish to gh-pages; adjust flags if you prefer prompts
	$(QUARTO) publish gh-pages --no-browser
