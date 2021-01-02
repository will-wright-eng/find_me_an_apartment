#!/bin/bash

cd /Volumes/boot
touch ssh
echo 'country=US # replace with your country code
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="WIFI_NETWORK_NAME"
    psk="WIFI_PASSWORD"
    key_mgmt=WPA-PSK
}' > wpa_supplicant.conf