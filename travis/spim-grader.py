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
import os, time, re
from subprocess import Popen, PIPE, STDOUT

def run(fn, sample_input='\n'):
    #start process and write input
    proc = Popen(["spim", "-file", "../submission/"+fn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if sample_input[-1:] != '\n':
        print "Warning: last line (of file below) must end with newline char to be submitted. Assuming it should..."
        sample_input = sample_input + '\n'
    proc.stdin.write(sample_input)
    return proc 

def grade(p, f):
    #arg = process running homework file, file to write results to
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
        output = proc.stdout.read()
        #remove output header
        hdrs = []
        hdrs.append(re.compile("SPIM Version .* of .*\n"))
        hdrs.append(re.compile("Copyright .*, James R. Larus.\n"))
        hdrs.append(re.compile("All Rights Reserved.\n"))
        hdrs.append(re.compile("See the file README for a full copyright notice.\n"))
        hdrs.append(re.compile("Loaded: .*/spim/.*\n"))
        for hdr in hdrs:
            output = re.sub(hdr, "", output)
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
    return ID + '_' + sample

def main():
    #no use in running if content directories aren't present
    test = "test_cases"
    subm = "../submission"
    resl = "results"
    diag = "diagnostics"
    assert os.path.isdir(test)
    assert os.path.isdir(subm)
    if os.path.isdir(resl) is False:
        assert os.path.isfile(resl) == False
        os.makedirs(resl)
    # cycle through files to grade:
    # TODO: IF STUDENTS WILL ONLY SUBMIT 1 FILE PER LAB, THEN NO NEED TO CYCLE
    for submission in os.listdir(subm):
        #cycle through samples to test:
        output_file = ""
        for f in os.listdir(test):
            cases = open("{}/{}".format(test, f), 'r')
            #read sample input; fix windows EOL char
            results = []
            for line in cases.readlines():
                sample_input = line
                sample_input = sample_input.replace('\r', '')
                #create process
                p = run(submission, sample_input)
                results.append(p)
            output_file = generate_filename(submission, f)
            grade(results, output_file)
            passed = compare(output_file, f)
            if not passed:
                exit(1)

if __name__ == "__main__":
    main()

