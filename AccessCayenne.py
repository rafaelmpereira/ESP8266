# https://community.mydevices.com/t/python-code-to-access-basic-cayenne-api/12343

import requests

import base64

import configparser
config = configparser.ConfigParser()


def get_mqtt_token(mqtt_username, mqtt_password ):
        string = mqtt_username + ':' + mqtt_password
        print(string)
        data = base64.b64encode(string.encode())
        mqtt_token = data.decode("utf-8")
        config['DEFAULT']['mqtt_token'] = mqtt_token
        with open('credentials.ini', 'w') as configfile:
                config.write(configfile)
        return (mqtt_token)

def get_access_token(client_id, client_secret, username, password):
        response = requests.post('https://accounts.mydevices.com/auth/realms/cayenne/protocol/openid-connect/token',
                data={'grant_type':'password',
                'client_id':client_id,
                'client_secret':client_secret,
                'username':username,
                'password':password },
                headers={'content-type':'application/x-www-form-urlencoded'})
        payload = response.json()
        access_token = payload['access_token']
        print('Access_Token = ' + access_token)
        config['DEFAULT']['access_token'] = access_token
        with open('credentials.ini', 'w') as configfile:
                config.write(configfile)
        return (access_token)

def get_latest_history(access_token, device_id, sensor_id):
        bearer = 'Bearer '+ access_token
        URL = 'https://platform.mydevices.com/v1.1/telemetry/'+device_id+'/sensors/'+sensor_id+'/summaries?type=latest'
        response = requests.get(URL,
                headers={'authorization': bearer},)
        payload = response.json()
        data = payload[0]['v']
        print ('Data history = %d' %data)

def get_user_credentials():
        client_id  = input ("Enter your client_id:  ")
        client_secret  = input ("Enter your client_Secret:  ")
        username = input ("Enter your Username:  ")
        password  = input ("Enter your Password:  ")
        mqtt_username = input("Enter your MQTT Username")
        mqtt_password = input("Enter your MQTT Password")
        config['DEFAULT']['client_id'] = client_id
        config['DEFAULT']['client_secret'] = client_secret
        config['DEFAULT']['username'] = username
        config['DEFAULT']['password'] = password
        config['DEFAULT']['mqtt_username'] = mqtt_username
        config['DEFAULT']['mqtt_password'] = mqtt_password

        with open('credentials.ini', 'w') as configfile:
                config.write(configfile)
        return client_id, client_secret, username, password, mqtt_username, mqtt_password;


def get_device_info():
        device_id  = input ("Enter your Device_ID:  ")
        sensor_id  = input ("Enter your Sensor_ID:  ")
        return device_id, sensor_id;

def get_client_data():
        config.read('credentials.ini')
        client_id = config['DEFAULT']['client_id']
        client_secret = config['DEFAULT']['client_secret']
        username = config['DEFAULT']['username']
        password = config['DEFAULT']['password']
        access_token = config['DEFAULT']['access_token']
        mqtt_token = config['DEFAULT']['mqtt_token']
        mqtt_username = config['DEFAULT']['mqtt_username']
        mqtt_password = config['DEFAULT']['mqtt_password']
        return client_id, client_secret, username, password, access_token, mqtt_token, mqtt_username, mqtt_password;

def get_history(access_token, device_id, sensor_id):
        list = []
        duration = input("Enter the history duration. example: 1month or 2month or 3month and so on ")
        bearer = 'Bearer '+ access_token
        URL = 'https://platform.mydevices.com/v1.1/telemetry/'+device_id+'/sensors/'+sensor_id+'/summaries?endDateLatest=true&type='+duration
        response = requests.get(URL,
                headers={'authorization': bearer},)
        history_list = response.json()
        for item in history_list:
                #print(item['v'])
                list.append(item['v'])
        print(list)
        print()

def publish_data(mqtt_token):
        device_id  = input ("Enter your Device_ID:  ")
        URL = 'https://api.mydevices.com/things/'+device_id+'/data'
        channel  = int(input("Enter channel:  "))
        value  = int(input("Enter value:  "))
        unit = input ("Enter unit:  ")
        type  = input ("Enter type:  ")
        basic = 'Basic '+mqtt_token
        headers= {'authorization': basic,
		'content-type': 'application/json'}
        data = [{'value': value,
                 'channel': channel,
                  'unit': unit,
                  'type' : type
                }]
        response = requests.post(URL, json=data, headers=headers)
        print(response)
x = 0

while True:
        if x == 0:
                print ("/////////////////////////////////////////////////")
                print ("")
                print ("WELCOME TO CAYENNE API")
                print (" 1 = For new number ")
                print (" 2 = Existing USer")
                user_input = int(input("Enter the appropriate number "))
                if user_input == 1 :
                        client_id, client_secret, username, password = get_user_credentials()
                        print ("Welcome" + username)
                        access_token = get_access_token(client_id, client_secret, username, password)
#                        mqtt_token = get_mqtt_token(username, password)
                elif  user_input == 2:
                        client_id, client_secret, username, password, access_token, mqtt_token, mqtt_username, mqtt_password = get_client_data()
                        print ("Welcome back " + username)
                x = 1

        if x == 1:
                print ("/////////////////////////////////////////////////")
                print (" 1 = Get new Access Token")
                print (" 2 = Get new Mqtt Token")
                print (" 3 = Get latest sensor data")
                print (" 4 = Get sensor history data")
                print (" 5 = Publish data")
                get_input = int(input("Enter the appropriate number "))
                if get_input == 1:
                        access_token = get_access_token(client_id, client_secret, username, password)
                elif get_input == 2:
                        mqtt_token = get_mqtt_token(mqtt_username, mqtt_password)
                elif get_input == 3:
                        device_id, sensor_id = get_device_info()
                        get_latest_history(access_token, device_id, sensor_id)
                elif get_input == 4:
                        device_id, sensor_id = get_device_info()
                        get_history(access_token, device_id, sensor_id)
                elif get_input == 5:
                        publish_data(mqtt_token)
