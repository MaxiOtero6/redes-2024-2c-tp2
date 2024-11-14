# TINCHOOOOOOOO

from mininet.topo import Topo


MAX_HOSTS = 4


class MyTopo(Topo):
    def __init__(self, _switches):
        # Initialize topology
        Topo.__init__(self)

        hosts = [self.addHost(f'h{i}') for i in range(1, MAX_HOSTS + 1)]
        switches = [self.addHost(f's{i}') for i in range(1, _switches + 1)]

        self.addLink(hosts[0], switches[0])
        self.addLink(hosts[1], switches[0])
        self.addLink(hosts[2], switches[-1])
        self.addLink(hosts[3], switches[-1])

        [
            self.addLink(switches[i], switches[i + 1])
            for i in range(len(switches))
        ]


topos = {"customTopo": MyTopo}
