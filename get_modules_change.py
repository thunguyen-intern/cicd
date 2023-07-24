import os
from sys import argv
import yaml
import subprocess
from functools import reduce

class GetChange:
    def __init__(self):
        self.commit_stat = ""
        try:
            self.commit_stat = subprocess.check_output(['git', 'show', '--stat', 'HEAD'], text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    
    def run(self):
        change_set = set()
        text_detect = "customized_addons"
        stat_by_line = self.commit_stat.split("\n")
        for line in stat_by_line:
            pos = line.find(text_detect)
            if pos != -1:
                change_set.add(line.split("/")[1])
        print(change_set)
    
if __name__ == "__main__":
    code = GetChange()
    code.run()
