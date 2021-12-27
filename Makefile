GITREV := $(shell git rev-parse HEAD)
.PHONY = cachebust build autobuild-ruddocom autobuild-manuelamador



build:
	cd src/manuelamador.policy/src/manuelamador/policy/theme && npm run build
	cd src/ruddocom.policy/src/ruddocom/policy/theme && npm run build

cachebust:
	# lines=$$(git status --porcelain | grep -v '[?][?]' | wc -l) ; if [ "$$lines" != "0" ] ; then echo Directory dirty, not busting >&2 ; exit 1 ; fi
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(GITREV)/|" src/ruddocom.policy/src/ruddocom/policy/theme/manifest.cfg
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(GITREV)/|" src/ruddocom.policy/src/ruddocom/policy/theme/index.html
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(GITREV)/|" src/manuelamador.policy/src/manuelamador/policy/theme/manifest.cfg
	sed -i "s|[+][+]unique[+][+][a-z0-9]*/|++unique++$(GITREV)/|" src/manuelamador.policy/src/manuelamador/policy/theme/index.html
	#git add -p
	#git commit -a

autobuild-ruddocom:
	cd src/ruddocom.policy/src/ruddocom/policy/theme/styles && npm run watch

	
autobuild-manuelamador:
	cd src/manuelamador.policy/src/manuelamador/policy/theme/styles && npm run watch
