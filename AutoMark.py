import subprocess
import yaml
import os
import pandas as pd
import shutil
import traceback
from pprint import pprint
from datetime import datetime
from difflib import SequenceMatcher
#Check submission CSF-Ex1-20213725 and CSF-Ex1-20307078 there is a mismatch ()


def getDirOrFile(dir_name, DirEntry_iterator, threshold=0.8):
    """This function compute the similarity index between a directory name and a list of DirEntry
    (i.e. contains path, and name of the directory)
    :parameter
    dir_name: the name of the desired directory (e.g. 1_Assembly)
    DirEntry: ScandirIterator of directories and files found in specific folder
    threshold: similarity ratio threshold
    :return
    target_dir=DirEntry object: if the dir_name match one of the directory's name in the list. And None otherwise.
    """
    DirEntry_list = list(DirEntry_iterator)
    similarity_list = [(SequenceMatcher(None, dir_name, dir_entry.name).ratio()) for dir_entry in DirEntry_list]
    if len(similarity_list)==0:
        return None

    max_index = similarity_list.index(max(similarity_list))

    # print("threshold is ", threshold)
    # print(similarity_list)
    # print(DirEntry_list)
    # exit(0)
    if (similarity_list[max_index]>=threshold):
        return DirEntry_list[max_index]
    else:# if nothing is found
        return None
def markFile(file_path, emulator_name):
    """This function execute the command HardwareSimulation file.tst
    :parameter
    - file_path: sting that contains the file full path (e.g. ./submissions/student1/exer3/1_assembly/Factorial.tst)
    - emulator_name: string that contains either HardwareSimulator or CPUEmulator
    :returns
    - is_successful : True if success or False otherwise
    - feedback : contains error messages if found or constant string SUCCESS otherwise
    """

    command = subprocess.run([emulator_name,file_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)

    cmd_output = command.stdout
    feedback = command.stderr
    is_successful = False
    if(cmd_output.find("Comparison ended success")>=0):
        is_successful = True
        feedback = SUCCESS


    return is_successful, feedback.rstrip('\n') # "End of ... succussfuly\n" --> "End of ... succussfuly"

def getYAMLConfig():
    """This function return a dictionary that contains all configurations for the exersise"""
    expected_config_file_name = "Exer_conf.yml"
    file=getDirOrFile(expected_config_file_name, os.scandir())
    if not file:
        printError("I didn't find the configuration file '%s' in the current directory\n %s" % (expected_config_file_name, root))
    with open(file.name, "r") as ymlfile:
        configurations = yaml.load(ymlfile, Loader=yaml.FullLoader)

    return configurations

def checkStructure():
    """This function checks for the following:
        - YAML configuration exists
        - Submissions folder exists
        :return
        root : Current directory path
        submissions : The directory path that has all students' submissions
        """
    root = os.path.dirname(os.path.realpath(__file__))

    # get list of all directories
    dir_list = os.scandir()

    submissions_dir = getDirOrFile("submissions",dir_list, threshold=0.5)

    if not submissions_dir:# if submissions_dir is None
        printError("submissions folder is not found in the current directory!!\n %s "%root)


    return root,submissions_dir

def printError(message,extraInfo=None):
    print("Error:\n"+message,flush=True)
    pprint(extraInfo)
    input("Press Enter to Exit...")
    exit(-1)

def _searchForDirOrFile(name,current_dir, threshold=0.8):
    """This is a recursive function that search for a specific directory in a breadth first fashion
    (i.e. search first for the name in the current_dir then go deeper)
    :parameter
    name: the target file\folder name
    current_dir: is a DirEntry object. The searching will start by this directory
    :return
    target_dir: is a DirEntry object that contains the dir. If not found None is returned
    """
    # if for some reason we revieved none path, return none. Otherwise os.scan(None) will
    #scan the ".\" ultimately will mark other submissions.
    if current_dir==None:
        return None
    # target should either be the actual path of the target or the current path.
    target_dir=None
    dir_iterator= os.scandir(current_dir)
    found = getDirOrFile(name,dir_iterator, threshold= threshold)

    if found:#if we found the name in the current_dir return
        target_dir = found
        return target_dir

    #if we didn't find the name in the current_dir search deeper
    dir_iterator= os.scandir(current_dir)
    for dir_temp in dir_iterator:
        if dir_temp.is_dir():
            found=_searchForDirOrFile(name, dir_temp, threshold= threshold)
            if found:  # if we found the name in the current_dir return
                target_dir = found
                return target_dir

    return target_dir

def _checkRequiredFiles(required_files_list, target_folder_name,url_of_our_tst,student_dir):
    """
    This function do two things:
     1- check the existence of required_files_list and add a penalty if a file is missing.

    :param required_files_list: list of all required files
    :param target_folder_name: which folder to 1- search for the required files, 2- to copy our .tst files
    :param url_of_our_tst: where to fetch our .tst files into the student's submission folder
    :param student_dir: the current working directory
    :return: total_penalties: summation of all penalties
    :return: all_feedbacks: string that contains all feedbacks for the penalties
    """
    #case one, we have multiple sections for the excersise, hence, we should have a target_folder_name
    total_penalties = 0
    all_feedbacks = target_folder_name+":"
    target_dir = _searchForDirOrFile(name=target_folder_name, current_dir=student_dir)
    if target_dir:# if found a directory with same name then check the required files
        for file_name_penalty in required_files_list:
            if not file_name_penalty: # if there is no required files, continue. In ".yaml" it would be like "Check_Files: - "
                continue
            temp = file_name_penalty.strip().split(' ')# CPU diagram.pdf -5 --> temp=['CPU','diagram.pdf', '-5']
            penalty = float(temp[-1])
            file_name = ' '.join(temp[:-1])
            found = _searchForDirOrFile(file_name, target_dir)
            if not found:
                total_penalties+=penalty
                all_feedbacks +=file_name_penalty + ", "
                # Creates a new file to prevent the simulator to invoke the build-in .hdl file incase this file is a prerequist within other chip
                if file_name.split('.')[-1] == 'hdl':
                    with open(target_dir.path+"\\"+file_name, 'w') as fp: # create file C:\....\student1\section1\CPU.tst
                        pass

    else:# if we didn't find the specified folder then search for the required file in sub-directories
        # print("we passed because we didn't find target_dir")
        # exit(0) #I think I should copy our .tst files here. check if there is a folder name for the task. If not become strict and give zero or I can do that by file bases
        pass
    # case two, we have only one section for the excersise, hence, we may not have a target_folder_name (i.e. target_folder_name='')
    if total_penalties == 0:
        all_feedbacks=""
    return total_penalties, all_feedbacks

def mark_submission(student_dir, use_our_tst=False):
    """This method is responsible for doing the marking for each section in the exercise for one student.
    It uses the global variable "configurations" defined in the __main__ to get essential information
    :parameter
    - student_dir:A DirEntry object that has the directory info of the current submission
    :returns
    - student_result dictionary that contains:
        - marks_dic: dictionary that contains the name of the file with its corresponding deserved mark
        - feedbacks_dic: dictionary that contains all the feedback for each .tst file.
        - mistakes_feedback_list: list of tuple (file_name, error_message) that contains only mistakes.
        This list is subset of feedbacks_dic
    """
    student_name = student_dir.name.split("_")[0] # Zaid Ahmad_3522_submision --> Zaid Ahmad
    marks_dic={} #dictionary that holds all the marks for each .tst file (e.g. "CPU.tst":10, "hack.tst":50 ...etc)
    feedbacks_dic={} #dictionary that holds all the feedbacks for each .tst file (e.g. "CPU.tst":10, "hack.tst":50 ...etc)
    penalties_dic = {} # dictionary that holds all the penalties
    #for each section in the exercise do the following
    for section in configurations:
        """ 
        Before we start makring student's solution, two things should done:
         1- Check that all required files exist, if not, add a penalty and insert an empty file to prevent
            invoking build-in files
         2- Load our .tst files to the specified folder
        Step 1 and 2 are done in method "checkRequiredFiles"
        """
        required_files_list = configurations[section]["Check_Files"]
        target_folder_name = configurations[section]["Folder_Name"]
        url_of_our_tst = configurations[section]["URL_of_tst"]
        penalties_dic[section], penalty_feedback = _checkRequiredFiles(required_files_list,target_folder_name,
                                                                       url_of_our_tst,student_dir)
        if penalties_dic[section] != 0:
            if feedbacks_dic.get("Penalties:"):
                feedbacks_dic["Penalties:"] += penalty_feedback # concatinate the penalties of all sections
            else:
                feedbacks_dic["Penalties:"] = penalty_feedback
        """actual marking start down below:"""
        emulator_name = configurations[section]["Emulator_Name"]
        student_tst_list = configurations[section]["Test_Files"]

        for tst_mark_yml in student_tst_list:# run the emulator for each .tst file and get the result
            file_name, mark = tst_mark_yml.split(" ") # Mult.tst 20 --> tst="Mult" and mark="20"
            mark = int(mark) # mark = "20" --> 20

            if target_folder_name: #if there is exist folder name, search for it
                target_folder_path = _searchForDirOrFile(target_folder_name,student_dir) # search for specific path
            else: target_folder_path = student_dir # otherwise use the student submission folder


            tst_file = _searchForDirOrFile(file_name,target_folder_path,threshold=1)

            if tst_file:#if the file name is found within the path
                #here we either copy our .tst or use the student's .tst
                if use_our_tst:
                    #students MyNot.tst path. #tst_file.path is actually path+name
                    tst_path = tst_file.path.split(tst_file.name)[0]
                    #copy .tst and .cmp from source to students folder
                    try:
                        shutil.copy2(os.path.join(url_of_our_tst, file_name), tst_path)
                        compare_name = file_name.split('.')[0] + ".cmp"  # Mult.tst -> Mult -> Mult.cmp
                        shutil.copy2(os.path.join(url_of_our_tst, compare_name), tst_path)
                    except Exception as e:
                        if url_of_our_tst=="":
                            printError("Where are our tst files resides?.Please add a path to the URL_of_tst's variable in "
                                       "the Excer.yaml file to copy our tst files from that path")
                        else:
                            print("Couldn't copy a file from our tst folder")
                            traceback.print_exc()



                is_success, feedback = markFile(tst_file.path,emulator_name)

                marks_dic[file_name] = 0
                feedbacks_dic[file_name]= feedback
                if is_success:
                    marks_dic[file_name] = mark
            else: # if we didnt find the tst_file print error
                marks_dic[file_name] = 0
                #if we didn't find the folder then regardless of the .tst file the error should be
                #folder not found
                if target_folder_path == None:
                    feedbacks_dic[file_name] = "Error: %s not found!!" % target_folder_name
                else:
                    feedbacks_dic[file_name] = "Error: %s not found!!"% file_name


    mistakes_feedback = [(key, feedbacks_dic[key]) for key in feedbacks_dic if feedbacks_dic[key] != SUCCESS ]
    # if not mistakes_feedback: # if the mistake feedback is empty list make it ""
    #     mistakes_feedback = "No Mistakes"

    total_marks = sum(marks_dic.values())
    total_penalties = sum(penalties_dic.values())
    print( "{}:{}%. {}".format(student_name, total_marks+total_penalties, mistakes_feedback), flush=True )

    one_row_result = marks_dic
    one_row_result["Total"] = total_marks + total_penalties
    one_row_result["Feedback"] = str(mistakes_feedback)

    # student_result = {"student_name":student_name, "marks_dic":marks_dic,
    #           "feedbacks_dic":feedbacks_dic, "mistakes_feedback":mistakes_feedback}

    return student_name, one_row_result


def save_to_excel(all_results, extra='' ):
    df = pd.DataFrame(data=all_results).T
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")



    df.to_excel(root_folder_name + '_Marks_' + extra + dt_string + '.xlsx')


def run(use_our_tst):
    ''' The mode variable should have the value "" or "strict"
    if "strict" ->
        1- The folder and file names should match 100%
        2- Copy our .tst files to the students folder first
    '''
    all_results = {}

    # For each student aka submission, do
    for student_dir in all_submissions:
        # submissions folder may contain non folders (e.g. submissions.rar that contain all submissions will be skipped)
        if student_dir.is_dir():
            student_name, one_row_result = mark_submission(student_dir, use_our_tst)
            all_results[student_name] = one_row_result
        
    


    #save results in excel file
    if use_our_tst:
        ourTst = "ourTst_"
    else:
        ourTst = "studentTst_"
    save_to_excel(all_results, extra=ourTst)

    return all_results


def unzipSubmissions(all_submissions):
    unzip_errors = []
    for student_dir in all_submissions:
        # submissions folder may contain non folders (e.g. submissions.rar that contain all submissions will be skipped)
        if student_dir.is_dir():
            zip_file = getDirOrFile('.zip',os.scandir(student_dir),threshold=0)
            if not zip_file:
                continue
            if zip_file.name.find('.zip')>=0: #if file name is .zip that mean it is a zip file
                # print(zip_file)
                try:
                    shutil.unpack_archive(zip_file,zip_file.path.split(zip_file.name)[0])
                    os.remove(zip_file)
                except Exception as e:
                    unzip_errors.append([zip_file.path,e])
    if len(unzip_errors)>0:
        printError("Please go to the listed submissions down below and unzip them by yourself"+
                   ", I couldn't unzip them due to an error. After you solve the problems delete '.zip' files\n\n"+
                   "You can delete what inside the submission folder to get rid of this error,"
                   "though, the corresponding student will get Zero.\n"+
                   'To help you figuring out the problems, '+
                   'check the following submission with corresponding error message:\n',unzip_errors)








if __name__ == '__main__':

    try:
        # global variables & Constant variable
        SUCCESS = "success"
        root, submissions_dir = checkStructure()
        root_folder_name = root.split("\\")[-1]

        configurations = getYAMLConfig()


        all_submissions = list(os.scandir(submissions_dir))
        #unzip submissions
        unzipSubmissions(all_submissions)

        results_student_tst = run(use_our_tst= False)

        print("\n------------- Now we will marking using our .tst files -------------")
        try:
            shutil.copytree(submissions_dir.path,submissions_dir.path+"_withOurTstScript")
        except:
            print("Notification:\n",submissions_dir.path+"_withOurTstScript"+" folder was created from a previous run."
                                                                             "Hence, we will delete it and copy again\n")
            try:
                shutil.rmtree(submissions_dir.path + "_withOurTstScript")
                shutil.copytree(submissions_dir.path, submissions_dir.path + "_withOurTstScript")
            except:
                traceback.print_exc()
                printError("")

        all_submissions = list(os.scandir(submissions_dir.path+"_withOurTstScript"))
        results_our_tst = run(use_our_tst=True)

        #create average marking
        average_mark = {}
        for student_name in results_student_tst.keys():
            student_tst_mark = results_student_tst[student_name]['Total']
            our_tst_mark = results_our_tst[student_name]['Total']
            avg = (student_tst_mark + our_tst_mark)/2
            diff = student_tst_mark - our_tst_mark
            average_mark[student_name] = {"Student .tst":student_tst_mark,
                                          "Our .tst":our_tst_mark,
                                          "difference":diff,
                                          "Average":avg}

        save_to_excel(average_mark, extra="average_")
        input(("=" * 70) + "\nFinished Marking All Students, Press Enter to exit")
            # run("strict")
    except Exception as e:
        traceback.print_exc()

        printError("")




