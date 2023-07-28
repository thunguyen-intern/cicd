import yaml
from functools import reduce
import subprocess
import os

class CodeGenerator:
    def __init__(self):
        self.path = "upgrade_module.yaml"
        self.dest = "upgrade.sh"
        self.bin_path = "/opt/odoo/odoo-bin"
        self.conf_path = "/etc/odoo.conf"
        self.up_list = set()
    
    def run(self):
        # f = open(self.dest, "w")
        code = self.genCode()
        print(code)
        # return self.up_list
        
    def genCode(self):
        _, instruc = self.read_yaml_file()
        code = "#!/bin/bash \n \n" + self.bin_path + " -c " + self.conf_path
        if instruc['upgrade_modules'] is not None:
            code += " -u " + ','.join(instruc['upgrade_modules'])
            for x in instruc['upgrade_modules']:
                self.up_list.add(x)
        if instruc['install_modules'] is not None:
            code += " -i " + ','.join(instruc['install_modules'])
        if instruc['database'] is not None:
            code += " -d " + ','.join(instruc['database'])
        code += " --stop-after-init\n"
        code += "echo $?"
        return code

    def read_yaml_file(self):
        with open(self.path, 'r') as file:
            data = yaml.safe_load(file)
        ver = list(data.keys())[0]
        instruc = list(data.values())[0]
        return ver, instruc
    
if __name__ == "__main__":
    code = CodeGenerator()
    code.run()