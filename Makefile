NSWITCHES := 3

install-pox:
	git clone http://github.com/noxrepo/pox && cd pox && git checkout origin/ichthyosaur

mininet:
	sudo mn -c  # Clean up first
	sudo mn --custom ./topology.py --topo customTopo,switches=${NSWITCHES} --controller remote,ip=127.0.0.1,port=6633 

make run-pox:
	python3 ./pox.py firewall


.PHONY: install-pox mininet run-pox
