# ADS-B Setup

### Is my dongle working?

```bash
sudo apt-get install rtl-sdr
rtl_test -t
# If you see this error
# usb_open error -3
# Please fix the device permissions, e.g. by installing the udev rules file rtl-sdr.rules
sudo wget -O /etc/udev/rules.d/rtl-sdr.rules "https://raw.githubusercontent.com/osmocom/rtl-sdr/master/rtl-sdr.rules"
```

### Basic Setup

*Mostly taken from gist: [rpi-adsb-feeder.md](https://gist.github.com/kanchudeep/2068aa149b1f787f8f77d7b785de304a)*

```bash
wget https://uk.flightaware.com/adsb/piaware/files/packages/pool/piaware/p/piaware-support/piaware-repository_7.2_all.deb
sudo dpkg --install piaware-repository_7.2_all.deb
sudo apt update
sudo apt install dump1090-fa lighttpd piaware
# check piaware at http://my_ip:8080/
```

#### piaware commands

```bash
# allow updates
sudo piaware-config allow-auto-updates yes
sudo piaware-config allow-manual-updates yes
# check config
piaware-config -showall
# Is it running?
piaware-status
systemctl status piaware
# restart piaware
sudo systemctl restart piaware
# Keep old feeder-id on a new install
sudo piaware-config feeder-id UUID
sudo systemctl restart piaware
# See the json
http://my_ip:8080/data/aircraft.json
# See the receiver's json
http://my_ip:8080/data/receiver.json
# See the stats json
http://my_ip:8080/data/stats.json
```

* Claim new client: [flightaware.com/adsb/piaware/claim](https://flightaware.com/adsb/piaware/claim)
* View your page: [https://flightaware.com/account/manage](https://flightaware.com/account/manage)

#### adsbexchange

* Steps taken from [github.com/adsbxchange/adsb-exchange](https://github.com/adsbxchange/adsb-exchange)

```bash
wget -O /tmp/axfeed.sh https://adsbexchange.com/feed.sh
sudo bash /tmp/axfeed.sh
# web interface (Go to http://my_ip/adsbx)
sudo bash /usr/local/share/adsbexchange/git/install-or-update-interface.sh
# check status
sudo systemctl status adsbexchange-feed
# restart feed
sudo systemctl restart adsbexchange-feed
# uninstall
sudo bash /usr/local/share/tar1090/uninstall.sh adsbx
```


* check feed status [adsbexchange.com/myip/](https://adsbexchange.com/myip/) | [adsbx.org/sync](http://adsbx.org/sync)

#### FlightRadar24

```
sudo bash -c "$(wget -O - https://repo-feed.flightradar24.com/install_fr24_rpi.sh)"
# Restart fr24feed
sudo systemctl restart fr24feed
# Info page
http://my_ip:8754/
```

#### Add-ons

```
# Install graph
sudo bash -c "$(curl -L -o - https://github.com/wiedehopf/graphs1090/raw/master/install.sh)"
# view graphs
http://192.168.x.yy/graphs1090
http://192.168.x.yy/perf
http://192.168.x.yy:8542
# Normal means of shutting down pi will cause data loss. Run this instead:
sudo shutdown now
```

### Todo

* Take pictures of the planes that fly by [github.com/IQTLabs/SkyScan](https://github.com/IQTLabs/SkyScan)
* Stats logger: 
  * https://github.com/nfacha/adsb-stats-logger
  * https://www.reddit.com/r/ADSB/comments/rutot0/python3_script_to_profile_dump1090_output_and/
* Monitoring
  * Telegraf
  * Python script to query receiver and send stats to Influx, [github.com/jmoekamp/adsb2influx](https://github.com/jmoekamp/adsb2influx/blob/main/adsb2influx.py)
* Get IP address via JS: [stackOverflow](https://stackoverflow.com/questions/3653065/get-local-ip-address-in-node-js)
* Antennas
  * DIY Spider antenna [forum.flightradar24.com](https://forum.flightradar24.com/forum/radar-forums/technical-matters-hardware/10396-quick-spider-no-soldering-no-connector)
  * [Coaxial Collinear Antenna for ADS-B Receiver](https://www.balarad.net/)
* [wiedehopf shopping list](https://github.com/wiedehopf/adsb-wiki/wiki/adsb-receiver-shopping-list)

### Resources

* Dump1090 Documentation (get the JSON)
  [SDRplay Github](https://github.com/SDRplay/dump1090/blob/master/README-json.md)
* Reddit
  * 978 and 1090, with monitoring, POE, and grounding [here](https://www.reddit.com/r/RTLSDR/comments/qzpp0q/latest_iteration_of_my_adsb_feeder_box_based_on/) and [here](https://www.reddit.com/r/ADSB/comments/qzpnwy/latest_iteration_of_my_adsb_feeder_box_based_on/)
  * [Remote receiver](https://m0taz.co.uk/2020/07/raspberry-pi4-remote-mount-adsb-receiver/), how to deal with power, discussion [here](https://www.reddit.com/r/ADSB/comments/i2eryr/outdoor_adsb_receiver_with_no_rx_coax_loss/)
  * 978 and 1090, proper grounding, LNA [here](https://www.reddit.com/r/ADSB/comments/lg9p7n/before_and_after/)
  * [Outdoor installation](https://www.reddit.com/r/raspberry_pi/comments/uhxt5k/finally_moved_the_piaware_outside/), using PG9 cable glands for cables into box
* [ADS-B FlightAware Enclosure Build](https://imgur.com/gallery/dpyGo) - and [reddit discussion](https://www.reddit.com/r/RTLSDR/comments/7pkso6/)
* [My ADS-B Setup - PiAware](https://www.reddit.com/r/ADSB/comments/akk01c/)






<!--

### potential shopping list

* If the cable is N-Type to N-Type:
  * Combine surge protector and cable: [400-Series N-Male to N-Male In-Line Lightning Protector Cable Assemblies](http://www.l-com.com/surge-protector-400-series-n-male-to-n-male-in-line-lightning-protector-cable-assemblies)
  * N-Male to N-SMA adapter. Options: [JEFA Tech Adapter](https://www.amazon.com/dp/B001GUSCH6/) | [Phonetone N male to SMA female](https://www.amazon.com/dp/B00KL6PXMI/)
* If the cable is N-Type to SMA:
  * Cable option: [MPD Digital LMR-400 Coaxial Antenna Cable Line with N Male & SMA Male Connectors](https://www.amazon.com/dp/B00H9II8I2/) - (1ft, can also be a jumper between n-type surge protector to dongle
  * Surge protector for the SMA end: [SMA Lightning Arrestor Surge Protector SMA Male to SMA Female](https://www.amazon.com/dp/B07K25Y1JW/)
* Antenna Mounting assembly
  * [CHANNEL MASTER CM-3090 Universal J-Mount](https://www.amazon.com/dp/B000BSIABM) - antenna mount along fascia of house
  * [Everbilt 1-3/4 in. Stainless-Steel Clamp](https://www.homedepot.com/p/202309386) - to manage wires on mast - $1.10 each
  * [10 Gauge Copper ground wire](https://www.amazon.com/dp/B008OILG5I)

-->

