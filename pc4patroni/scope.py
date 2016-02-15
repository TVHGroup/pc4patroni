'''
Created on 11-feb.-2016

@author: jankeir
'''

from etcd import EtcdFrontend
from service import Service
import logging
logger = logging.getLogger(__name__)
class Scope(object):
    '''
    classdocs
    '''


    def __init__(self, scopeConfig):
        self.scope = scopeConfig['scope']
        self.dcs = EtcdFrontend(self.scope, scopeConfig['etcd'])
        self.scopestate = None 
        
        self.services = []
        for serviceDict in scopeConfig['services']:
            for key, service in serviceDict.iteritems():
                self.services.append(Service(service))
    
    def checkState(self):
        '''
        Check the state cluster and if it has changed (another master, change is 
        slaves) reload and regenerate all configurations 
        '''
        newstate = self.dcs.getScopeState()
        if self.scopestate != newstate:
            self.scopestate = newstate
            for service in self.services:
                service.reconfigure(newstate)
        else :
            logger.info("Not doing anything for {0}, nothing changed.".format(self.scope))
