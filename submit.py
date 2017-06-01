import os
from git import Repo
import shutil

def main():
    print os.environ['PRIVATE']
    print os.environ['PUBLIC']

if __name__ == "__main__":
    main()
    
    
