#!/bin/bash
# PCH: A script to extract ip and let nbeyond know it.

echo "Starting vpn client to nbeyond, the ground control..."
sudo openvpn --script-security 2 --config /home/pi/Documents/OpenVPN/nbeyond.ovpn &
sleep 10
echo "The vpn connected."
echo "Now this PI gets ip on nbeyond vpn."
/usr/local/bin/HereOnNbeyond.py > /home/pi/Documents/Pis/$(GetIDofThisPi).txt
echo "Now this PI transfers the IP to nbeyond, the ground control server."
