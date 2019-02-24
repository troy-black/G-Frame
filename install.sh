#!/bin/bash
echo "This Install Script is intended to be ran on a FRESH INSTALL of Raspbian Lite - No Desktop GUI"
echo ""
echo "Run raspi-config and configure basic setting:"
echo "   1. Change Password"
echo "   2. Network"
echo "         - Update Hostname - gframe"
echo "         - Config Wifi"
echo "         - Enable Names"
echo "   3. Boot Options"
echo "         - Autologin console"
echo "         - Wait Network on boot"
echo "   4. Localization"
echo "         - Local - en_US.UTF-8"
echo "         - Timezone"
echo "         - Keyboard layout"
echo "   5. Interfaces"
echo "         - SSH"
echo "   7. Advanced Options"
echo "         - Disable overscan"
echo ""
echo "Complete raspi-config before continuing..."
echo ""

echo "Updating Rasbian"
sudo apt-get update -y && sudo apt-get upgrade -y

echo "Installing Openbox and Chromium"
sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox chromium-browser -y

echo "Install python3-pip git"
sudo apt-get install python3-pip git -y

echo "Clone G-Frame"
git clone https://github.com/troy-black/G-Frame.git

echo "cd G-Frame"
cd G-Frame

echo "Install virtualenv"
pip3 install virtualenv

echo "Create virtualenv venv"
virtualenv venv

echo "Activate venv"
source venv/bin/activate

echo "install requirements.txt"
pip install -r requirements.txt

echo "Writing to /etc/xdg/openbox/autostart"
sudo cp install/autostart /etc/xdg/openbox/autostart

echo "Writing to /etc/rc.local"
sudo cp install/rc.local /etc/rc.local

echo "Making run.sh executable"
sudo chmod +x run.sh
