#!/usr/bin/env python3
import http.client, urllib.parse
import base64
import ssl

class WarehouseClient:



    def __init__(self):
        self.connection = http.client.HTTPSConnection("localhost:443")


    def validAuth(self):
        try:
            creds = base64.b64encode(b'testUsername:testPassword').decode()
            header = {'Authorization': 'Basic ' + creds}
            print("before send request")
            self.connection.request("GET", "/warehouse", headers = header)
            print("before get response")
            resp = self.connection.getresponse()
            if resp.status == 200:
                data = resp.read().decode("utf-8")
                print(data)
                return str(data)
            else:
                print("error")
                raise KeyError
        except KeyError:
            print("error")
            return "KeyError(invalid login params)"


def main():
    auth = WarehouseClient()
    auth.validAuth()

main()