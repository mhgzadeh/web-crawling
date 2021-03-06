import json
from abc import ABC, abstractmethod

from mongo import MongoDatabase


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass

    def load(self):
        pass

    def update_flag(self, data):
        pass


class MongoStorage(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data, collection):
        print('collection', collection)
        print(self.mongo.database)
        collection = getattr(self.mongo.database, collection)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)
            print(data['post_id'])

    def load(self):
        print(self.mongo.database.advertisement_links.find({'flag': False}).count())
        return self.mongo.database.advertisement_links.find({'flag': False})

    def update_flag(self, data):
        """
        :param data: get links of advertisements which their flag is
        equal to False.
        this avoids crawling the links which were extracted before.
        :return: each link info
        """
        return self.mongo.database.advertisement_links.find_one_and_update(
            {'_id': data['_id']},
            {'$set': {'flag': True}}
        )


class FileStorage(StorageAbstract):
    def store(self, data, filename):
        filename = filename + '-' + data['post_id']
        with open(f'fixture/adv/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'fixture/adv/{filename}.json')

    def load(self):
        with open('fixture/adv/advertisement_links.json', 'r') as f:
            links = json.loads(f.read())
        return links
