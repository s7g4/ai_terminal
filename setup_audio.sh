#!/bin/bash

# Setup script for audio configuration on systems using PipeWire or PulseAudio
# This script checks and enables PipeWire services, installs recommended packages,
# and removes conflicting JACK packages if necessary.

echo "Setting up audio for Jarvis AI Terminal..."

# Check if PipeWire is installed
if ! command -v pipewire &> /dev/null; then
    echo "PipeWire not found. Installing PipeWire..."
    sudo apt update
    sudo apt install -y pipewire pipewire-pulse pipewire-alsa
else
    echo "PipeWire is already installed."
fi

# Enable and start PipeWire services
echo "Enabling PipeWire services..."
systemctl --user enable pipewire pipewire-pulse
systemctl --user start pipewire pipewire-pulse

# Remove conflicting JACK packages if present
if dpkg -l | grep -q jackd2; then
    echo "Removing conflicting JACK packages..."
    sudo apt remove -y jackd2 qjackctl
fi

# Install recommended audio packages
echo "Installing recommended audio packages..."
sudo apt install -y alsa-utils pulseaudio-utils pavucontrol

# Restart PipeWire
echo "Restarting PipeWire..."
systemctl --user restart pipewire pipewire-pulse

echo "Audio setup complete. It is recommended to reboot your system."
echo "After reboot, run 'python3 core/list_input_devices_pyaudio.py' to list devices."
echo "Then test with 'python3 core/test_mic.py'."
