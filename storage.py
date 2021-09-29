import json
from abc import ABC, abstractmethod


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass


class MongoStorage(StorageAbstract):
    def store(self, data, *args):
        print('Mongo has not already been implemented.')


class FileStorage(StorageAbstract):
    def store(self, data, filename, *args):
        with open(f'fixture/adv/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'fixture/adv/{filename}.json')
