# Final Project: Pi Security System
# CSE-525 (Fall 2022)
  *Group 9:*
Tahereh Alamdari
Jacob "Hat" Butler
Brady Gehrman
Michael Martin
Dylan Nicholson

## Purpose
This project is serves as a demonstration of what we have learned throughout the CSE/ECE 525 "Microcomputer Design" course at the University of Louisville. As our final project, we decided to create a security system, using a Raspberry Pi connected to a camera, motion detector, and keypad. The system can be managed by the user by connecting to a website hosted by the Pi (using Flask). If the motion detector picks up movement, the alarm is tripped. A user can enter a secret code in the website if the alarm is not triggered, and onto the keypad attached to the Pi if the alarm is triggered. If the alarm is tripped and is not subsequently deactivated, then a photo of the incident is sent over email to the system's owner.

## Setup
