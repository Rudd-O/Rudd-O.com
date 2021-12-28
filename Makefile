ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
HASH_RUDDOCOM := $(shell cd $(ROOT_DIR) && ./build/hash ruddocom.policy)
HASH_MANUELAMADOR := $(shell cd $(ROOT_DIR) && ./build/hash manuelamador.policy)
.PHONY = all build autobuild-ruddocom autobuild-manuelamador


all: \
  .cachebust/manuelamador/$(HASH) \
  .cachebust/ruddocom/$(HASH) \

.cachebust/manuelamador/$(HASH): \
  Makefile \
  build/hash \
  src/manuelamador.policy/src/manuelamador/policy/theme/styles/theme.min.css
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/manuelamador.policy/src/manuelamador/policy/theme/manifest.cfg
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/manuelamador.policy/src/manuelamador/policy/theme/index.html
	rm -rf .cachebust/manuelamador
	mkdir -p .cachebust/manuelamador
	touch .cachebust/manuelamador/$(HASH_MANUELAMADOR)

.cachebust/ruddocom/$(HASH): \
  Makefile \
  build/hash \
  src/ruddocom.policy/src/ruddocom/policy/theme/styles/theme.min.css
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/ruddocom.policy/src/ruddocom/policy/theme/manifest.cfg
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/ruddocom.policy/src/ruddocom/policy/theme/index.html
	rm -rf .cachebust/ruddocom
	mkdir -p .cachebust/ruddocom
	touch .cachebust/ruddocom/$(HASH_RUDDOCOM)

src/ruddocom.policy/src/ruddocom/policy/theme/styles/theme.min.css: \
  src/ruddocom.policy/src/ruddocom/policy/theme/styles/theme.scss \
  src/ruddocom.policy/src/ruddocom/policy/theme/styles/custom.scss \
  src/ruddocom.policy/src/ruddocom/policy/theme/node_modules/@plone/plonetheme-barceloneta-base/package.json
	cd src/ruddocom.policy/src/ruddocom/policy/theme && npm run build

src/manuelamador.policy/src/manuelamador/policy/theme/styles/theme.min.css: \
  src/manuelamador.policy/src/manuelamador/policy/theme/styles/theme.scss \
  src/manuelamador.policy/src/manuelamador/policy/theme/styles/custom.scss \
  src/manuelamador.policy/src/manuelamador/policy/theme/node_modules/@plone/plonetheme-barceloneta-base/package.json
	cd src/manuelamador.policy/src/manuelamador/policy/theme && npm run build

src/ruddocom.policy/src/ruddocom/policy/theme/node_modules/@plone/plonetheme-barceloneta-base/package.json:
	cd src/ruddocom.policy/src/ruddocom/policy/theme && npm install

src/manuelamador.policy/src/manuelamador/policy/theme/node_modules/@plone/plonetheme-barceloneta-base/package.json:
	cd src/manuelamador.policy/src/manuelamador/policy/theme && npm install

autobuild-ruddocom:
	cd src/ruddocom.policy/src/ruddocom/policy/theme/styles && npm run watch
	
autobuild-manuelamador:
	cd src/manuelamador.policy/src/manuelamador/policy/theme/styles && npm run watch
