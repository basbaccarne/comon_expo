# Comon Expo Interface
This repo describes the interface used for the permament [comon](https://comon.gent/en) expo in [De Krook](https://dekrook.be/en/).    

Visitors are presented with questions using tangible buttons (experience has learned that touch screens trigger lesss interaction in semi-public places).
These buttons are embedded in robot hands. The robot asks the visitors a question and they can high five the robot to indicate wether they agree, disagree or have no opinion on the subject. Next the vistor is presented with the responses of the other repondents.   

## Components
**Construction**
* The main structure is a robot
  * With a **front panel** and a **back panel** (see [design](https://www.canva.com/design/DAGePvjJkDo/3mGJuS1pnpP1t1xx3RmYJg/edit))
  * Held together by a **wooden frame**
  * Mounted on a **heavy foot** of a sun umbrella
  * With cutouts for the buttons (in the hands) and a screen in its chest
* A **Raspberry pi** is mounted on the back of a **screen** (offical [raspi monitor](https://www.raspberrypi.com/products/raspberry-pi-monitor/)), with a [3D printed connector](https://a360.co/40PoLU7)
* The screen and Raspi are mounted behind the cutout using [low](https://a360.co/3WMRYOa) and [high](https://a360.co/4jMSnKw) mounting pieces
* The questions are regularly updated on a printed callout box strung up to the ceiling next to the robot
  
**Electonics**
* The core of the system is a raspberry pi
* Connected to 3 **arcade buttons**
* Connected to a screen with PyGame
* In V1 the leds of the buttons are connected to a seperate 12V connection with a Female Connector DC Power Plug Adapter and a universal variable AC/DC adapter

**Code**   
The raspi runs a PyGame on boot ([splash](img/splash.png)). It listens to the buttons and stores the votes in a json file. The script is managed in 3 scenes: (1) listening to input (question state), (2) an animation after button press (response animation state) and (3) the response screen that shows the percentages of votes (response state). Scene 1 > 2 is triggered by a button press, Scene 2 > 3 through a timer and Scene 3 > 1 through a second timer. Changing and resetting campaigns in manages by defining a new json file name.   

⌨️ [Main Robot Code](src/main.py)
  
## Background: storing data
We can send data back and forth using public MQTT brokers, but we want to introducce two new challenges: 
1.  How can we set-up a local MQTT broker?
2.  How can we store incoming data in a database?

We want to do both things on a Raspberry Pi.   

To do this, we're working with **[Docker](https://www.docker.com/)** as a way to manage the different things our Pi has to do. Docker allows you to install (using 'images'), set-up, run and manage different services (including launch on boot, monitoring, configuring, ...) [^1][^2][^3].   

The tech stack to to this has 4 components:   
* An `MQTT Broker` ([Mosquito](https://mosquitto.org/)) that listens and dispatches MQTT messages accross applications and devices.
* A `server` (node-RED) that captures these messsages and writes them in a database
* A `database` (InfluxDB) that stores these values
* A `dashboard` (Grafana) to visualise the data in the dashboard

**Step 1: Raspberry Pi lazy install**   
*  Install [docker](https://www.docker.com/) & other required components (lazy download)
  
    ```console
    $sudo apt update
    $sudo apt upgrade -y
    $curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | bash
    ```
* After auto-reboot, Check if docker and docker-compose are installed correctly
  
   ```console
    $docker --version
    $docker-compose --version
    ```
* Install the desired components (mosquito, node-RED, influxDB & Grafana). This can be done using the handler script [IOTStack](https://sensorsiot.github.io/IOTstack/Basic_setup/) provides. Portainer is used to monitor docker components. See [video](https://youtu.be/_DO2wHI6JWQ?si=bsf9yWkBHiDuVUct&t=283) for installation flow.
  
  ```console
  $cd IOTstack/
  $./menu.sh
  ```
* You can manage and monitor your coker containers on `ip_adress:9000`
* You can enter the CLI of a docker using `$docker exec -it [id]`
  
**step 2: Configure the database**
* Enter the InfluxDB container:

  ```console
  $docker exec -it influxdb influx
  ```

* Now you can create databases (e.g. interface_input)

  ```console
  $CREATE DATABASE interface_input
  $quit
  ```

**step 3: Configure node-RED**
* Go to the web interface on `ip_adress:1880`
* Configure a MQTT input module
* Configure a change module to get clear datbase names
* Configure a influxdb out module to store the data in influxdb

**step x: set-up the MQTT sender**
* In the Arduino script: connect to the ip adress with port `1883` and topic e.g. `/xpo/test`

**step 4: check if data comes in**
* In your consol, go into the influxdb container
  ```console
  docker exec -it influxdb influx
  ```
* Show available databases
  ```console
  SHOW DATABASES
  ```
* Select database (e.g. interface_data)
  ```console
  USE interface_data
  show measurements
  ```
* And show the data that's in there
  ```console
  select * from interface_data
  ```
* exit when ready
  ```console
  quit
  ```

  **Step 5: set-up a dashboard with grafana**
  * Go to the grafana interface on `ip_adress:3000`
  * The default for the first login is admin / admin
  * The data source is an influxdb database on url `http://<ip>:8086`
  * Also give grafana the name of the influx db database & select the GET HTTP method
 

# Background: booting in PyGame
If you create a PyGame and you have a Raspi dedicated to running that pygame (in this case: the pi is automatically powered down and powered up at the end and beginning of each day). This is how you create a custom boot that directly opend the python script and first shows a custom splash screen.   

**Step 1. Create a service**
```console
sudo nano /etc/systemd/system/comon_expo.service
```
add the following content in the file:
```
[Unit]
Description=Comon Expo App
After=graphical.target

[Service]
User=comon
WorkingDirectory=/home/comon/comon_expo/src
ExecStart=/usr/bin/python3 /home/comon/comon_expo/src/main.py
Restart=always
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/comon/.Xauthority
Environment=XDG_RUNTIME_DIR=/run/user/1000
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=graphical.target
```
enable this service:
```console
sudo systemctl enable comon_expo.service
```
testrun this service:
```console
sudo -u comon /usr/bin/python3 /home/comon/comon_expo/src/main.py
```
If you update the python code:
```console
sudo systemctl restart comon_expo.service
```
To monitor the logs
```console
journalctl -u comon_expo.service -f
```
# Background: custom splash

**step 2. Hide boot messages for a cleaner look**   

By editting the `cmdline.txt` file
```console
sudo nano /boot/firmware/cmdline.txt
```
remove any instances of 
```
console=tty1 console=serial0
```
To hide text during boot, edit ´/boot/config.txt´
```console
sudo nano /boot/firmware/config.txt
```
add the following:
```
disable_splash=1
```

# Sources
[^1]: [Arduino Documentation](https://docs.arduino.cc/tutorials/portenta-x8/datalogging-iot/)
[^2]: [IOT stack Youtube channel](https://www.youtube.com/watch?v=_DO2wHI6JWQ)
[^3]: [IOT stack documentation](https://learnembeddedsystems.co.uk/easy-raspberry-pi-iot-server)
