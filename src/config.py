import os 
import yaml

class Config():
    
    def __init__(self, path):
        if not path:
            dir     = os.path.dirname(__file__)
            project = os.path.dirname(dir)
            path    = os.path.join(project, "config.yml")

        with open(path) as f:
            self.cfg = yaml.safe_load(f)

    def __getitem__(self, key):
        return self.cfg[key]
    
    def get(self, key, default=None):
        return self.cfg.get(key, default)
    
