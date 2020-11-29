import subprocess
import yaml
import os
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
    file_path: sting that contains the file full path (e.g. ./submissions/student1/exer3/1_assembly/Factorial.tst)
    emulator_name: string that contains either HardwareSimulator or CPUEmulator'''

    command=subprocess.run([emulator_name,file_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)

    cmd_output = command.stdout
    if(cmd_output.find("Comparison ended success")>=0):
        return True, cmd_output
    else:
        return False,command.stderr

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
    print("Error:\n"+message)
    input("Press Enter to Exit...")
    exit(-1)

# def _getStudentActualSubmission(student_dir):
#     '''This function process the student_dir to extract a student's name and the actha, Exercise's folder
#     :parameter
#     - student_dir: A DirEntry object that has the directory info of the current submission
#     :return
#     - exercise_dir: DirEntry that points to the actual location of the students work (i.e. dir that has 1_Assembly & 2_HACK) '''
#
#     exercise_dir = _searchForDirOrFile()
#     return exercise_dir
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
    - total_marks: dictionary that contains the name of the file with its corresponding deserved mark
    - total_feedbacks: dictionary that contains all the feedback for each .tst file.
    '''
    student_name = student_dir.name.split("_")[0] # Zaid Ahmad_3522_submision --> Zaid Ahmad
    total_marks={} #dictionary that holds all the marks for each .tst file (e.g. "CPU.tst":10, "hack.tst":50 ...etc)
    total_feedbacks={} #dictionary that holds all the feedbacks for each .tst file (e.g. "CPU.tst":10, "hack.tst":50 ...etc)


    #for each section in the exercise get the .tst files and test them
    for section in configurations:
        folder_name = configurations[section]["Folder_Name"]
        emulator_name = configurations[section]["Emulator_Name"]
        student_tst_list = configurations[section]["Test_Files"]
        num_of_tst_files = len(student_tst_list)

        for tst_mark in student_tst_list:# run the emulator for each .tst file and get the result
            tst, mark = tst_mark.split(" ") # Mult.tst 20 --> tst="Mult" and mark="20"
            mark = int(mark) # mark = "20" --> 20

            tst_file = _searchForDirOrFile(tst,student_dir)
            file_name = tst_file.name
            if tst_file:
                success, feedback = markFile(tst_file,emulator_name)
                total_marks[file_name] = 0
                total_feedbacks[file_name]= feedback
                if success:
                    total_marks[file_name] = mark
            else:
                total_marks[file_name] = 0
                total_feedbacks[file_name] = "Error: %s not found!!"%tst_file.name
    print("%s:%d"%(student_name,sum(total_marks.values())))
    print(total_marks)

    return total_marks,total_feedbacks
if __name__=='__main__':
    root, submissions_dir= checkStructure()
    configurations=getYAMLConfig()
    all_submissions = os.scandir(submissions_dir)

    #For each student\submission do
    for student_dir in all_submissions:
        if student_dir.is_dir():
            result = mark_submission(student_dir)



