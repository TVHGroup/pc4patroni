'''
Created on 11-feb.-2016

@author: jankeir
'''
from commonequalitymixin import CommonEqualityMixin
class ScopeState(CommonEqualityMixin):
    '''
    classdocs
    '''
    def __init__(self, master, slaves):
        self.master = master
        self.slaves = slaves
        
            