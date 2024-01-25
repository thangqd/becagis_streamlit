
<h1 style="text-align: center;">BecaGIS Streamlit - Geospatial Apps made Easy</h1>

A BecaGIS Streamlit geospatial application inspired by [streamlit-geospatial](https://github.com/giswqs/streamlit-geospatial). It can be deployed to [Streamlit Cloud](https://streamlit.io/cloud), [Heroku](https://heroku.com/), or [MyBinder](https://mybinder.org/).

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/thangqd/becagis_streamlit/HEAD)

- Web app: <https://becagis.streamlit.app>
- Source code: <https://github.com/thangqd/becagis_streamlit>

# Run Geoprocessing from popular Container Registries

## Prerequisites

- Docker installed on your machine.

## How to run Geoprocessing from Docker Hub
1. **Pull Geoprocessing from Docker Hub:**
	```bash
	docker pull thangqd/becagis_streamlit
	```	

2. **Run the Docker Container:**
    ```bash
    docker run -p 8501:8501 thangqd/becagis_streamlit
	```
3. **Access Geoprocessing powered by Stramlit:**

Open your web browser and go to http://localhost:8501.


## How to run Geoprocessing from GitHub Container Registry
1. **Pull Geoprocessing from GitHub Container Registry:**
	```bash
	docker pull ghcr.io/thangqd/becagis_streamlit
	```	

2. **Run the Docker Container:**
    ```bash
    docker run -p 8501:8501 ghcr.io/thangqd/becagis_streamlit
	```
3. **Access Geoprocessing powered by Stramlit:**

Open your web browser and go to http://localhost:8501.



# Build and run Docker image from source  

## Prerequisites

- Git and Docker installed on your machine.

## How to install

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/thangqd/becagis_streamlit.git
	```
	

3. **Build the Docker Image:**
	```bash
	cd becagis_streamlit
	docker-compose build 
	```
	
4. **Run the Docker Container:**
    ```bash
    docker-compose up
	```

5. **Access Geoprocessing powered by Stramlit:**

Open your web browser and go to http://localhost:8501.

## Support
Feel free to access https://github.com/thangqd/geoprocessing/issues to report any inquiries or issues

![flightroute](https://github.com/thangqd/becagis_streamlit/assets/1776420/7a1c0de3-c8a5-4e45-a42f-54b0ec77806b)
