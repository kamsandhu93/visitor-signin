# Ad-Hoc Connection On Raspberry Pi
Scripts and configs to setup ad-hoc connection on raspberry pi
## Project Dependencies
 - hostapd
 - dnsmasq

## Setup or Un-setup Ad-Hoc network
MAKE SURE YOU ARE IN THE ADHOC FOLDER
ONLY USE THIS SCRIPT ON RASPBERRY PI
```
./setup_adhoc.sh -t [operation type] -p [network passphrase]
<will ask for confirmation, press y to continue>
```
To setup ad-hoc, use operation type `set`
To un-setup ad-hoc, use operation type `unset`

**NOTE: Due to an update to hostapd. raspberry pi will automatically mask hostapd if an invalid country code is detected.**
To check for this issue run:
`sudo systemctl start hostapd`
The following message should appear:
`Failed to start hostapd.service: Unit hostapd.service is masked.`

To fix, run the following commands:
```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```

## How it works
The setup script does a few things.
### Disable Wifi
First it backups and replaces `/etc/network/interfaces` and `/etc/dhcpcd.conf`. This switches the wifi card (wlan0) from receiving to send out signal. The IP address of the wifi card is set to `192.158.1.1` with a networkmask of `255.255.255.0`.
### Setup SSID and Passphrase
This only sets the IP address. So `hostapd` is used to setup the SSID and Passphrase of the access point. The `hostapd.conf` is copied to `/etc/hostapd/hostapd.conf`. This config sets up SSID rpi3net with WPA2 encryption. The passphrase is inserted to the config via the bash script.
### Setup DHCP
The above two will create a working access point that devices can connect to. But, these devices will not be assigned IP addresses (connected device will assign some random IP address to themselves) due to no [DHCP server](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol). This means unless we manually set the correct IP addresses (in this case 192.168.1.x), the devices would not be able to access websites/services hosted on the pi.
Using `dnsmasq`, we can setup a DHCP server to automatically assign IP addresses. `dnsmasq.conf` will be copied to `/etc/dnsmasq.conf`. This creates an IP range of 192.168.1.2 to 192.168.1.3 (so max two devices can connect) with a lease time of 24h.
### Lease Time
When a device connects to the pi, the DHCP server reserves an IP address for the device. Even when the device disconnects, the DHCP server maintains that reservation until the lease time is up (in this case, if you connect two devices to the pi, you cannot connect a third until you disconnect one device and wait 24 hours). The lease can be manually deleted by deleting the entry in `/var/lib/misc/dnsmasq.leases`
