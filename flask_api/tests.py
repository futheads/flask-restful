# coding:utf-8
import requests
import json


class APITest(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {}
        self.token = None

    def login(self, phone_number, password, path="/login"):
        payload = {"phone_number": phone_number, "password": password}
        self.headers = {"content-type": "application/json"}
        response = requests.post(url=self.base_url + path, data=json.dumps(payload), headers=self.headers)
        response_data = response.json()
        self.token = response_data.get("token")
        return response_data

    def user(self, path="/user"):
        self.headers = {"token": self.token}
        response = requests.get(url=self.base_url + path, headers=self.headers)
        response_data = response.json()
        return response_data

    def logout(self, path="/logout"):
        self.headers = {"token": self.token}
        response = requests.post(url=self.base_url + path, headers=self.headers)
        response_data = response.json()
        return response_data


if __name__ == "__main__":
    api = APITest("http://localhost:5000/api")
    data = api.login("12345678901", "1234567")
    print(data.get("message"))

    data = api.login("12345678901", "123456")
    print(data.get("message"))

    data = api.user()
    print(data)

    data = api.logout()
    print(data)




