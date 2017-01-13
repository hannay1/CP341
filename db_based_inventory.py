#!/usr/bin/env python3
import json
import sqlite3
import sys
import inventory


class WarehouseDB(inventory.AbstractStorage):

    def __init__(self):
        self.dbName = "warehouse.db"
        self.connex = sqlite3.connect(self.dbName)
        self.cur = self.connex.cursor()
        self.makeWarehouse()

    def getPrefixMatch(self, prefix):
        prefix = "%" + prefix + "%"
        #prefix = prefix + "%"
        try:
            print(type(prefix))
            self.cur.execute('SELECT * FROM warehouse WHERE item LIKE?', [prefix])
            self.connex.commit()
            result = {}
            for row in self.cur:
                result[row[0]] = row[1]
            if len(result) > 0:
                items = []
                for key in result:
                    items.append(key)
                return ' '.join(items)
            else:
                raise ValueError
        except ValueError:
            print("no such item")
            return "ValueError(prefix not found amongst any items)"

    def filteredQuery(self, output):
        if int(output['lower'][0]) >= int(output['upper'][0]):
            return "ValueError(invalid bounds selected)"
        try:
            self.cur.execute('SELECT * FROM warehouse WHERE quantity >=? AND quantity <=?', [int(output['lower'][0]), int(output['upper'][0])])
            self.connex.commit()
            result = {}
            #iterative query
            for row in self.cur:
                result[row[0]] = row[1]
            if len(result) > 0:
                return str(result)
            else:
                raise ValueError
        except ValueError:
            return "KeyError(could not find any bounds)"

    def makeWarehouse(self):
        query = 'CREATE TABLE IF NOT EXISTS warehouse (item TEXT, quantity INTEGER)'
        self.cur.execute(query)
        self.cur.execute('SELECT * FROM warehouse')
        self.connex.commit()
        if self.cur.fetchone() is None:
            print("writing init entries...")
            vals = [("nexus", 2), ("macbook", 1), ("galaxyNote", 1), ("htcOne", 3), ("surfacePro", 8)]
            self.cur.executemany('INSERT INTO warehouse VALUES (?,?)', vals)
            self.connex.commit()
        else:
            return

    def getAllItems(self):
        try:
            query = 'SELECT * FROM warehouse'
            self.cur.execute(query)
            ans = self.cur.fetchall()
            allItems = json.dumps(ans)
            return str(allItems)
        except sqlite3.OperationalError:
            print("no such table")
            return "OperationalError(warehouse table does not exist)"

    def getItemQuantity(self, item):
        try:
            self.cur.execute('SELECT * FROM warehouse WHERE item=?', [item])
            ans = self.cur.fetchall()
            if ans:
                print(ans)
                return str(ans)
            else:
                raise ValueError
        except ValueError:
            print("no such item")
            return "ValueError(item does not exist in warehouse)"

    def deleteItem(self, item):
        try:
            deleted = self.cur.execute('DELETE FROM warehouse WHERE item=?', [item])
            self.connex.commit()
            if deleted:
                return "I just took a hammer to all the " + str(item) + "s"
            else:
                raise ValueError
        except ValueError:
            print("no such item")
            return "ValueError(item does not exist in warehouse)"

    def updateItemCount(self, item, updatedDict):
        if type(item) != str:
            return "TypeError(item is not a string)"
        if 'updateItemCount' in updatedDict:
            param = updatedDict['updateItemCount'][0]
            if int(param) not in range(0,sys.maxsize):
                return "ValueError(invalid decrease value detected)"
            else:
                try:
                    self.cur.execute('UPDATE warehouse SET quantity=? WHERE item=?',[int(updatedDict['updateItemCount'][0]),item])
                    self.connex.commit()
                    print(updatedDict)
                    return updatedDict
                except sqlite3.OperationalError:
                    return "OperationalError(could not perform query)"
        else:
            return "KeyError(cant find update params)"

    def updateWarehouse(self, upDatedDict):
        wrote = 0
        for key in upDatedDict.keys():
            upDatedDict[key] = str(upDatedDict[key][0])
            try:
                item = key
                quantity = upDatedDict[key]
                if abs(int(quantity)) not in range(0,sys.maxsize):
                    return -1#"ValueError(invalid item count parsed)"
                self.cur.execute('UPDATE warehouse SET quantity=? WHERE item=?',[abs(int(quantity)),str(item)])
                self.connex.commit()
                self.cur.execute('SELECT * FROM warehouse WHERE item=?', [str(item)])
                self.connex.commit()
                if self.cur.fetchone() is None:
                    self.cur.execute('INSERT INTO warehouse VALUES (?,?)', [str(item), abs(int(quantity))])
                    self.connex.commit()
                    wrote +=1
            except KeyError:
                return -2 #"KeyError(invalid item parsed)"
            except ValueError:
                return -1#"ValueError(invalid item count parsed)"
        print(wrote)
        return wrote
