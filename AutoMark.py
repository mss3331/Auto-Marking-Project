import subprocess
import yaml
import os


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
    with open("Marking_Configuration.yml", "r") as ymlfile:
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
    yaml_conf= "Marking_Configuration.yml"
    submissions_dir = ""

    isFile = os.path.isfile(yaml_conf)
    if not isFile :
        printError("I didn't find the configuration file '%s' in the current directory\n %s" % (yaml_conf,root))

    # get list of all directories
    dir_list = os.listdir()

    # convert it to lowercase to search for submissions folder
    dir_list_lowercase =[name.lower() for name in dir_list]

    if "submissions" in dir_list_lowercase:
        index = dir_list_lowercase.index("submissions")
        submissions_dir = root+"/"+dir_list[index]
    else:
        printError("submissions folder is not found in the current directory!!\n %s "%root)

    return root,submissions_dir


def printError(message):
    print("Error:\n"+message)
    input("Press Enter to Exit...")
    exit(-1)

if __name__=='__main__':
    checkStructure()
    configurations=getYAMLConfig()

    #Print the main sections
    for section in configurations:
        print(section)
