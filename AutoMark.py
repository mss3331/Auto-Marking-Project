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
        print(DirEntry_list[max_index].name)
        return DirEntry_list[max_index]
    else:# if nothing is found
        return None
def mark():
    address = r"C:\Users\Mahmood_Haithami\Documents\Computer Fundametals Demos\AutoMarking Project\Submissions\Zeyad Hesham Mohamed Abdelalim Emara_3745894_assignsubmission_file_\2_HACK\CPU.tst"
    command=subprocess.run(["HardwareSimulator",address],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)

    cmd_output = command.stdout
    if(cmd_output.find("Comparison ended success")>=0):
        print("good")
        print(cmd_output)
        if not command.stderr:print("no errors, empty error")
    else:
        print("Faild")
        print(command.stderr)

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

def _getStudentSubmission(student_dir):
    '''This function process the student_dir to extract a student's name and the actha, Exercise's folder
    :parameter
    -DirEntry object: It has the directory info of the current submission
    :return
    student_name: processed student name (e.g.Abbygail Yuen Mun Ong_3745904_assignsubmission_file_ --> Abbygail Yuen Mun Ong )
    exercise_dir: DirEntry that points to the actual location of the students work (i.e. dir that has 1_Assembly & 2_HACK) '''
    student_name = student_dir.name.split("_")[0]

    ########################### Cases #############################
    ''' 1- Exercise contains only one task, one of the follows are expected:
            1- All .hdl codes would be in the student folder
            2- All .hdl codes would be in the student sub_folder
        2- Exercise contains several tasks, one of the follows are expected:
            1- All tasks' folder would be in the student folder
            2- All tasks' folder would be in the student sub_folder '''

    exercise_dir = os.scandir(student_dir)
    print(student_name," has sub-folders: ",list(exercise_dir))
    exit(0)
    return student_name, exercise_dir
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
    student_name, exercise_dir = _getStudentSubmission(student_dir)
    return 0
if __name__=='__main__':
    root, submissions_dir= checkStructure()
    configurations=getYAMLConfig()
    all_submissions = os.scandir(submissions_dir)

    #For each student\submission do
    for student_dir in all_submissions:
        if student_dir.is_dir():
            result = mark_submission(student_dir)



