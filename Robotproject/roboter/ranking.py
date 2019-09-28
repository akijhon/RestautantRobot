import csv
import os
import pathlib
import collections

RANKING_COLUMN_NAME='NAME'
RANKING_COLUMN_COUNT='COUNT'
RANKING_CSV_FILE='ranking.csv'


class CsvModel(object):
    def __init__(self,csv_file):
        self.csv_file=csv_file
        if not os.path.exists(csv_file):
            pathlib.Path(csv_file).touch()

class RankingModel(CsvModel):
    def __init__(self,csv_file=None,*args,**kwargs):
        csv_file=RANKING_CSV_FILE
        super().__init__(csv_file,*args,**kwargs)
        self.column = [RANKING_COLUMN_NAME,RANKING_COLUMN_COUNT]
        self.data = collections.defaultdict(int)
        self.load_data()

    def load_data(self):
        with open(self.csv_file,'r+')as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.data[row[RANKING_COLUMN_NAME]]=int(row[RANKING_COLUMN_COUNT])
        return self.data

    def save(self):
        with open(self.csv_file,'w+')as csv_file:
            writer=csv.DictWriter(csv_file,fieldnames=self.column)
            writer.writeheader()

            for name,count in self.data.items():
                writer.writerow({
                    RANKING_COLUMN_NAME:name,
                    RANKING_COLUMN_COUNT:count
                })

    def get_most_popular(self,not_list=None):
        if not_list is None:
            not_list=[]
        if not self.data:
            return None
        sorted_data = sorted(self.data,key=self.data.get,reverse=True)
        for name in sorted_data:
            if name in not_list:
                continue
            return name

    def increment(self,name):
        self.data[name.title()]+=1
        self.save()
