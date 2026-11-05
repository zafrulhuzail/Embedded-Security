#!/usr/bin/env bash
set -euo pipefail

BOARD_IP="192.168.13.13"
HOST_IP="192.168.13.17/24"

if [[ ${EUID} -eq 0 ]]; then
  echo "Run this script as your normal user, not with sudo." >&2
  exit 1
fi

if [[ $# -gt 1 ]]; then
  echo "Usage: $0 [ethernet-interface]" >&2
  exit 1
fi

if [[ $# -eq 1 ]]; then
  IFACE="$1"
else
  echo "Available network interfaces:"
  ip -br link show
  echo
  read -r -p "Enter the USB Ethernet interface name (e.g. enx... or eth1): " IFACE
fi

if [[ -z "$IFACE" || "$IFACE" == "lo" || ! -d "/sys/class/net/$IFACE" ]]; then
  echo "Invalid network interface: $IFACE" >&2
  exit 1
fi

printf '\nConfiguring %s for the STM32 board...\n' "$IFACE"
sudo ip link set dev "$IFACE" up
if ! ip -4 addr show dev "$IFACE" | grep -Fq "inet $HOST_IP "; then
  sudo ip addr add "$HOST_IP" dev "$IFACE"
fi

printf '\nTesting board connectivity (%s)...\n' "$BOARD_IP"
if ping -I "$IFACE" -c 4 -W 2 "$BOARD_IP"; then
  echo "Board is reachable."
else
  echo "Board did not respond. Check power, Ethernet cable, USB adapter passthrough, and interface selection." >&2
  exit 1
fi

read -r -p "Connect via SSH as root? [Y/n] " ANSWER
if [[ -z "$ANSWER" || "$ANSWER" =~ ^[Yy]$ ]]; then
  echo "The lab notebook lists the board's root password as: root"
  ssh "root@$BOARD_IP"
fi
