#!/bin/sh
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

if [ "${config:-}" ]
then
    echo "${config}" > /tmp/virtualpdu.conf
else
    cat > /tmp/virtualpdu.conf <<EOF
[global]
libvirt_uri=${libvirt_uri:-"test:///default"}
outlet_default_state=${outlet_default_state:-"ON"}

[pdu]
listen_address=${listen_address:-"0.0.0.0"}
listen_port=${listen_port:-"161"}
community=${community:-"public"}
ports=${ports:-"0:default"}
EOF
fi

exec virtualpdu /tmp/virtualpdu.conf
