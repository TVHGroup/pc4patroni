'''
Created on 11-feb.-2016

@author: jankeir
'''
from scopestate import ScopeState
from patroni import Etcd

class EtcdFrontend(object):
    '''
    classdocs
    '''

    def __parseHostnameAndPortFromConnectionString(self, connectionString):
        ''' input: 'postgres://user:pass@host.name:port/postgres'
        '''
        temp = connectionString.split("@")[1].split("/")[0].split(":")
        return { "hostname": temp[0], "port": temp[1]}
        pass

    def __init__(self, scope, etcdConfig):
        '''
        Constructor
        '''
        self.host = etcdConfig['host']
        self.dcs =  Etcd(scope, {"host":etcdConfig['host'], "scope": scope} )
        
    def getScopeState(self):
        self.dcs.reset_cluster()
        cluster = self.dcs.get_cluster()
        master = self.__parseHostnameAndPortFromConnectionString(cluster.leader.member.data['conn_url']) 
        slaves = [] 
        for member in cluster.members:
            if member.data['role'] == 'replica' and member.data['state'] == 'running':
                slaves.append(self.__parseHostnameAndPortFromConnectionString(member.data['conn_url']) )
        return ScopeState(master, slaves)
