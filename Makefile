.PHONY = cachebust build


cachebust:
	# lines=$$(git status --porcelain | grep -v '[?][?]' | wc -l) ; if [ "$$lines" != "0" ] ; then echo Directory dirty, not busting >&2 ; exit 1 ; fi
	GITREV=$$(git rev-parse HEAD) && echo sed -i "s|/[+][+]unique[+][+][a-z0-9]*/|/++unique++$$GITREV/|" src/ruddocom.policy/src/ruddocom/policy/theme/manifest.cfg && sed -i "s|/[+][+]unique[+][+][a-z0-9]*/|/++unique++$$GITREV/|" src/ruddocom.policy/src/ruddocom/policy/theme/manifest.cfg
	#git add -p
	#git commit -a

autobuild:
	cd src/ruddocom.policy/src/ruddocom/policy/theme/styles && npm run watch
