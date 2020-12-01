import subprocess
import yaml
import os
import pandas as pd
from difflib import SequenceMatcher


def getDirOrFile(dir_name, DirEntry_iterator, threshold=0.8):
    '''This function compute the similarity index between a directory name and a list of DirEntry (i.e. contains path, and name of the directory)
    :parameter
    dir_name: the name of the desired directory (e.g. 1_Assembly)
    DirEntry: ScandirIterator of directories and files found in specific folder
    threshold: similarity ratio threshold
    :return
    target_dir=DirEntry object: if the dir_name match one of the directory's name in the list. And None otherwise.
    '''
    DirEntry_list = list(DirEntry_iterator)
    similarity_list = [(SequenceMatcher(None, dir_name.lower(), dir_entry.name.lower()).ratio()) for dir_entry in DirEntry_list]
    if len(similarity_list)==0:
        return None

    max_index = similarity_list.index(max(similarity_list))

    if (similarity_list[max_index]>=threshold):
        return DirEntry_list[max_index]
    else:# if nothing is found
        return None
def markFile(file_path, emulator_name):
    '''This function execute the command HardwareSimulation file.tst
    :parameter
    - file_path: sting that contains the file full path (e.g. ./submissions/student1/exer3/1_assembly/Factorial.tst)
    - emulator_name: string that contains either HardwareSimulator or CPUEmulator
    :returns
    - is_successful : True if success or False otherwise
    - feedback : contains error messages if found or constant string SUCCESS otherwise
    '''

    command=subprocess.run([emulator_name,file_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)

    cmd_output = command.stdout
    feedback = command.stderr
    is_successful = False
    if(cmd_output.find("Comparison ended success")>=0):
        is_successful = True
        feedback = SUCCESS

    return is_successful, feedback.rstrip('\n') # "End of ... succussfuly\n" --> "End of ... succussfuly"

def getYAMLConfig():
    '''This function return a dictionary that contains all configurations for the exersise'''
    expected_config_file_name = "Exer_conf.yml"
    file=getDirOrFile(expected_config_file_name, os.scandir())
    if not file:
        printError("I didn't find the configuration file '%s' in the current directory\n %s" % (expected_config_file_name, root))
    with open(file.name, "r") as ymlfile:
        configurations = yaml.load(ymlfile, Loader=yaml.FullLoader)

    return configurations

def checkStructure():
    '''This function checks for the following:
        - YAML configuration exists
        - Submissions folder exists
        :return
        root : Current directory path
        submissions : The directory path that has all students' submissions
        '''
    root = os.path.dirname(os.path.realpath(__file__))

    # get list of all directories
    dir_list = os.scandir()

    submissions_dir = getDirOrFile("submissions",dir_list)

    if not submissions_dir:# if submissions_dir is None
        printError("submissions folder is not found in the current directory!!\n %s "%root)

    return root,submissions_dir

def printError(message):
    print("Error:\n"+message,flush=True)
    input("Press Enter to Exit...")
    exit(-1)

def _searchForDirOrFile(name,current_dir):
    '''This is a recursive function that search for a specific directory in a breadth first fashion
    (i.e. search first for the name in the current_dir then go deeper)
    :parameter
    name: the target file\folder name
    dir: is a DirEntry object
    :return
    target_dir: is a DirEntry object that contains the dir. If not found None is returned
    '''
    target_dir=None
    dir_iterator= os.scandir(current_dir)
    found = getDirOrFile(name,dir_iterator)

    if found:#if we found the name in the current_dir return
        target_dir = found
        return target_dir

    #if we didn't find the name in the current_dir search deeper
    dir_iterator= os.scandir(current_dir)
    for dir_temp in dir_iterator:
        if dir_temp.is_dir():
            found=_searchForDirOrFile(name, dir_temp)
            if found:  # if we found the name in the current_dir return
                target_dir = found
                return target_dir

    return target_dir
def mark_submission(student_dir):
    '''This method is responsible for doing the marking for each section in the exercise for one student.
    It uses the global variable "configurations" defined in the __main__ to get essential information
    :parameter
    - student_dir:A DirEntry object that has the directory info of the current submission
    :returns
    - student_result dictionary that contains:
        - marks_dic: dictionary that contains the name of the file with its corresponding deserved mark
        - feedbacks_dic: dictionary that contains all the feedback for each .tst file.
        - mistakes_feedback_list: list of tuple (file_name, error_message) that contains only mistakes.
        This list is subset of feedbacks_dic
    '''
    student_name = student_dir.name.split("_")[0] # Zaid Ahmad_3522_submision --> Zaid Ahmad
    marks_dic={} #dictionary that holds all the marks for each .tst file (e.g. "CPU.tst":10, "hack.tst":50 ...etc)
    feedbacks_dic={} #dictionary that holds all the feedbacks for each .tst file (e.g. "CPU.tst":10, "hack.tst":50 ...etc)


    #for each section in the exercise get the .tst files and test them
    for section in configurations:
        emulator_name = configurations[section]["Emulator_Name"]
        student_tst_list = configurations[section]["Test_Files"]

        for tst_mark_yml in student_tst_list:# run the emulator for each .tst file and get the result
            file_name, mark = tst_mark_yml.split(" ") # Mult.tst 20 --> tst="Mult" and mark="20"
            mark = int(mark) # mark = "20" --> 20

            tst_file = _searchForDirOrFile(file_name,student_dir)

            if tst_file:
                is_success, feedback = markFile(tst_file.path,emulator_name)
                marks_dic[file_name] = 0
                feedbacks_dic[file_name]= feedback
                if is_success:
                    marks_dic[file_name] = mark
            else: # if we didnt find the tst_file print error
                marks_dic[file_name] = 0
                feedbacks_dic[file_name] = "Error: %s not found!!"%file_name

    mistakes_feedback = [(key, feedbacks_dic[key]) for key in feedbacks_dic if feedbacks_dic[key] != SUCCESS ]
    if not mistakes_feedback: # if the mistake feedback is empty list make it ""
        mistakes_feedback = "No Mistakes"

    total_marks = sum(marks_dic.values())
    print( "{}:{}%. {}".format(student_name, total_marks, mistakes_feedback), flush=True )

    one_row_result = marks_dic
    one_row_result["Total"] = total_marks
    one_row_result["Feedback"] = str(mistakes_feedback)

    # student_result = {"student_name":student_name, "marks_dic":marks_dic,
    #           "feedbacks_dic":feedbacks_dic, "mistakes_feedback":mistakes_feedback}

    return student_name, one_row_result

#global variables
# Constant variable
SUCCESS = "success"

root, submissions_dir= checkStructure()
configurations=getYAMLConfig()
all_submissions = os.scandir(submissions_dir)

def run():
    all_results = {}
    # all_students_marks_dic={}
    # all_students_feedback_dic={}
    # all_students_mistakes_dic={}
    # For each student aka submission, do
    for student_dir in all_submissions:
        # submissions folder may contain non folders (e.g. submissions.rar that contain all submissions will be skipped)
        if student_dir.is_dir():
            student_name, one_row_result = mark_submission(student_dir)
            all_results[student_name] = one_row_result
            # extract all results for each student
            # student_name = student_result_dic["student_name"]
            # marks = student_result_dic["marks_dic"]
            # feedbacks = student_result_dic["feedbacks_dic"]
            # mistakes = student_result_dic["mistakes_feedback"]
            #
            # all_students_marks_dic[student_name] = marks
            # all_students_feedback_dic[student_name] = feedbacks
            # all_students_mistakes_dic[student_name] = str(mistakes)
    root_folder_name = root.split("\\")[-1]
    df = pd.DataFrame(data=all_results).T
    df.to_excel(root_folder_name + '_Marks.xlsx')

    input(("="*70)+"\nFinished Marking All Students, Press Enter to exit")
if __name__ == '__main__':
    run()


