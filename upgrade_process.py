import yaml
from functools import reduce
import subprocess
import os

class GetChange:
    def __init__(self):
        self.commit_stat = ""
        try:
            self.commit_stat = subprocess.check_output(['git', 'show', '--stat', 'HEAD'], text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")

    def list_subdirectories(self):
        directory = os.getcwd() + '/customized_addons'
        subdirectories = set()
        for entry in os.scandir(directory):
            if entry.is_dir():
                subdirectories.add(entry.path)
        return subdirectories

    
    def run(self):
        git_change_set = set()
        text_detect = "customized_addons"
        stat_by_line = self.commit_stat.split("\n")
        for line in stat_by_line:
            pos = line.find(text_detect)
            if pos != -1:
                git_change_set.add(line.split("/")[1])
        existing_set = self.list_subdirectories()
        change_set = existing_set.intersection(git_change_set)
        return change_set

class CodeGenerator:
    def __init__(self):
        self.path = "upgrade_module.yaml"
        self.dest = "upgrade.sh"
        self.bin_path = "/opt/odoo/odoo-bin"
        self.conf_path = "/etc/odoo.conf"
        self.up_list = set()
    
    def run(self):
        f = open(self.dest, "w")
        code = self.genCode()
        f.write(code)
        f.close()
        return self.up_list
        
    def genCode(self):
        _, instruc = self.read_yaml_file()
        code = "#!/bin/bash \n \n" + self.bin_path + " -c " + self.conf_path
        if len(instruc['upgrade_modules']) > 0:
            code += " -u " + ','.join(instruc['upgrade_modules'])
            for x in instruc['upgrade_modules']:
                self.up_list.add(x)
        if len(instruc['install_modules']) > 0:
            code += " -i " + ','.join(instruc['install_modules'])
        if len(instruc['database']) > 0:
            code += " -d " + ','.join(instruc['database'])
        return code

    def read_yaml_file(self):
        with open(self.path, 'r') as file:
            data = yaml.safe_load(file)
        ver = list(data.keys())[0]
        instruc = list(data.values())[0]
        return ver, instruc
    
if __name__ == "__main__":
    code = CodeGenerator()
    uplist = code.run()
    git_change = GetChange()
    change_list = git_change.run()
    missing = change_list - uplist
    missing = ('A', 'B')
    if len(missing) > 0:
        result_list = [str(item) for item in missing]
        result_string = ",".join(result_list)
        print(result_string)
