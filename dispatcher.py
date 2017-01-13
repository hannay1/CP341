#!/usr/bin/env python3
import urllib.parse


class Dispatcher:

    def __init__(self, wh):
        self.validBodyParams = ['updateItemCount', 'upper', 'lower'] #add more later?
        self.warehouse = wh

    def parseCRUD(self, environ):
        #routes HTTP requests from server to relevant method below
        uri = environ['PATH_INFO']
        uri = uri.split('/')
        for place in uri:
            if place == '':
                uri.remove(place)
        if uri[0].lower() == 'warehouse':
            if environ['REQUEST_METHOD'] == 'POST':
                response = self.createCRUD(environ, uri)
            elif environ['REQUEST_METHOD'] == 'GET':
                response = self.retrieveCRUD(environ,uri)
            elif environ['REQUEST_METHOD'] == 'PUT':
                response = self.updateCRUD(environ, uri)
            elif environ['REQUEST_METHOD'] == 'DELETE':
                response = self.deleteCRUD(uri)
            return [response]
        else:
            return ["AssertionError (no warehouse specified)"]

    def createCRUD(self,environ, uri):
        #maps POST requests to addItem method in Warehouse
        #contentLength = int(environ['CONTENT_LENGTH'])
        if environ['CONTENT_LENGTH'] != '' and len(uri) == 1:
            #update warehouse with new entry(s)
            body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
            output = urllib.parse.parse_qs(body.decode('utf-8'))
            numNewItems = self.warehouse.updateWarehouse(output)
        else:
            return "AttributeError(could not read item)"
        if numNewItems > 0:
            return str(numNewItems)
        else:
            return "ValueError(no new items to add)"


    def retrieveCRUD(self,environ,uri):
        #maps GET requests to getInventory/getItem methods in Warehouse
        #contentLength = int(environ['CONTENT_LENGTH'])
        if environ['CONTENT_LENGTH'] == '':
            if len(uri) == 1:
                #get entire JSON object
                response = self.warehouse.getAllItems()
            elif len(uri) == 2 and len(uri[1]) > 0:
                #get specific item count
                if 'match' in uri[1]:
                    params = uri[1].split("=")
                    prefix = params[1]
                    print(prefix)
                    response = self.warehouse.getPrefixMatch(prefix)
                else:
                    response = self.warehouse.getItemQuantity(uri[1])
        else:
            try:
                body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
                output = urllib.parse.parse_qs(body.decode('utf-8'))
                for key in output:
                    if key not in self.validBodyParams:
                        raise KeyError
                response = self.warehouse.filteredQuery(output)
            except AttributeError:
                return "AttributeError(body not properly formatted)"
            except KeyError:
                return "KeyError(please specify lower and upper bounds)"
        return response

    def updateCRUD(self,environ, uri):
        #maps POST/PUT requests to updateItemQuantity method in Warehouse
        #contentLength = int(environ['CONTENT_LENGTH'])
        if environ['CONTENT_LENGTH'] != '' and len(uri) == 2:
            #update warehouse with new entry(s)
            if type(uri[1]) != str:
                #raise TypeError("TypeError(item is not a string)")
                return "TypeError(item is not a string)"
            try:
                body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
                output = urllib.parse.parse_qs(body.decode('utf-8'))
                output = self.warehouse.updateItemCount(uri[1], output)
            except AttributeError as ae:
                #raise ae
                return "AttributeError(body not properly formatted)"
            #output = self.warehouse.updateItemCount(uri[1], output)
            for key in output:
                if key not in self.validBodyParams:
                    #raise KeyError
                    return "KeyError(invalid parameter detected)"
            if 'updateItemCount' in output:
                resp = str(output['updateItemCount'])
                return resp
            else:
                #raise LookupError
                return "LookupError(could not find item to update)"

    def deleteCRUD(self,uri):
        #maps DELETE requests to deleteItem method in Warehouse
        if len(uri) == 2 and len(uri[1]) > 0:
            #update warehouse with new entry(s)
            response = self.warehouse.deleteItem(uri[1])
        else:
            #raise ValueError("did not specify delete item")
            response = "ValueError(didn't specify item to delete)"
        return response
