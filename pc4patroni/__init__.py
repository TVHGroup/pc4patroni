import logging
import sys
import os
import yaml
from scope import Scope
import time

logger = logging.getLogger(__name__)

class PC4Patroni:
    def __init__(self, config):
        self.sleeptime = config['checkfrequency']
        self.scopes = []
        for scope in config['scopes']:
            for key, scopeConfig in scope.iteritems():
                self.scopes.append(Scope(scopeConfig)) 
        
    def run(self):
        while True:
            for scope in self.scopes:
                try:
                    scope.checkState()
                except Exception as e:
                    logger.error("Caught exception {0}".format(e.args))
                finally:
                    time.sleep(self.sleeptime)
        

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    
    if len(sys.argv) == 2 and sys.argv[1] == "--version" :
        print "pc4patroni version 0.1"
        return
    
    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        print ('Usage: {} settings.yml'.format(sys.argv[0]))
        return
    
    with open(sys.argv[1], 'r') as cfStream:
        config = yaml.load(cfStream)

    logger.setLevel(config['logginglevel'])
    pc4patroni = PC4Patroni(config)
    
    try: 
        pc4patroni.run()
    except KeyboardInterrupt:
        pass    
