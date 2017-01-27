virtualpdu-container
====================

This project builds a Docker image running
[VirtualPDU](http://github.com/openstack/virtualpdu), a Power
Distrbution Unit (PDU) simulator.

As of today, only the SNMPv2 protocol over UDP is supported and it has
the ability simulates the following PDUs:
 - [APC Rack PDU](https://github.com/openstack/virtualpdu/blob/master/virtualpdu/pdu/apc_rackpdu.py)
 - [Baytech MRP27 PDU](https://github.com/openstack/virtualpdu/blob/master/virtualpdu/pdu/baytech_mrp27.py)


Usage
-----

To configure the service, some environment variables must be set.
It is possible to pass a complete configuration to simulate
multiple units or only the settings to override if there is only one
unit to simulate.


### Full configuration ###

In this mode, the `config` environment variable must be set with the
content of the configuration file that
[VirtualPDU](http://github.com/openstack/virtualpdu) expects.

Example from docker-compose.yml:

    services:
      virtualpdu:
        image: "internap/virtualpdu:latest"
        ports:
         - '9997:9997/udp'
        environment:
          config: |
            [global]
            libvirt_uri=test:///default
            outlet_default_state=ON

            [my_second_pdu]
            listen_address=0.0.0.0
            listen_port=9997
            community=public
            ports=2:test


### Single PDU configuration ###

In this mode, only the configuration that needs to be changed has to be
declared as an environment variable.

| Variable               | Default value   |
|------------------------|-----------------|
| `outlet_default_state` | ON              |
| `libvirt_uri`          | test:///default |
| `listen_address`       | 0.0.0.0         | 
| `listen_port`          | 161             |
| `community`            | public          |
| `ports`                | 0:default       |

**Example from docker-compose.yml:**

    services:
      virtualpdu:
        image: "internap/virtualpdu:latest"
        ports:
         - '9997:9997/udp'
        environment:
          libvirt_uri: test:///default
          outlet_default_state: OFF
          listen_address: 0.0.0.0
          listen_port: 9997
          community: public
          ports: 2:test


Advanced usage with [libvirt](http://libvirt.org/)
--------------------------------------------------

By default, the simulator will not interact with outside resources, unless
a [proper `libvirt_uri`](http://libvirt.org/uri.html) is defined, and
a `outlet:domain` mapping is provided in the `ports` environment variable.
In that case, the corresponding libvirt domain will be started and stopped
based on the outlet state.

This container image does not provide a libvirt-server, it's up to the
user to provide their own libvirt provider.
