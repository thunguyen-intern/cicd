import os, ast
# from test_base_utils.__manifest__ import manifest

class CodeGenerator:
    def __init__(self):
        # self.src = "test_base_utils/tests/test_utils.py"
        self.dest = "test_utils.sh"
        self.bin_path = "/opt/odoo/odoo-bin"
        self.conf_path = "/etc/odoo.conf"
        self.mod_path = "modules.txt"
        self.rootDir = "./odoo-ex-file"
        # self.index = 0
    
    def check_path(self, fpath):
        return os.path.isfile(fpath)
    
    def run(self):
        f = open(self.dest, "w")
        code = self.genCode()
        f.write(code)
        f.close()
    
    def check_module(self, fpath):
        with open(fpath, "w") as f:
            for entry in os.scandir(self.rootDir):
                if entry.is_dir():
                    f.write(entry.name + '\n')
        
        with open(fpath, "r") as f:
            return [modules.strip() for modules in f]

    def genCode(self):
        modules_list = self.check_module(self.mod_path)
        code = "#!/bin/bash \n \n" + self.bin_path + " -c " + self.conf_path
        # Load module
        # First argument from input: database name
        code += " -d " + "abc"
        # Modules
        if len(modules_list) > 0:
            code += " -i "
            code += ','.join(modules_list)
        code += " --stop-after-init \n"
        # Test module
        code += self.bin_path + " -c " + self.conf_path
        code += " -d " + "abc"
        # Modules
        if len(modules_list) > 0:
            code += " --test-tag "
            code += "/"
            code += ',/'.join(modules_list)
        code += " --stop-after-init"
        return code

if __name__ == "__main__":
    code = CodeGenerator()
    code.run()