#!/bin/sh
# setup ip address, subnet mask, and default gateway
if [ "$ip" ] && [ "$mask" ] && [ "$interface" ]; then
    ip addr add "$ip/$mask" dev "$interface"
fi

if [ "$router" ]; then
    ip route add default via "$router" dev "$interface"
fi

# debug
if [ "$interface" ]; then
    echo "DHCP configuration for $interface"
    echo ""
    echo "IP address: $ip"
    echo "Subnet mask: $mask"
    echo "Router: $router"
fi
