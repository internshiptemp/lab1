import os
from git import Repo
import shutil

def main():
    print os.environ['PRIVATE']
    print os.environ['PUBLIC']
    
    repo = Repo("./")
    print repo.heads.master
    # print repo.update_environment()
    shutil.copy("./.travis/diagnostics/output", "./output.txt")
    assert(os.path.isfile("./output.txt"))
    repo.git.add("output.txt")
    repo.git.commit("Committing diagnostic feedback.")
    repo.git.push("origin")

if __name__ == "__main__":
    main()
    
    
