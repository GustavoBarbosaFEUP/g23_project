from classes.gclass import Gclass
class Designers(Gclass):
    obj=dict()
    lst=list()
    pos=0
    storkey=""
    att = ['_designer_id', '_name', '_nationality']
    header = 'Designers'
    des = ['Id', 'Name', 'Nationality']
    def __init__(self, designer_id:int, name:str, nationality:str):
        super().__init__()  
        designer_id = self.get_id(designer_id)
        self._designer_id = designer_id
        self._name = name
        self._nationality = nationality
        Designers.obj[designer_id] = self
        Designers.lst.append(designer_id)
        
  
    @property
    def designer_id(self):
        return self._designer_id
    @designer_id.setter
    def designer_id(self,id):
        self._designer_id=id
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name=name
    @property
    def nationality(self):
        return self._nationality
    @nationality.setter
    def nationality(self, nationality):
        self._nantionality=nationality
    
d=Designers(12,' gus', 'num')

