from flask import Flask
import os
from dotenv import load_dotenv
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.components.sensor import Sensor
from viam.services.mlmodel import MLModelClient
from viam.services.vision import VisionClient



load_dotenv()
app = Flask(__name__)

VIAM_API_KEY = os.getenv('VIAM_API_KEY')
VIAM_API_KEY_ID = os.getenv('VIAM_API_KEY_ID')
VIAM_API_ADDRESS = os.getenv('VIAM_API_ADDRESS')


async def connect():
    opts = RobotClient.Options.with_api_key(
            # Replace "<API-KEY>" (including brackets) with your machine's api key 
        api_key=VIAM_API_KEY,
        # Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
        api_key_id=VIAM_API_KEY_ID
    )
    return await RobotClient.at_address(VIAM_API_ADDRESS, opts)

async def viam_main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)
    
    
    # sensor-1
    sensor_1 = Sensor.from_robot(machine, "sensor-1")
    sensor_1_return_value = await sensor_1.get_readings()
    
    await machine.close()
    return sensor_1_return_value

def make_html_file():
    detection_string = 'default'
    sensor_1_return_value = asyncio.run(viam_main())
    print(f"sensor-1 get_readings return value: {sensor_1_return_value}")
    print(type(sensor_1_return_value))
    
    if sensor_1_return_value['person_detected']:
        detection_string = 'YES!!!!!'
    else:
        detection_string = 'No...'
    
    sec_app_html = '''
    <html>
        <head>
            <title>My Viam Security Application!</title>
        </head>
        <body>
            <h1>My Viam Security Application!</h1>
            <h2>Has a person been detected?<br><br>'''+detection_string+'''</h2>
        </body>
    </html>

    '''
    return sec_app_html

@app.route("/")
def my_application():
    return make_html_file()






