# Final Project: Pi Security System
**CSE-525 (Fall 2022)**  
---
  *Group 9:*  
Tahereh Alamdari  
Jacob "Hat" Butler  
Brady Gehrman  
Michael Martin  
Dylan Nicholson  

## Purpose
This project is serves as a demonstration of what we have learned throughout the CSE/ECE 525 "Microcomputer Design" course at the University of Louisville. For our final project, we decided to create a security system, using a Raspberry Pi connected to a camera, motion detector, and keypad. 

## Design and Implementation
The Raspberry Pi is connected to a keypad, motion detector (AKA PIR sensor), RGB LED, and a Pi camera module. The camera is connected to the Pi via a ribbon cable, and everything else is connected using GPIO pins. The "main" python file that controls everything is `flaskapp.py`, which uses the Flask library to host a web server. The same file also manages the overall state of the system.

![Diagram of devices connected to the Pi](/assets/Pi-sensor-setup.png)

These are the specific GPIO pins we're using:  
```
Keypad:
ROW_PINS = [5, 6, 13, 19] #BCM Numbering
COL_PINS = [26, 16, 20, 21] #BCM Numbering

PIR Sensor:
GPIO 14 (BCM number)

RGB LED:
GPIO 17 - RED
GPIO 27 - GREEN
GPIO 22 - BLUE 
```

A user can manage the system by connecting to the website hosted by the Pi. If the motion detector picks up movement, the "alarm" is tripped. A user can enter a secret code in the website if the alarm is not triggered, and onto the keypad attached to the Pi if the alarm is triggered. If the alarm is tripped and is not subsequently deactivated, then a photo of the incident is sent over email to the system's owner.

## Setup
This project must be run on an actual Raspberry Pi, due to Pi-specific packages required to interface with the sensors. You may want to use a machine other than the Pi for development/testing. One solution is to use VS Code to connect to a folder hosted by the Pi over SSH. This can be done with the "Remote - SSH" extension by Microsoft. See: https://singleboardblog.com/coding-on-raspberry-pi-remotely-with-vscode/

The Raspberry Pi should be set up with Raspberry Pi OS/Raspbian. The version used for this project is the standard 32-bit distribution based on Debian Bullseye. Python 3.9 must be installed, along with necesarry packages used in the Python files. On Raspberry Pi OS, these should come preinstalled.

When running `flaskapp.py`, it will start a webserver on port 1234. To see the webpage, you can open a browser on the Pi and enter the URL http://0.0.0.0:1234/ into the browser's address bar. If you are developing on another machine connected to the Pi over LAN, you can also visit the web page by entering the Pi's private IP address into a browser followed by port 1234. You can get the Pi's private IP by running `ip a` on the Pi; it should likely start with "192.168.".