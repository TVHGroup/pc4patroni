'''
Created on 11-feb.-2016

@author: jankeir
'''
import subprocess
import logging
import jinja2
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class ConfigFile(object):
    j2_env = Environment(loader=FileSystemLoader('/', followlinks=True))
    def __init__(self, configFile):
        self.template = self.j2_env.get_template(configFile['template'])
        self.destination = configFile['destination']
    def regenerate(self, servers):
        with open(self.destination,"wb") as fh:
            fh.write(self.template.render(master=servers.master, slaves=servers.slaves))

class Service(object):
    '''
    classdocs
    '''
    def __init__(self, serviceConfig):
        '''
        Constructor
        '''
        self.configFiles = []
        for fileDict in serviceConfig['configfiles']:
            for key, file in fileDict.iteritems():
                self.configFiles.append(ConfigFile(file))
        self.reloadCommand = serviceConfig['reloadcommand']
    
    def reconfigure(self, servers):
        for configFile in self.configFiles:
            configFile.regenerate(servers)
        ret = subprocess.call(self.reloadCommand, shell=True)
        logger.warning("Service reload triggered: reload command {0} exited with exit code {1}".format(self.reloadCommand, ret))
