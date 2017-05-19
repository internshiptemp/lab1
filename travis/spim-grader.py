#!/usr/bin/python
'''
This program is modified from:
SPIM Auto-grader
Owen Stenson
Grades every file in the 'submissions' folder using every test in the 'samples' folder.
Writes to 'results' folder.

Source: https://github.com/stensonowen/spim-grader
Licence: GPL 2.0
'''
import os, time, re, sys
from subprocess import Popen, PIPE, STDOUT

def run(fn, sample_input='\n'):
    proc = Popen(["spim", "-file", "../submission/"+fn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.stdin.write(sample_input)
    return proc 

def remove_header(output):
    #remove output header
    hdrs = []
    hdrs.append(re.compile("SPIM Version .* of .*\n"))
    hdrs.append(re.compile("Copyright .*, James R. Larus.\n"))
    hdrs.append(re.compile("All Rights Reserved.\n"))
    hdrs.append(re.compile("See the file README for a full copyright notice.\n"))
    hdrs.append(re.compile("Loaded: .*/spim/.*\n"))
    for hdr in hdrs:
        output = re.sub(hdr, "", output)
    return output

def grade(p, f):
    f = open("results/" + f, 'w')
    for proc in p:
        time.sleep(.1)
        if proc.poll() is None:
            #process is either hanging or being slow
            time.sleep(5)
            if proc.poll() is None:
                proc.kill()
                f.write("Process hung; no results to report\n")
                continue
        output = remove_header(proc.stdout.read())
        errors = proc.stderr.read()
        if errors == "":
            f.write(output + '\n')
        else:
            f.write(output + '\t' + errors + '\n')
    f.close() 

def compare(results, expectations):
    expected = True
    diag = open("./diagnostics/{}".format(results), "w")
    results = open("./results/{}".format(results), "r")
    expectations = open("./expectations/{}".format(expectations), "r")

    r = results.readlines()
    e = expectations.readlines() 
    assert(len(e) == len(r))
    for i in range(len(e)):
        status = "PASSED" if r[i] == e[i] else "FAILED"
        diag.write("Test Case {}: {}\n".format(i+1, status))
        diag.write("\tExpected: {}".format(e[i]))
        diag.write("\tReceived: {}".format(r[i]))
        if status == "FAILED":
            expected = False
    results.close()
    expectations.close()
    diag.close()
    
    return expected

# ASSUMPTION: Git repos' names will contain the team name
#             since repos currently take the format "<team_name>_<lab>".
# ASSUMPTION: This script will be called from "<some_path>/<team_repo>/travis/"
def generate_filename(submission, sample):
    try:
        path = os.path.abspath(".")
        team = path[:path.rfind("_")]
        ID = team[team.rfind("/")+1:]
    except:
        ID = submission
    print ID + '_' + sample
    return ID + '_' + sample

def update_results(output_file, passed):
    path = "./diagnostics/{}".format(output_file)
    f = open(path, "r")
    results = f.read()
    f.close()
    f = open(path, "w")
    f.write("{}{}".format(passed.__str__(), "\n"))
    f.write(results)
    f.close()

def input_lines(test, subm, resl, diag):
    # ASSUMPTION: THE FILE THAT WILL BE USED TO GRADE SOME SUBMISSION
    #             WILL SHARE NAMES WITH THE SUBMISSION FILE.
    for submission in os.listdir(subm):
        #cycle through samples to test:
        output_file = ""
        cases_f = submission[:submission.rfind(".")]
        cases = open("{}/{}".format(test, cases_f), 'r')
        results = []
        for line in cases.readlines():
            sample_input = "{}{}".format(line.strip(), "\n")
            #create process
            p = run(submission, sample_input)
            results.append(p)
        cases.close()

        output_file = generate_filename(submission, cases_f)
        grade(results, output_file)
        passed = compare(output_file, cases_f)
        update_results(output_file, passed)

def passed_all():
    path = "./travis/diagnostics/"
    files = os.listdir(path)
    files.remove(".empty")

    for f in files:
        f = open("{}{}".format(path, f), "r")
        lines = f.readlines()
        print lines[0]
        passed = bool(lines[0])
        if not passed:
            return False
    return True
    
# Austen intends to grade labs with a binary blob file
def input_blob(test, subm, resl, diag):
    pass

def main(input_type="line"):
    os.chdir("./travis/")
    #no use in running if content directories aren't present
    test = "test_cases"
    subm = "../submission"
    resl = "results"
    diag = "diagnostics"
    assert os.path.isdir(test)
    assert os.path.isdir(subm)
    assert os.path.isdir(resl)
    assert os.path.isdir(diag)
    if input_type == "line":
        input_lines(test, subm, resl, diag)
    else:
        input_blob(test, subm, resl, diag)

       
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        main()

    if "-t" in args:
        t = args[args.index("-t")+1]
        main(t)

    if "-g" in args:
        if not passed_all():
            exit(1)

