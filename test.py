import requests

requests.post('http://pipi.dev.corp/auth/login',
              json={
                  "login": "string",
                  "password": "string"
              })

print(requests)
