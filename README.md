# FireGuard - Group 5

The FireGuard Ckoud Service v.0.1.0 for the ADA502 course.

## <span style="color:tomato"> Prerequisites </span>
Mandatory:
* [Python 3.11](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installation)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Recommended:
* [Powershell](https://github.com/PowerShell/PowerShell/releases/tag/v7.4.1)

## <span style="color:tomato"> Installation </span>

To install the program for this project, you need to download/pull the docker image from DockerHub.

After downloading the Docker image, you can set up and run the program locally (on localhost).

### <span style="color:tomato">Step 1: Open Docker Desktop</span>

First, open [Docker Desktop](https://www.docker.com/products/docker-desktop/). 

(Docker needs to be running in the background.) 

### <span style="color:tomato">Step 2: Open a terminal window</span>

Launch your terminal of choice. 

Tip: You can type "cmd" in a Windows search bar to find the embedded command-line interface on Windows devices, or alternatively press Windows key + R, type "cmd", and hit enter. 

### <span style="color:tomato">Step 3: Pull the project from Docker</span>
Next, you need to download the project from Docker. 

Write the following command in your terminal window: 
```
docker pull princesig/ada502_group_5:latest 
```
<img src=https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/c8caa6fd-327b-49c7-97a1-670f8b05c548 width="570">

#### <span style="color:tomato">Step 3.1 (optional): Check Docker images on your local machine</span>
The project's Docker image should now be on your computer. 


To confirm this, you can write the following command in your terminal window: 
```
docker images 
```
You should see something like this: 

<img src="https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/17d6a082-31cb-43e8-91dd-940c71ddd789" width="620">

#### <span style="color:tomato">Step 3.2 (optional): Check the Docker Desktop Application</span>
In the Docker Desktop application, you should now be able see the project image in the "Images" tab: 

![Docker Images](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/e2077c31-f916-4ba5-beea-d662d7caffb5)

### <span style="color:tomato">Step 4: Run the project image</span>
In the "Images" tab, select the newly added image. Press the run button for the project: 

![Run Image](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/42ac821c-58ea-4963-83cc-65df7e537a2c)

Enter "8000" as the host port, and then press run: 

<img src="https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/6ebceb70-95f3-476a-a43c-e7931ae2dfef" width="325">

### <span style="color:tomato">Step 5: Profit!!! 🎉🥳🎂</span>
Congratulations, you are now running the application! 

You should now be able to see the following information about the running container in your Docker Desktop application, in the "Containers" tab: 

<img src="https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/0b4b1d72-09c7-4ce4-b5f5-bfe0677a09e3" width="650">

Continue to the "User guide" below for pointers on how you can use the program to perform fire risk calculations. 

## <span style="color:tomato"> User guide </span> 

Once the image is running within a container, the FireGuard Cloud Service will accept inputs. If the image is running locally and the tests are being ran locally, you may communicate with the container locally on localhost:8000 (alternatively 127.0.0.1:8000). 

#### <span style="color:tomato">Options for communicating with the cloud service.</span>
The Cloud Service accepts inputs in the form of standard http requests through a RestAPI. To communicate with the cloud service you may use any framework or program that sends get, post, etc. requests with the proper parameters as described further below. 
For simple testing of functionality, we recommend using Postman as it gives a simple GUI for setting up these requests, however be aware that postman by default only sends one request at a time, even if you try to run an entire collection of postman requests, it will simply send them one-by-one. For simple functionality this is no issue, however if you wish to simulate multiple users at a time, a sort of "stress-test", you will need a different approach. A good alternative for setting up tests for multiple users is to make a small python-script using the threading and requests modules to make a certain amount of threads that send their own request simultaneously.
If Postman will be satisfactory, a pre-configured Postman collection exists under the "test" folder of this repository.

#### <span style="color:tomato">Setting up requests to the FireGuard Cloud Service</span>
Assuming that the request is sent locally to the docker container, the ip of the container is given here as localhost:8000, however if this is not the case, if the container is running on a server or such, find and use the correct IP for your usecase.

The most simple request that can be made to FireGuard is
```
GET http://localhost:8000/fireguard
```
This request does not require any tags. FireGuard will simply return a welcoming message.

The next request is called services and returns what kind of services are available. NB: As of v.1.0 the services list is not updated to include all services and follow this guide instead of that.
```
GET http://localhost:8000/fireguard/services
```

At this point you are presented with a couple of choices. FireGuard offers a couple of different methods of calculating firerisk. You may insert weather data, location and timestamp yourself and have the model simply calculate and return the results using the following request.
```
POST http://localhost:8000/fireguard/rawdata? tags...
```
The request requires the following tags to be included.
```
temp:                float - The termperature in degrees celsius
temp_forecast:       float - The forecast temperature in degrees celsius
humidity:            float - The humidity
humidity_forecast:   float - The forecast humidity
wind_speed:          float - The wind speed in meters per second
wind_speed_forecast: float - The forecast wind speed in meters per second
timestamp:           str   - The timestamp at the time of measuring the physical data
timestamp_forecast:  str   - The timestamp for the forecast physical data
lon:                 float - The longitude coordinate where the data was measured
lat:                 float - The latitude coordinate where the data was measured
```

If you do not have all this data but is instead interested in the firerisk in a certain location, FireGuard offers a variety of requests that only requires you to specify a location. FireGuard will from there convert the location to coordinates through a GeoCoding service and get the weather data for that location through a Meteorological service.

The available options for the area service are as follows.

##### <span style="color:tomato">GPS</span>
```
GET http://localhost:8000/fireguard/services/area/gps
```
This option takes coordinates as inputs along with a timedelta for which the service is to calculate for.
The required tags.
```
lon:  float - The longitude coordinate
lat:  float - The latitude coordinate
days: float - Number of days to be calculated for
```

##### <span style="color:tomato">Multiple GPS'</span>
```
GET http://localhost:8000/fireguard/services/area/multiple_gps
```
This option takes multiple coordinates as inputs along with a timedelta for which the service is to calculate for.
The required tags.
```
lon:  list[float] - The longitude coordinate
lat:  list[float] - The latitude coordinate
days: float - Number of days to be calculated for
```

##### <span style="color:tomato">Address</span>
```
GET http://localhost:8000/fireguard/services/area/address
```
This option takes a address string and uses a Geocoding API to try and turn the address into coordinates automatically.
The required tags.
```
adr:  str - The address string. Make sure it is a valied address, for example "Inndalsveigen 28"
days: float - The number of days to be calculated for.
```

##### <span style="color:tomato">Postcode</span>
```
GET http://localhost:8000/fireguard/services/area/postcode
```
This option takes a four-digit postcode and uses a Geocoding API to try and turn the address into coordinates automatically. Normally the Geocoding API will give a whole lot of coordinates for the postcode in question, the code requests that only the one best representing the postcode area be sent. This is a hard-coded option into FireGuard, however it is possible to change this option of course, but the user does not have this option by default.
The required tags.
```
postcode:  int - The four-digit postcode for the area. Make sure that the postcode is valid. For example "5063" (Bergen)
days:      float - The number of days to be calculated for.
```


#### <span style="color:tomato">Following Versions</span>
The next versions is also expected to accept multiple datapoints for any options, as well as feature more options such as postal area, authentication and subscription to data for a certain area.

