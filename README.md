# FireGuard - Group 5

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

