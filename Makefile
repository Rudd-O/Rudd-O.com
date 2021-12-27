HASH := $(shell ./build/hash)
.PHONY = all build autobuild-ruddocom autobuild-manuelamador


all: \
  build \
  .cachebust/$(HASH)

.cachebust/$(HASH):
	mkdir -p .cachebust
	touch .cachebust/$(HASH)
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/ruddocom.policy/src/ruddocom/policy/theme/manifest.cfg
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/ruddocom.policy/src/ruddocom/policy/theme/index.html
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/manuelamador.policy/src/manuelamador/policy/theme/manifest.cfg
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(HASH)/|" src/manuelamador.policy/src/manuelamador/policy/theme/index.html

build: \
  src/ruddocom.policy/src/ruddocom/policy/theme/styles/theme.min.css \
  src/manuelamador.policy/src/manuelamador/policy/theme/styles/theme.min.css

src/ruddocom.policy/src/ruddocom/policy/theme/node_modules/@plone/plonetheme-barceloneta-base/package.json:
	cd src/ruddocom.policy/src/ruddocom/policy/theme && npm install

src/manuelamador.policy/src/manuelamador/policy/theme/node_modules/@plone/plonetheme-barceloneta-base/package.json:
	cd src/manuelamador.policy/src/manuelamador/policy/theme && npm install

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

autobuild-ruddocom:
	cd src/ruddocom.policy/src/ruddocom/policy/theme/styles && npm run watch
	
autobuild-manuelamador:
	cd src/manuelamador.policy/src/manuelamador/policy/theme/styles && npm run watch
