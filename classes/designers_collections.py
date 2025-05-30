from classes.gclass import Gclass
class Designers_collections(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
    att = ['_designer_id','_collection_id','_contribution_percentage']

    header = 'Designer_collections'

    des = ['Designer Id','Collection ID','Contribution Percentage']
   
    def __init__(self, designer_id, collection_id, contribution_percentage):
        super().__init__()
        
        self._designer_id = designer_id
        self._collection_id = collection_id
        self._contribution_percentage = float(contribution_percentage)
        Designers_collections.obj[designer_id] = self
        # Add the id to the list of object ids
        Designers_collections.lst.append(designer_id)
        

 
    @property
    def designer_id(self):
        return self._designer_id
    @designer_id.setter
    def designer_id(self, designer_id):
        self._designer_id = designer_id
    
    @property
    def collection_id(self):
        return self._collections_id
    
    @collection_id.setter
    def collection_id(self, collection_id):
        self._collection_id = collection_id
    
    @property
    def contribution_percentage(self):
        return self._contribution_percentage

    @contribution_percentage.setter
    def contribution_percentage(self, contribution_percentage):
        self._contribution_percentage = contribution_percentage
    
