# Copyright (c) 2016 Red Hat Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_lib.api.definitions import portbindings
from neutron_lib import constants
from neutron_lib.db import constants as db_consts
from neutron_lib.services.qos import base
from neutron_lib.services.qos import constants as qos_consts
from oslo_log import log as logging


LOG = logging.getLogger(__name__)

DRIVER = None

SUPPORTED_RULES = {
    qos_consts.RULE_TYPE_BANDWIDTH_LIMIT: {
        qos_consts.MAX_KBPS: {
            'type:range': [0, db_consts.DB_INTEGER_MAX_VALUE]},
        qos_consts.MAX_BURST: {
            'type:range': [0, db_consts.DB_INTEGER_MAX_VALUE]},
        qos_consts.DIRECTION: {
            'type:values': [constants.EGRESS_DIRECTION]}
    },
    qos_consts.RULE_TYPE_MINIMUM_BANDWIDTH: {
        qos_consts.MIN_KBPS: {
            'type:range': [0, db_consts.DB_INTEGER_MAX_VALUE]},
        qos_consts.DIRECTION: {'type:values': constants.VALID_DIRECTIONS}
    }
}


class SRIOVNICSwitchDriver(base.DriverBase):

    @staticmethod
    def create():
        return SRIOVNICSwitchDriver(
            name='sriovnicswitch',
            vif_types=[portbindings.VIF_TYPE_HW_VEB],
            vnic_types=[portbindings.VNIC_DIRECT,
                        portbindings.VNIC_MACVTAP,
                        portbindings.VNIC_DIRECT_PHYSICAL],
            supported_rules=SUPPORTED_RULES,
            requires_rpc_notifications=True)


def register():
    """Register the driver."""
    global DRIVER
    if not DRIVER:
        DRIVER = SRIOVNICSwitchDriver.create()
    LOG.debug('SR-IOV NIC Switch QoS driver registered')
