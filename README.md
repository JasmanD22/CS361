To programmatically request room temperature data from the microservice, you can send an HTTP GET request to the /room_temperatures endpoint. Below is an example using Python's requests library:

import requests

url = 'http://localhost:5000/room_temperatures'
response = requests.get(url)

if response.status_code == 200:
    room_temperatures = response.json()
    print("Room temperatures:", room_temperatures)
else:
    print("Failed to retrieve room temperatures:", response.status_code)
Will replace 'http://localhost:5000/room_temperatures' with the actual URL of your microservice unless you want it to stay local.

To programmatically update room temperature data in the microservice, you can send an HTTP POST request to the /room_temperatures endpoint with the new data in JSON format. Here's an example using Python's requests library:

import requests

url = 'http://localhost:5000/room_temperatures'

new_temperatures = {}
with open('room_temperatures.txt', 'r') as file:
    for line in file:
        room, temperature = line.strip().split(', ')
        new_temperatures[room] = int(temperature)

response = requests.post(url, json=new_temperatures)

if response.status_code == 200:
    print("Room temperatures updated successfully")
else:
    print("Failed to update room temperatures:", response.status_code)

UML:
![I Main Screen o Check box for](https://github.com/JasmanD22/CS361/assets/122345230/f606f2fd-9844-4d01-81a1-5b2d752eec59)

