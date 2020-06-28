import pandas as pd
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config

class Philosopher(StructuredNode):
    name = StringProperty(unique_index=True)
    same_line = RelationshipTo('Philosopher', 'SAME_LINE')

class Philosograph(object):
    def __init__(self, uri, user, password):
        config.DATABASE_URL = 'bolt://'+user+':'+password+'@'+uri

    def create_from_csv(self, file_name):
        df = pd.read_csv(file_name, sep=';')
        for row in df.iterrows():
            philosopher = row[1]['philosopher']
            same_line = row[1]['same_line'].split('|')
            
            for other_philosopher in same_line:
                self.__connect(philosopher, other_philosopher)

    def __get_or_create_philosopher(self, name):
        philosopher = Philosopher.nodes.first_or_none(name=name)
        
        if philosopher == None:
            philosopher = Philosopher(name=name).save()
            
        return philosopher

    def __connect(self, from_name, to_name):
        from_philosopher = self.__get_or_create_philosopher(from_name)
        to_philosopher = self.__get_or_create_philosopher(to_name)

        if from_philosopher != None and to_philosopher != None:
            from_philosopher.same_line.connect(to_philosopher)


philosograph = Philosograph('localhost:7687', 'neo4j', 'test')
philosograph.create_from_csv('dataset.csv')