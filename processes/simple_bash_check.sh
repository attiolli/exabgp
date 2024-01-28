#!/bin/bash
while true; do
    if systemctl is-active --quiet nfs-server; then
        echo "announce route 10.0.99.12 next-hop self"
    else
        echo "withdraw route 10.0.99.12 next-hop self"
    fi
    sleep 5
done
