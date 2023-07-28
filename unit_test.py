import os, ast
# from test_base_utils.__manifest__ import manifest

class CodeGenerator:
    def __init__(self):
        self.bin_path = "/opt/odoo/odoo-bin"
        self.conf_path = "/etc/odoo.conf"
        self.rootDir = "./unit_test"
        self.mod_list = []
    
    def check_path(self, fpath):
        return os.path.isfile(fpath)
    
    def run(self):
        code = self.genCode()
        print(code)
        self.mod_list = []
    
    def check_module(self):
        for entry in os.scandir(self.rootDir):
            if entry.is_dir():
                self.mod_list.append(entry.name)
        return self.mod_list

    def genCode(self):
        modules_list = self.check_module()
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
        code += " --stop-after-init\n"
        code += "echo $?"
        return code

if __name__ == "__main__":
    code = CodeGenerator()
    code.run()