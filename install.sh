#!/bin/bash
echo "This must be ran as sudo!!!"
echo ""
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
apt-get update -y && apt-get upgrade -y

echo "Installing Openbox and Chromium"
apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox chromium-browser -y

echo "Install python3-pip git"
apt-get install python3-pip git -y

echo "Clone G-Frame"
su pi -c "git clone https://github.com/troy-black/G-Frame.git"

echo "cd G-Frame"
cd G-Frame

echo "Install virtualenv"
pip3 install virtualenv

echo "Create virtualenv venv"
su pi -c "virtualenv venv"

echo "Activate venv"
su pi -c "source venv/bin/activate"

echo "install requirements.txt"
su pi -c "pip install -r requirements.txt"

echo "Writing to /etc/xdg/openbox/autostart"
cp install/autostart /etc/xdg/openbox/autostart

echo "Writing to /etc/rc.local"
cp install/rc.local /etc/rc.local

echo "Making run.sh executable"
chmod +x run.sh
