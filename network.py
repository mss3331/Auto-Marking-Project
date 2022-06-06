import subprocess


if __name__=='__main__':
    file_url = r'.\networking\Abdelrahman Ashraf Abdelmoghni Elsayed Lasheen_5176672_assignsubmission_file_\server2.c'
    compile = subprocess.run(['gcc', file_url, '-o','ser','-lws2_32'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                             shell=True)
    print(compile)