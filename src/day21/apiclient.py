import requests

url = "http://localhost:8000"

incident = {
    "service": "Payment Service",
    "description": "Payments are failing after today's deployment",
    "severity": "HIGH"
}
response = requests.get(url ) 
response.raise_for_status()
print(response.json())

# get call to the /incidents endpoint
response = requests.get(url+ "/chat", 
    params={"message": "2*2"})

response.raise_for_status()
print(response.json())



# post call to the /incidents endpoint
response = requests.post(
    url + "/incidents",
    json=incident
)

response.raise_for_status()

result = response.json()

print(result)