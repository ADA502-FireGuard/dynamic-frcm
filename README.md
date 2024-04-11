# FireRisk - Group 5

The FireGuard Project for the ADA502 course.

## <span style="color:tomato"> Prerequisites </span>
Mandatory:
* [Python 3.11](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installation)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Recommended:
* [Powershell](https://github.com/PowerShell/PowerShell/releases/tag/v7.4.1)

## <span style="color:tomato"> Installation </span>

To install the program for this project, we need to download/pull the docker image from DockerHub.

After downloading the Docker image, we can set up and run the program/application on localhost.

### <span style="color:tomato">Step 1: Open Docker Desktop</span>

First, open [Docker Desktop](https://www.docker.com/products/docker-desktop/). 

(Docker needs to be running in the background.)

### <span style="color:tomato">Step 2: Open a terminal window</span>

Launch your terminal of choice.

You can type "cmd" in a Windows search bar to find the embedded command-line interface on Windows devices (alternatively press Windows key + R, type "cmd", and hit enter.)

### <span style="color:tomato">Step 3: Pull the project from Docker</span>
Next, we need to download the project from Docker.

In your terminal window of choice, write the following command:
```
docker pull xxx
```
image

### <span style="color:tomato">Step 4: Check Docker images on your local machine</span>
The project's Docker image should now be on your computer. 

To confirm this, run the following command in your terminal window:

```
docker images
```
![Cmd Docker Images](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/17d6a082-31cb-43e8-91dd-940c71ddd789)

### <span style="color:tomato">Step 5: Check the Docker Desktop Application</span>
In the Docker application, we should now be able see the project image in the image folder:

![Docker Images](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/e2077c31-f916-4ba5-beea-d662d7caffb5)

### <span style="color:tomato">Step 6: Run the project image</span>
Press the run button for the project:

![Run Image](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/42ac821c-58ea-4963-83cc-65df7e537a2c)


Enter "8000" as the host port, and then press run:

<img src="https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/6ebceb70-95f3-476a-a43c-e7931ae2dfef" width="100">

### <span style="color:tomato">Step 7: Profit!!! 🎉🥳🎂</span>
Congratulations, you are now running the application!

You should see the following in your Docker application:

![Docker Logs](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/94006886/0b4b1d72-09c7-4ce4-b5f5-bfe0677a09e3)

Continue to the "User guide" below for pointers on how to use the program.

## <span style="color:tomato"> User guide </span> 
