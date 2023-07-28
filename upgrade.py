import yaml
from functools import reduce
import subprocess
import os
from sys import argv

class CodeGenerator:
    def __init__(self):
        self.path = "upgrade_module.yaml"
        self.dest = "backup.sh"
        self.recovery = "recovery.sh"
        self.bin_path = "/opt/odoo/odoo-bin"
        self.conf_path = "/etc/odoo.conf"
        self.up_list = set()
    
    def run(self):
        self.f = open(self.dest, "w")
        self.f.write('#!/bin/bash\n')
        self.g = open(self.recovery, "w")
        self.g.write('#!/bin/bash\n')
        code = self.genCode()
        print(code)
        self.f.close()
        self.g.close()
        
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
            for db in instruc['database']:
                backup = "pg_dump {} > backup_data/{}_backup.sql\n".format(db, db)
                self.f.write(backup)
                self.g.write("dropdb {}\ncreatedb {} --owner='admin'\npsql dbname < backup_data/{}_backup.sql\n".format(db, db, db))
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