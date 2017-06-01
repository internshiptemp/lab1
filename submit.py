import os
from git import Repo
import shutil

def main():
    print os.environ['PRIVATE']
    print os.environ['PUBLIC']
    
    repo = Repo("./")
    print repo.heads.master
    # print repo.update_environment()
    shutil.move("./.travis/diagnostics/output", "./output.txt")
    assert(os.path.isfile("./output.txt"))
    repo.git.add("output.txt")
    repo.index.commit("Committing diagnostic feedback.")
    repo.push("origin")

if __name__ == "__main__":
    main()
    
    
