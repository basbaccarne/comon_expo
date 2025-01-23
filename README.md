# Comon Expo Interface
This repo describes the interface used for the permament [comon](https://comon.gent/en) expo in [De Krook](https://dekrook.be/en/). Visitors are presented with questions using tangible buttons.

## Background: storing data
We can send data back and forth using public MQTT brokers, but we want to introducce two new challenges: 
1.  How can we set-up a local MQTT broker?
2.  How can we store incoming data in a database?

We want to do both things on a Raspberry Pi.   

To do this, we're working with **[Docker](https://www.docker.com/)** as a way to manage the different things our Pi has to do. Docker allows you to set-up, run and manage different services (including launch on boot, monitoring, configuring, ...) [^1][^2][^3].   

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
* Install the desired components (mosquito, node-RED, influxDB & Grafana). This can be done using the handler script [IOTStack](https://sensorsiot.github.io/IOTstack/Basic_setup/) provides
  
  ```console
  cd IOTstack/
  ./menu.sh
  ```
**step 2:*** 


# Sources
[^1]: [Arduino Documentation](https://docs.arduino.cc/tutorials/portenta-x8/datalogging-iot/)
[^2]: [IOT stack Youtube channel](https://www.youtube.com/watch?v=_DO2wHI6JWQ)
[^3]: [IOT stack documentation](https://learnembeddedsystems.co.uk/easy-raspberry-pi-iot-server)
