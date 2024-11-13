install-pox:
	cd src/lib && git clone http://github.com/noxrepo/pox && cd pox && git checkout origin/ichthyosaur && rm -rf .git

.PHONY: install-pox