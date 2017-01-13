from abc import ABCMeta
import abc


class AbstractStorage(metaclass= ABCMeta):

    @abc.abstractmethod
    def makeWarehouse(self):
        return

    @abc.abstractmethod
    def getAllItems(self):
        return

    @abc.abstractmethod
    def getPrefixMatch(self, prefix):
        return

    @abc.abstractmethod
    def filteredQuery(self, output):
        return

    @abc.abstractmethod
    def getItemQuantity(self, item):
        return

    @abc.abstractmethod
    def deleteItem(self, item):
        return

    @abc.abstractmethod
    def updateItemCount(self, item, updatedDict):
        return

    @abc.abstractmethod
    def updateWarehouse(self, upDatedDict):
        return
