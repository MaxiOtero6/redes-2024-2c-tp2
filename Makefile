NSWITCHES := 3

install-pox:
	git clone http://github.com/noxrepo/pox && cd pox && git checkout origin/ichthyosaur

mininet:
	sudo mn -c  # Clean up first
	sudo mn --custom ./topology.py --topo customTopo,${NSWITCHES}  --controller remote,ip=0.0.0.0,port=6633 -v debug

.PHONY: install-pox mininet
