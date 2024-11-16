'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''
import os

from collections import namedtuple
from pox.lib.addresses import EthAddr
from pox.lib.util import dpidToStr
from pox.lib.revent import *
from pox.lib.addresses import IPAddr
import pox.openflow.libopenflow_01 as of
from pox.core import core

import pox.lib.packet as pkt
import json

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']

POLICY_FILE_PATH = "./firewall-policies.json"

DL_TYPE = {
    "ipv4": pkt.ethernet.IP_TYPE,
    "ipv6": pkt.ethernet.IPV6_TYPE
}

NW_PROTO = {
    "tcp": pkt.ipv4.TCP_PROTOCOL,
    "udp": pkt.ipv4.UDP_PROTOCOL
}


class Firewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        self.load_policies()
        log.info("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        self.set_policies(event)
        log.info("Firewall rules installed on %s", dpidToStr(event.dpid))

    def load_policies(self):
        """
        Load the firewall policies from the file
        """
        with open(POLICY_FILE_PATH, 'r') as f:
            self.policies = json.load(f)["discard_policies"]

    def set_policies(self, event):
        """
        Set the firewall policies on the event, if there is no nw_proto or dl_type in the policy, generate all variants
        """
        for policy in self.policies:

            policy_variants = [policy]
            if "nw_proto" not in policy:
                policy_variants = self._generate_variants(
                    policy_variants, "nw_proto", NW_PROTO.keys())

            if "dl_type" not in policy:
                policy_variants = self._generate_variants(
                    policy_variants, "dl_type", DL_TYPE.keys())

            for policy_variant in policy_variants:
                rule = self._rule_from_policy(policy_variant)
                event.connection.send(rule)

    def _rule_from_policy(self, policy):
        """
        Generate a rule from the policy
        """
        rule = of.ofp_flow_mod()

        for (field, value) in sorted(policy.items()):
            if policy.get('dl_type') == 'ipv6' and field != "dl_type":
                continue

            parsed_value = self._parse_field_value(field, value)

            if parsed_value is None:
                continue

            rule.match.__setattr__(field, parsed_value)
        return rule

    def _parse_field_value(self, field, value):
        """
        Parse the field value based on the field
        """
        match (field):
            case "tp_dst":
                return int(value)
            case "tp_src":
                return int(value)
            case "nw_proto":
                return NW_PROTO.get(value, None)
            case "nw_src":
                return IPAddr(value)
            case "nw_dst":
                return IPAddr(value)
            case "dl_type":
                return DL_TYPE.get(value, None)

    def _generate_variants(self, policies, field, values):
        """
        Generate all variants of the policies with the field set to the values
        """
        new_policies = []

        for policy in policies:
            for value in values:
                __policy = policy.copy()
                __policy[field] = value
                new_policies.append(__policy)

        return new_policies


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
