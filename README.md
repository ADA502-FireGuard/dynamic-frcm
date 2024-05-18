# FireGuard - Group 5

The FireGuard Cloud Service v.0.1.0 for the ADA502 course.

**Collaborators:** Alexander Ringheim, Daniel Vikøyr, Sigve Bjørhovde, Thomas Mavropoulos

![firerisk drawio](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/4137667/55bc8db2-eecd-4cf1-8f12-f2505d1a3d48)

The project git repository is publicly available on [Github](https://github.com/ADA502-FireGuard/dynamic-frcm). The Docker repository can be found at [DockerHub](https://hub.docker.com/r/alexbringh/fireguard-v-0-1-0/).

This FireGuard project .... database .... testing .... docker/containerization/orchestration/deployment ... CI/CD ... RESTful degree (level) ... Architecture?

We currently provide these security measures (HTTPS) and have begun implementing authentication through keycloak....

#TODO: her begynner alex å skriva om architecture

#TODO: her begynner alex å skrive om REST api. Par setningar.


## Getting started

There are mainly two recommended ways of getting the service running on your machine. You can either clone the Git repository or grab the Docker image. We describe the required steps to both approaches below.

For interacting with the API in Windows, we recommend these applications:

* [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701) - Modern terminal application
* [Bruno](https://www.usebruno.com/) - Web API client

> **Tip:** Windows comes with two terminals pre-installed, `Command Prompt` and `PowerShell`. You can access either from the Windows search bar.

Note that FireGuard encrypts traffic with `Secure Sockets Layer`. For purposes of testing and demoing, we provide keys with the project. As they are publicly available, they should not be trusted in production settings. Generate your own `SSL` keys and add them before deploying.

### Cloning the repository

FireGuard employs [Met.no's API](https://api.met.no), which requires authentication to use. You need to register for credentials [here](https://frost.met.no/auth/requestCredentials.html) before beginning.

Clone the repository to your machine

```bash
git clone https://github.com/ADA502-FireGuard/dynamic-frcm.git
```

Navigate to the project directory you cloned

```bash
cd dynamic-frcm
```

Add the MET API ID and secret to your environment variables

```bash
export MET_CLIENT_ID="<INSERT ID>"
export MET_CLIENT_SECRET="<INSERT SECRET>"
```

Now, start the docker containers

```bash
docker-compose up 
```

You can exit by pressing `CTRL+C`

You will need to do the equivalent for `postgres-frcm` to get database functionality.

#TODO nevn noko om Postgres og Database, 

### Running with Docker-compose

> **Note:** Assuming you are using Windows, you will need to have [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) installed to run the Docker image.

#TODO Fix text underneath
With container orchestration through docker-compose, we're able to easily run several docker containers in conjunction, all communicating with each other through a bridged network.

Open a terminal and pull the Docker image

```bash
docker pull alexbringh/fireguard-v-0-1-0
```

> **Tip:** You can confirm that the Docker image has been downloaded to your computer by entering, `docker images`. You should see a line detailing the image `alexbringh/fireguard-v-0-1-0`.

At this point, the docker image should also be viewable in `Docker Desktop for Windows`.

Add the MET API ID and secret to your environment variables

```bash
export MET_CLIENT_ID="<INSERT ID>"
export MET_CLIENT_SECRET="<INSERT SECRET>"
```

You can now run the image

```bash
docker-compose up -d
```

You can now access the service at `https://127.0.0.1:8000`.

#### Docker Desktop

If you would rather run the image from `Docker Desktop`, find the image under the `Images` tab. Select the play button and enter 8000 as the host port under `Optional settings`. Now press `Run`.

![rundockerdesktop](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/4137667/70963408-f437-44ec-bed0-5cd2c8aeb915)

#### Running tests

```bash
#Command to tests in container
```

#TODO

Beskrivelse av tester her?

## User guide

Once running, the FireGuard Cloud Service will accept inputs. Assuming the Docker container is running locally you can reach the API at `https://127.0.0.1:8000`.

The service accepts inputs in the form of standard HTTP requests through a `RESTful API`. You may use any framework or program that sends HTTP requests such as `get` and `post` to interact with the service. The `API endpoints` with the valid `query parameters` are described below.

For simple testing of functionality, we recommend using `Bruno`, as it gives a simple GUI for setting up these requests. We have prepared a pre-configured Postman collection which can be imported into `Bruno`. You can find the tests [here](https://github.com/ADA502-FireGuard/dynamic-frcm/tree/main/tests).

 For stress-testing or multi-user simulation of the system, it would be more appropriate to create a custom multithreading script. By default, `Bruno` only sends one request at a time.

### Setting up requests to the FireGuard Cloud Service

The following examples assume that you have set up the Docker container as detailed above.

The most simple HTTP request that can be made of FireGuard is `GET https://127.0.0.1:8000/`, which will simply return a welcoming message, letting you know the service is available.

The next endpoint is `/services", which lists available API endpoints and query parameters.

```bash
GET https://localhost:8000/services
```

> **Note:** As of v0.1.0 the services list is not updated to include all services, and you should instead follow this guide for now.

FireGuard offers five different methods of calculating fire risk. You may manually insert weather data, location and timestamp yourself, and have the model simply calculate and return the results using the following request.

```bash
POST https://localhost:8000/rawdata?temp=...
```

Usually, users will not have all necessary data to use the `rawdata` option directly. Rather, a more common use-case is someone interested in discovering the fire risk at a certain location, such as an address, postal code or even longitude and latitude. Based on the given location data point, FireGuard offers to retrieve the remaining required parameters for the user. FireGuard accomplishes this by seamlessly converting that location to coordinates through a GeoCoding service. We then retrieve weather data for those coordinates through a Meteorological service, before finally doing the fire risk calculations.

The available options for the area service are as follows.

### GPS

```bash
POST https://localhost:8000/area/gps?lon=...+lat=...+day=...
```

This option takes coordinates as inputs along with a timedelta for which the service is to calculate for.
The required tags.

```bash
lon:  float - The longitude coordinate
lat:  float - The latitude coordinate
days: float - Number of days to be calculated for
```

```bash
POST https://localhost:8000/area/address?adr=...+days=...
```

```bash
adr:  str - The address string. Make sure it is a valied address, for example "Inndalsveigen 28"
days: float - The number of days to be calculated for.
```

### Postcode

```bash
GET http://localhost:8000/area/postcode?postcode=...+days=...
```

This option takes a Norwegian four-digit postcode and uses a Geocoding API to try and turn the address into coordinates automatically. Normally the Geocoding API will give a whole lot of coordinates for the postcode in question, the code requests that only the one best representing the postcode area be sent. This is a hard-coded option into FireGuard, however it is possible to change this option of course, but the user does not have this option by default.
The required tags.

```bash
postcode:  int - The four-digit postcode for the area. Make sure that the postcode is valid. For example "5063" (Bergen)
days:      float - The number of days to be calculated for.
```

## Following Versions

The next versions are expected to also accept multiple data points for any options, as well as feature more options such as postal area, authentication and subscription to data for a certain area.

#TODO fix text below
Input validering, mer automatisk testing,  