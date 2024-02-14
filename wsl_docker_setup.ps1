$network = "feinstaub_network"
$databaseVolume = "feinstaub_database_vol"
$databaseContainerName = "feinstaub_database"
$pgadminVolume = "pgadmin_vol"
$pgadminContainerName = "pgadmin"
$apiContainerName = "feinstaub"
$apiVersion = 1

Write-Output "Starting setup"

$dockerNetworks = wsl docker network ls
Write-Output "Found networks:"
Write-Output $dockerNetworks

$dockerVolumes = wsl docker volume ls
Write-Output "Found volumes:"
Write-Output $dockerVolumes

$dockerContainer = wsl docker ps -a
Write-Output "Found container:"
Write-Output $dockerContainer

if(!$dockerNetworks -Match $network){
    Write-Output "Creating $network"
    wsl docker network create $network
}

if(!$dockerVolumes -Match $databaseVolume){
    Write-Output "Creating $databaseVolume"
    wsl docker volume create $databaseVolume
}

if(!$dockerVolumes -Match $pgadminVolume){
    Write-Output "Creating $pgadminVolume"
    wsl docker volume create $pgadminVolume
}

if($dockerContainer -Match $databaseContainerName){
    Write-Output "Container already found. Updating: $databaseContainerName"
    wsl docker stop $databaseContainerName
    wsl docker rm $databaseContainerName
}

wsl docker run -d --name $databaseContainerName -p 5432:5432 --restart always --network $network -v ${databaseVolume}:/var/lib/postgresql/data -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password postgres:15.3-bullseye
Write-Output "Container successfully started: $databaseContainerName"

if($dockerContainer -Match $pgadminContainerName){
    Write-Output "Container already found. Updating: $pgadminContainerName"
    wsl docker stop $pgadminContainerName
    wsl docker rm $pgadminContainerName
}

wsl docker run -d --name $pgadminContainerName -p 9091:9091 --restart always --network $network -v ${pgadminVolume}:/var/lib/pgadmin -e PGADMIN_DEFAULT_EMAIL=admin@admin.de -e PGADMIN_DEFAULT_PASSWORD=password -e PGADMIN_LISTEN_ADDRESS=0.0.0.0 -e PGADMIN_LISTEN_PORT=9091 dpage/pgadmin4:8.4
Write-Output "Container successfully started: $pgadminContainerName"

Write-Output "Building API image"
wsl docker build --pull --no-cache --force-rm --tag ${apiContainerName}:$apiVersion .

if($dockerContainer -Match $apiContainerName){
    Write-Output "Container already found. Updating: $apiContainerName"
    wsl docker stop $apiContainerName
    wsl docker rm $apiContainerName
}

wsl docker run -d --name $apiContainerName -p 9090:9090 --restart always --network $network ${apiContainerName}:$apiVersion
Write-Output "Container successfully started: $apiContainerName"
