import yaml
from functools import reduce
import subprocess
import os

list_addons = ["customized_addons"]

class GetChange:
    def __init__(self):
        self.commit_stat = ""
        try:
            self.commit_stat = subprocess.check_output(['git', 'show', '--stat', 'HEAD'], text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")

    def list_subdirectories(self, addons):
        directory = os.getcwd() + '/' + addons
        target_file = '__manifest__.py'
        subdirectories = set()
        for dir_path, dir_names, filenames in os.walk(directory):
            if target_file in filenames:
                subdirectories.add(os.path.basename(dir_path))
        return subdirectories

    
    def run(self):
        git_change_set = set()
        for addons in list_addons:
            module_list = self.list_subdirectories(addons)
            for module in module_list:
                if self.commit_stat.find(module) != -1:
                    git_change_set.add(module)
        return git_change_set

class CodeGenerator:
    def __init__(self):
        self.up_list = set()
        self.path = "upgrade_module.yaml"
    
    def run(self):
        self.genCode()
        return self.up_list
        
    def genCode(self):
        _, instruc = self.read_yaml_file()
        if instruc['upgrade_modules'] is not None:
            for x in instruc['upgrade_modules']:
                self.up_list.add(x)

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
    if len(missing) > 0:
        result_list = [str(item) for item in missing]
        result_string = ",".join(result_list)
    else:
        result_string = ""
    if len(uplist) == 0:
        result_string = ""
    print("Missing:" + result_string)
    print("Update:" + ",".join(uplist))