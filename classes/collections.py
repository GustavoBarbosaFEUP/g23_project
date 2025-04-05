from classes.gclass import Gclass
from datetime import date
class Collections(Gclass):
    obj=dict()
    lst=list()
    pos=0
    storkey=""
    att = ['_collection_id', '_style', '_theme', '_season', '_release_year']
    header = 'Collections'
    des = ['Collection Id', 'Style', 'Theme', 'Season', 'Release Year']
    def __init__(self, collection_id:int, style:str, theme:str, season:str, release_year:date):
        super().__init__()  # Chama o construtor da Gclass
        collection_id = self.get_id(collection_id)
        self._collection_id = collection_id
        self._style = style
        self._theme = theme
        self._season = season
        self._release_year = release_year
        Collections.obj[collection_id] = self
        Collections.lst.append(collection_id)
    @property
    def collection_id(self):
        return self._collection_id
    @collection_id.setter
    def collection_id(self,id):
        self._collection_id=id
    @property
    def style(self):
        return self._style
    @style.setter
    def style(self, style):
        self._style=style
    @property
    def season(self):
        return self._season
    @season.setter
    def season(self, season):
        self._season=season
    @property
    def release_year(self):
        return self._release_year
    @release_year.setter
    def release_year(self, datanova):
        if isinstance(datanova, date):
            self._release_year = datanova
        else:
            raise ValueError("Data inválida. Use datetime.date.")
    
    