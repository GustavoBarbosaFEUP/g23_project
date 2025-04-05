from classes.gclass import Gclass
import datetime
class Fashion_show(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
   
    att = ['_fashion_id','_show_name','_venue', '_date']

    header = 'Fashion_show'

    des = ['Fashion ID', 'Show Name','Venue', 'Date']
   
    def __init__(self, fashion_id, show_name, venue, date):
        super().__init__()
        self._fashion_id=fashion_id
        self._show_name=show_name
        self._venue=venue
        self._date=datetime.date.fromisoformat(date)
        Fashion_show.obj[fashion_id] = self
        Fashion_show.lst.append(fashion_id)

    @property
    def fashion_id(self):
        return self._fashion_id
    @fashion_id.setter
    def fashion_id(self, fashion_id):
        self._fashion_id = fashion_id
 
    @property
    def show_name(self):
        return self._show_name
    @show_name.setter
    def show_name(self, show_name):
        self._show_name = show_name
        
    @property
    def venue(self):
        return self._venue
    @venue.setter
    def venue(self, venue):
        self._venue = venue
        
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, date):
        self._date = datetime.date.fromisoformat(date)

    


    