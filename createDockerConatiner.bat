@echo off
SET IMAGE_NAME=noc-dashboard
SET CONTAINER_NAME=noc-dashboard-app

:: 1. Find and delete existing containers built from this image
echo Checking for existing containers...
FOR /F "tokens=*" %%i IN ('docker ps -a -q --filter "ancestor=%IMAGE_NAME%"') DO (
    echo Removing container %%i...
    docker rm -f %%i
)

:: 2. Find and delete the existing image
echo Checking for existing image...
FOR /F "tokens=*" %%i IN ('docker images -q %IMAGE_NAME%') DO (
    echo Deleting image %IMAGE_NAME%...
    docker rmi -f %IMAGE_NAME%
)

:: 3. Build the new image
echo Building new Docker image: %IMAGE_NAME%...
docker build -t %IMAGE_NAME% .

:: 4. Start a new container with a random host port mapping
echo Starting new container on a random port...
docker run -d -P --name %CONTAINER_NAME% %IMAGE_NAME%

:: 5. Display the newly assigned random port
echo Container is up! Current port mapping:
docker port %CONTAINER_NAME%

:: 6. Export the image to a .tar archive in the current directory
echo Exporting image to %IMAGE_NAME%.tar...
docker save -o %IMAGE_NAME%.tar %IMAGE_NAME%

echo Process complete!
pause
