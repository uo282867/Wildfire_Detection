### Wildfire_Detection
#### TFG: DETECCIÓN DE INCENDIOS FORESTALES MEDIANTE INTELIGENCIA ARTIFICIAL EN EL BORDE (EDGE AI)
------------
Este repositorio tiene la finalidad de almacenar el software desarrollado por Enrique Hilanderas para su TFG. En este repositorio podemos encontrar una variedad de pequeños scripts para: entrenamiento, e inferencia de modelos YOLO tanto para un PC como para sistemas empotrados como una Raspberry PI.

------------

This repository is intended to store the software developed by Enrique Hilanderas for his TFG. In this repository, we can find a variety of small scripts for: training, and inference of YOLO models for both a PC and embedded systems like a Raspberry PI.

------------

# Español
## Estructura del repositorio
Hay un total de 4 carpetas importantes con sus correspondientes scripts necesarios para su ejecución.
- ServerDatabase.
- SoftwareDetect.
- Train
- Utils

### Server Database
------------
En este directorio podemos encontrar un archivo *docker-compose.yaml* que nos permite:
1. Crear una base de datos Timescale para almacenar los datos de las detecciones junto con una timestamp para saber en qué momento se produjo la detección.
2. Crear una API que escuche en el puerto 5000 para poder acceder a la base de datos tanto a la hora de escribir como de leer los datos de esta.

#### Archivo database.env
En este archivo se encuentran las credenciales por defecto de la base de datos, es recomendable cambiarlas en caso de querer usar el proyecto para cualquier cosa que no sea un test de este.

***API_KEYS*** : Este campo es una pequeña medida de seguridad empleada para que solo dispositivos autorizados sean capaces de escribir en la base de datos. Es muy recomendable generar una key nueva y no emplear la actual. En caso de modificarla, se ha de modificar también en el archivo ***config.json*** de *Software Detect*.

#### Funcionamiento de la API
La API posee los siguientes métodos:

**/add [POST]**: Permite añadir una nueva alerta a la base de datos y guardar la imagen adjunta en la petición post. Formato de la petición posrt:
```
data = {
        'title': '...',
        'message': '...',
        'key' : 'API_KEY'
		}

files = {
        'img': (img_url, img_data, 'image/png')
		}
```
Una vez recibe una petición valida (posee la API_KEY correcta), se almacena en la base de datos los valores obtenidos y se registran como alertas que **no han sido comprobadas**, además se guardan las imágenes en un directorio con el nombre del ide que se genera para la imagen para poder ser accedidas posteriormente.

**/data [GET]**: permite acceder a la lista detallada de todas las alertas que no hayan sido comprobadas.

**/data/all [GET]**: permite acceder a la lista detallada de todas las alertas.

**/see/{id} [GET]**: permite visualizar en pantalla la alerta asociada a ***{id}***. Accediendo a esta url la alerta asociada a dicho ***{id}*** pasará a estado **comprobada**.

**/img/{id} [GET]**: devuelve la imagen asociada a ***{id}***.

#### Puesta en marcha
```
# bash
cd /directorio/del/proyecto/ServerDatabase
docker-compose up --build
```
**Posibles fallos** </br>
Si por algún casual alguno de los contenedores falla y se para, esperar a que el otro este inicializado correctamente y volverlo a arrancar.

```
# bash
docker-compose start
```

### Software Detect
------------
**Antes de comenzar**
Esta aplicación esta ideada para ser empleada en un sistema empotrado. 
En este caso, fue diseñado para una Raspberry PI 4, con una cámara [Raspberry Pi High Quality Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/). En caso de emplear otro sistema empotrado y/o cámara (incompatible con Picamera2) será necesario cambiar como mínimo el script: ***predict-camera.py***.

Es necesario también, sustituir en el archivo config.json `YOUR_SERVER_IP` por la IP del dispositivo en el que se esté ejecutando la **API** (ver: Server Database). Además, si se ha modificado la **API_KEY** de como se mencionó anteriormente se ha de sustituir también en este archivo por la nueva.

también es necesario tener instalado [Python3](https://www.python.org/).

------------
#### Instalar dependencias
**Picamera 2**
En caso de cualquier posible error con la instalación, consultar la documentación oficial: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
```
# bash
sudo apt install -y python3-picamera2
```

**Ultralytics**
En caso de cualquier posible error con la instalación, consultar la documentación oficial: https://docs.ultralytics.com/guides/raspberry-pi/#start-with-docker
```
# bash
sudo apt update
sudo apt install python3-pip -y
pip install -U pip

pip install ultralytics[export]

sudo reboot
```
**Error común**
En el caso de que no te permita emplear el gestor de paquetes pip por este error:
`error: externally-managed-environment`
Es posible que puedas solucionarlo de la siguiente forma:
```
# bash
sudo apt update
sudo apt install python3-pip -y

sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.bak

pip install -U pip

pip install ultralytics[export]

sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED.bak /usr/lib/python3.11/EXTERNALLY-MANAGED

sudo reboot
```

**Pillow, request y cv2**
```
# bash
sudo apt install -y python3-request
sudo apt install -y python3-pillow
sudo apt install -y python3-opencv
```

#### Puesta en marcha
```
# bash
cd /dir/del/proyecto/SoftwareDetect
python3 predict-camera.py
```

### Train
------------
En esta carpeta se encuentra un notebook para el entrenamiento de diversos modelos YOLO.
Para el entrenamiento es **necesario** un dataset. Si deseas acceder al dataset empleado para estos entrenamientos puedes encontrar su link en el archivo README.dataset.txt que se encuentra en el directorio Train también.
Una vez poseas un dataset adecuado para entrenar modelos YOLO guardalo dentro  del directorio Train con el nombre `Dataset`.

#### Ejecucion
**Instalar e importar ultralytics:**
Ejecutar las dos primeras celdas:
`! pip install ultralytics`
`from ultralytics import YOLO`

** Seleccionar el modelo a entrenar **
Ejecutar la celda con el nombre del modelo que deseas entrenar.
Ej. para entrenar YOLOv8n, ejecutar la celda:
`modelName = "yolov8n"`
Para entrenar otros modelos consultar la wiki de ultralytics: https://docs.ultralytics.com/models/

** Realizar el entrenamiento **
Ejecutar la siguiente celda:
```
# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from YAML
##model = YOLO(modelName+".pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="./Dataset/data.yaml", epochs=200, imgsz=640, device=[1], project='runs/detect/'+modelName)
```
Si tu dataset no se encuentra en el directorio especificado en la celda o posee otro nombre, modificar la ruta en la celda para que coincida.
Es necesario poseer el archivo ***data.yaml***.
La ultima celda fue creada para reentrenar uno de los modelos ya entrenados con otro dataset.

### Utils
------------
En esta carpeta podemos encontarar un archivo JSON para poder importarlo en grafana. Este Dashboard nos permite ver en tiempo real las detecciones que se realizan.
**Requisitos**
- Tener instalado grafana
- Instalar los siguientes plugins de grafana:
	- `Infinity` : https://github.com/grafana/grafana-infinity-datasource
	- `Dynamic image panel` : https://github.com/Dalvany/dalvany-image-panel

**ANTES DE IMPORTAR EL ARCHIVO! **
Reemplaza en el archivo todos los: `YOUR_SERVER_IP` con la IP del dispositivo donde estes almacenando los datos obtenidos de la inferencia junto con la API para acceder a los datos de la base de datos (ver: ***Server Database***). 

# English translation
## Structure of the repository
There are a total of 4 important folders with their corresponding scripts necessary for execution.
- ServerDatabase.
- SoftwareDetect.
- Train
- Utils

### Server Database
------------
In this directory, we can find a *docker-compose.yaml* file that allows us to:
1. Create a Timescale database to store detection data along with a timestamp to know when the detection occurred.
2. Create an API that listens on port 5000 to access the database for both writing and reading data.

#### database.env file
This file contains the default credentials for the database. It is recommended to change them if you want to use the project for anything other than a test.

***API_KEYS***: This field is a small security measure used so that only authorized devices can write to the database. It is highly recommended to generate a new key and not use the current one. If you modify it, you must also modify it in the ***config.json*** file of *Software Detect*.

#### API Operation
The API has the following methods:

**/add [POST]**: Allows adding a new alert to the database and saving the attached image in the post request. Format of the post request:
```
data = {
        'title': '...',
        'message': '...',
        'key' : 'API_KEY'
		}

files = {
        'img': (img_url, img_data, 'image/png')
		}
```
Once it receives a valid request (it has the correct API_KEY), it stores the obtained values in the database and registers them as alerts that **have not been verified**, and also saves the images in a directory with the name of the generated ID for the image for later access.

**/data [GET]**: allows access to the detailed list of all unverified alerts.

**/data/all [GET]**: allows access to the detailed list of all alerts.

**/see/{id} [GET]**: allows viewing the alert associated with ***{id}*** on the screen. Accessing this URL will change the alert associated with that ***{id}*** to **verified** status.

**/img/{id} [GET]**: returns the image associated with ***{id}***.

#### Startup
```
# bash
cd /project/directory/ServerDatabase
docker-compose up --build
```
**Possible Failures**
If for some reason one of the containers fails and stops, wait for the other to initialize correctly and restart it.

```
# bash
docker-compose start
```

### Software Detect
------------
**Before Starting**
This application is designed to be used on an embedded system. 
In this case, it was designed for a Raspberry PI 4, with a [Raspberry Pi High Quality Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/). If using another embedded system and/or camera (incompatible with Picamera2) it will be necessary to change at least the script: ***predict-camera.py***.

It is also necessary to replace `YOUR_SERVER_IP` in the config.json file with the IP of the device running the **API** (see: Server Database). Additionally, if the **API_KEY** has been modified as mentioned earlier, it must also be replaced in this file with the new one.

It is also necessary to have [Python3](https://www.python.org/) installed.

------------
#### Install Dependencies
**Picamera 2**
In case of any possible error with the installation, refer to the official documentation: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
```
# bash
sudo apt install -y python3-picamera2
```

**Ultralytics**
In case of any possible error with the installation, refer to the official documentation: https://docs.ultralytics.com/guides/raspberry-pi/#start-with-docker
```
# bash
sudo apt update
sudo apt install python3-pip -y
pip install -U pip

pip install ultralytics[export]

sudo reboot
```
**Common Error**
If you are unable to use the pip package manager due to this error:
`error: externally-managed-environment`
You may be able to solve it as follows:
```
# bash
sudo apt update
sudo apt install python3-pip -y

sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.bak

pip install -U pip

pip install ultralytics[export]

sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED.bak /usr/lib/python3.11/EXTERNALLY-MANAGED

sudo reboot
```

**Pillow, request and cv2**
```
# bash
sudo apt install -y python3-request
sudo apt install -y python3-pillow
sudo apt install -y python3-opencv
```

#### Startup
```
# bash
cd /project/directory/SoftwareDetect
python3 predict-camera.py
```

### Train
------------
In this folder, there is a notebook for training various YOLO models.
For training, a **dataset** is **required**. If you want to access the dataset used for these trainings, you can find its link in the README.dataset.txt file located in the Train directory as well.
Once you have a suitable dataset to train YOLO models, save it inside the Train directory with the name `Dataset`.

#### Execution
**Install and import ultralytics:**
Run the first two cells:
`! pip install ultralytics`
`from ultralytics import YOLO`

** Select the model to train **
Run the cell with the name of the model you want to train.
E.g., to train YOLOv8n, run the cell:
`modelName = "yolov8n"`
To train other models, refer to the ultralytics wiki: https://docs.ultralytics.com/models/

** Perform the training **
Run the following cell:
```
# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from YAML
##model = YOLO(modelName+".pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="./Dataset/data.yaml", epochs=200, imgsz=640, device=[1], project='runs/detect/'+modelName)
```
If your dataset is not in the directory specified in the cell or has a different name, modify the path in the cell to match.
It is necessary to have the ***data.yaml*** file.
The last cell was created to retrain one of the already trained models with another dataset.

### Utils
------------
In this folder, we can find a JSON file to import into Grafana. This Dashboard allows us to see the detections in real-time.
**Requirements**
- Have Grafana installed
- Install the following Grafana plugins:
	- `Infinity` : https://github.com/grafana/grafana-infinity-datasource
	- `Dynamic image panel` : https://github.com/Dalvany/dalvany-image-panel

**BEFORE IMPORTING THE FILE!**
Replace all occurrences of `YOUR_SERVER_IP` in the file with the IP of the device where you are storing the inference data along with the API to access the database data (see: ***Server Database***).
