import subprocess



def mark():
    address = r"C:\Users\Mahmood_Haithami\Documents\Computer Fundametals Demos\AutoMarking Project\Submissions\Zeyad Hesham Mohamed Abdelalim Emara_3745894_assignsubmission_file_\2_HACK\CPU.tst"
    command=subprocess.run(["HardwareSimulator",address],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)

    cmd_output = command.stdout
    if(cmd_output.find("Comparison ended success")>=0):
        print("good")
        print(cmd_output)
        print(command.stderr)
    else:
        print("Faild")
        print(command.stderr)


if __name__=='__main__':
    mark()