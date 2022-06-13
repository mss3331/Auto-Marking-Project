import os
import signal
import subprocess
import time
import sys

if __name__=='__main__':
    ################## information about subprocess argument ######################
    #The underlying object is Popen.
    #The input argument is passed to Popen.communicate() and thus to the subprocess’s stdin.
    ##############################################################################
    folder_url = r'.\networking\Arjun Khetan_5176644_assignsubmission_file_'
    file_name = 'server2.c'
    file = os.path.join(folder_url, file_name)
    destination = os.path.join(folder_url,'ser2')
    timeout_s=1
    # compile = subprocess.run(['gcc', file, '-o',destination,'-lws2_32'], capture_output=True, text=True,
    #                          shell=True)
    # print(compile.stdout, compile.stderr)
    # try:
    #     run = subprocess.run([destination], capture_output=True, text=True,timeout=0.01,
    #                          shell=True)
    # except subprocess.TimeoutExpired:
    #     print(subprocess.stdout, subprocess.stderr)
    # result = []
    # try:
    #     p = subprocess.Popen([destination,'9999'], start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     result = p.communicate(timeout=timeout_s)
    #     # p.wait(timeout=timeout_s)
    # except subprocess.TimeoutExpired:
    #
    #     # print(f'Timeout for {destination} ({timeout_s}s) expired', file=sys.stderr)
    #     # print('Terminating the whole process group...', file=sys.stderr)
    #     #os.killpg(os.getpgid(p.pid), signal.SIGTERM) #this is for linux
    #     os.kill(p.pid, signal.CTRL_C_EVENT) #this is for windows
    #
    #     # result.append(p.stdout)
    #
    # print(result)

    # outs = ''
    # errs = ''
    # ins = ''
    # f = open("demofile.txt", "w")
    # proc = subprocess.Popen([destination,'9999'], stdout=subprocess.PIPE,stderr=subprocess.PIPE )
    # try:
    #     outs,errs = proc.communicate(timeout=1)
    # except subprocess.TimeoutExpired:
    #     print(outs, errs)
    #     print(proc.stdout)
    #     proc.kill()
    #     outs, errs = proc.communicate()
    #     # print(proc.stdout)
    #
    #     print(outs, errs)
    #     os.kill(proc.pid, signal.CTRL_C_EVENT)
    #     # proc.kill()
    #
    #     # print(outs)
    #     # print(errs)
    #
    # print('finished')
    # sys.stdout = open('file.txt', 'w')
    # sys.stderr = open('file2.txt', 'w')
    try:
        server = subprocess.Popen([destination, '8989'],text=True, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                  # , close_fds=False,
                                  # start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # print('im in try')
        # outs, errs = server.communicate(timeout=timeout_s)
        # server.wait(timeout=timeout_s)
        output = server.communicate(timeout=timeout_s)
        exitCode = server.returncode
        print('what the hell!')
    except subprocess.TimeoutExpired:
        print('im in excpetion')
        print(server.stdout.readline())
        # outs, errs = server.communicate()
        # server.kill()
        # server.stdout.close()
        # outs, errs = server.communicate()
        # print(outs,errs)
        # print(f'Timeout for {destination} ({timeout_s}s) expired', file=sys.stderr)
        # print('Terminating the whole process group...', file=sys.stderr)
        # os.killpg(os.getpgid(p.pid), signal.SIGTERM) #this is for linux
        os.kill(server.pid, signal.CTRL_C_EVENT) #this is for windows

        # print(server.stdout)

        # result.append(p.stdout)
    # print(output)
    print('finished finally')



