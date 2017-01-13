#!/usr/bin/env python3
import os.path
import json
from json import JSONDecodeError
import sys
import inventory


class Warehouse(inventory.AbstractStorage):

    def __init__(self):
        self.filename = "warehouse.json"
        self.dict = {}
        self.makeWarehouse()

    def getAllItems(self):
        self.loadWarehouse()
        try:
            allItems = json.dumps(self.dict)
            return str(allItems)
        except JSONDecodeError:
            return "JSONDecodeError(could not decode items from dictionary)"

    def getPrefixMatch(self, prefix):
        self.loadWarehouse()
        matching = []
        try:
            for key in self.dict.keys():
                if prefix in key:
                    matching.append(key)
            if len(matching) > 0:
                print(' '.join(matching))
                return ' '.join(matching)
            else:
                raise ValueError
        except ValueError:
            return "ValueError(prefix not found amongst any items)"

    def getItemQuantity(self, item):
        self.loadWarehouse()
        #item = str.lower(item)
        try:
            if item in self.dict.keys():
                item_num = self.dict[item]
                ans = item_num
            else:
                raise ValueError
        except ValueError:
            ans = "ValueError(item not found)"
        return ans

    def filteredQuery(self, output):
        self.loadWarehouse()
        dictCopy = self.dict
        matching = []
        if int(output['lower'][0]) >= int(output['upper'][0]):
            return "ValueError(invalid bounds selected)"
        try:
            for key in dictCopy.keys():
                dictCopy[key] = int(dictCopy[key])
                if dictCopy[key] in range(int(output['lower'][0]), int(output['upper'][0])):
                    matching.append(key)
            if len(matching) > 0:
                print(str(matching))
                return (str(matching))
            else:
                raise ValueError
        except ValueError:
            return "ValueError(could not find item in bounds)"

    def updateItemCount(self, item, updatedDict):
        self.loadWarehouse()
        total = -1
        for key in updatedDict:
            updatedDict[key] = str(updatedDict[key][0])
        if type(item) != str:
            return "TypeError(item is not a string)"
        if item not in self.dict:
            return "KeyError(item not in warehouse)"
        if 'updateItemCount' in updatedDict:
            if int(updatedDict['updateItemCount']) not in range(0,sys.maxsize):
                return "ValueError(invalid decrease value detected)"
            else:
                total = int(updatedDict['updateItemCount'])
        else:
            return "KeyError(did not give count in body)"
        if total <= -1:
            total = int(self.dict[item])
        self.dict[item] = str(total)
        newData = json.dumps(self.dict)
        self.overwriteFile(newData)
        self.loadWarehouse()
        return updatedDict

    def updateWarehouse(self, output):
        self.loadWarehouse()
        wrote = 0
        for key in output.keys():
            wrote +=1
            output[key] = str(output[key][0])
            try:
                item = key
                quantity = str(abs(int(output[key])))
            except KeyError:
                    return "KeyError(invalid item parsed)"
            except ValueError:
                    return "ValueError(invalid item count parsed)"
            self.dict[item] = str(quantity)
            newData = json.dumps(self.dict)
            self.overwriteFile(newData)
            self.loadWarehouse()
        return wrote

    def deleteItem(self, item):
        self.loadWarehouse()
        try:
            quant = self.dict[item]
            del self.dict[item]
            newData = json.dumps(self.dict)
            self.overwriteFile(newData)
            output = "\njust took a hammer to " + str(quant) + str(" ") + str(item) + "s\n"
            print("deleted", item)
        except LookupError:
            return "LookupError(could not find item to delete)"
        return output

    def loadWarehouse(self):
        try:
            with open(self.filename, "r") as fl:
                toJson = fl.read()
                fl.close()
                if toJson:
                    self.dict = json.loads(toJson)
        except (FileNotFoundError, JSONDecodeError) as e:
            print("error in loading from file")
            raise e

    def overwriteFile(self, data):
        try:
            with open(self.filename, "w") as fl:
                fl.write(data)
                fl.close()
        except (FileNotFoundError, TypeError) as e:
            raise e

    def makeWarehouse(self):
        try:
            if not os.path.isfile(self.filename):
                print("making new file...")
                with open(self.filename, "a") as fl:
                    data = {"nexus": "2", "htc": "3", "macbook": "1", "galaxyNote": "7", "surfacePro": "8"}
                    json.dump(data, fl)
                    fl.close()
        except FileExistsError as e:
            raise e
