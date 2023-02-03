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

### Install GUI

* use Tar1090 from @wiedhopf here: https://github.com/wiedehopf/tar1090
  ```
  sudo bash -c "$(wget -nv -O - https://github.com/wiedehopf/tar1090/raw/master/install.sh)"
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
* View your page: [https://flightaware.com/account/manage](https://flightaware.com/account/manage)bash /usr/local/share/tar1090/uninstall.sh adsbx
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

#### adsbexchange (DEPRECATD)

* ADSBx has been sold. Don't do it.
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
sudo 

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
