# Copyright 2017 Internap
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import signal
import subprocess
import sys
import time
import unittest

from pyasn1.type import univ
from pysnmp.entity.rfc3413.oneliner import cmdgen

from tests import snmp_client

ON = univ.Integer(1)
OFF = univ.Integer(2)

APC_RACK_PDU_BASE = (1, 3, 6, 1, 4, 1, 318, 1, 1, 12)
OUTLET_CONTROL_COMMAND = APC_RACK_PDU_BASE + (3, 3, 1, 1, 4)


class TestDockerImage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        docker_compose('build', stdout=subprocess.PIPE).communicate()

    def setUp(self):
        self.process = docker_compose('up', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sys.stdout.write(self.process.stdout.readline().decode())  # Wait for first pdu
        sys.stdout.write(self.process.stdout.readline().decode())  # Wait for second pdu
        sys.stdout.write(self.process.stdout.readline().decode())  # Wait for third pdu
        time.sleep(1)

    def tearDown(self):
        self.assertIsNone(self.process.poll())
        self.process.send_signal(signal.SIGINT)
        stdout, _ = self.process.communicate()
        sys.stdout.write(stdout.decode())
        docker_compose('down').communicate()

    def test_happy_path(self):
        _turn_on_outlet(outlet=2, port=9997)
        _turn_off_outlet(outlet=2, port=9997)

        _turn_on_outlet(outlet=5, port=9998)
        _turn_off_outlet(outlet=5, port=9998)

        _turn_on_outlet(outlet=3, port=9999, community='private')
        _turn_off_outlet(outlet=3, port=9999, community='private')


def _turn_on_outlet(outlet, port, listen_address='127.0.0.1', community='public'):
    outlet = OUTLET_CONTROL_COMMAND + (outlet,)
    snmp = snmp_client.SnmpClient(
        cmdgen, listen_address, port, community, timeout=1, retries=1)
    snmp.set(outlet, ON)


def _turn_off_outlet(outlet, port, listen_address='127.0.0.1', community='public'):
    outlet = OUTLET_CONTROL_COMMAND + (outlet,)
    snmp = snmp_client.SnmpClient(
        cmdgen, listen_address, port, community, timeout=1, retries=1)
    snmp.set(outlet, OFF)


def docker_compose(*args, **kwargs):
    docker_compose_path = os.path.join(os.path.dirname(sys.executable), 'docker-compose')
    process = subprocess.Popen((docker_compose_path,) + args, **kwargs)
    return process
