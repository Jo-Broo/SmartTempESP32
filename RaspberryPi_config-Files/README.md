# Raspberry PI config Files

## Table of Contents
- [Featured Config Files](#config-files)
- [Installation Guide](#installation-guide)

## Config Files

- [MQTT-Broker(Mosquitto)](mosquitto.conf) On my System this File was located in /etc/mosquitto. 
- [MariaDB](mariadb.cnf) On my System this File was located in /etc/mysql. 

## Installation Guide

The First Step in every installation is to always Update your Raspberry to 
the newest Version, this can be achieved by executing 
`sudo apt update && sudo apt upgrade`.

Now that our System is up to Date we can start installing all the necessary 
Packages.

### MQTT-Broker
1. Installing the Mosquitto MQTT-Broker <br>
`sudo apt install -y mosquitto mosquitto-clients` <br>
With this command we install the Mosquitto-Broker and Clients in one go, the -y
parameter indicates that we will answer every question proposed to us with yes.
Right now the Mosquitto-Broker is not running at has to be started manually 
every time the System boots up. To start the Service automatically we type 
`sudo systemctl enable mosquitto.service` this will place the Service in 
the autostart of the OS. After a Reboot we can confirm the installation by 
running `sudo service mosquitto status`, you should see something like this. 
![Screenshot of the Command Output](/Images/Mosquitto.PNG "Output on my System")
2. Configuring the Broker <br> 
    The Config File on my System was located in `/etc/mosquitto/`. <br>
    You can configure your Broker in two ways:
    * Without Authentification <br> Enter the File `mosquitto.conf` 
    with your preferred editor and just add ``listener 1883`` 
    and ``allow_anonymous true`` to the end of the file 
    and save it.
    * With Authentification <br> Enter the File `mosquitto.conf` 
    with your preferred editor, at the start of File right after the 
    commentblock add ``per_listener_settings true``. At the end 
    add ``listener 1883`` and ``allow_anonymous false`` 
    (notice that here the connection for non authenticated users is prohibited). 
    To add Mosquitto Users for the first time you use the following command 
    `sudo mosquitto_passwd -c <passwordfile location> <username>` 
    (the recommended location for the passwordfile would be `/etc/mosquitto/passwd` 
    but you can really place it anywhere, and the username is also up to you) 
    the `-c` flag is for creating a     new passwordfile by clearing any existing one's.
    <br>To further add users you have to use 
    `sudo mosquitto_passwd <passwordfile location> <username>` 
    notice how we didn't add the `-c` flag.<br><br> 
    To apply all changes we made execute `sudo systemctl restart mosquitto`
3. Testing the Broker <br> 
    To test everything we open up two terminal windows. In the first window
    we set up a MQTT-Client that will listen to the Topic 'Test' by executing 
    `mosquitto_sub -t Test`. 
    In the second window we execute `mosquitto_pub -t Test -m 'My first MQTT Message'`.
    The Message should now appear in the first window where the client was listening.
    ![Screenshot of the listening Client](/Images/Mosquitto_sub.PNG "Output on my System")
    ![Screenshot of the publishing Client](/Images/Mosquitto_pub.PNG "Output on my System")

Thats all there is to setup the MQTT-Broker it should now work correctly.

### MariaDB

...