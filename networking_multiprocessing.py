import multiprocessing
import time
import os
import signal
import subprocess

# Your foo function
def foo(n,output_dic):
    folder_url = r"'.\networking\Arjun Khetan_5176644_assignsubmission_file_\ser2'"
    file_name = 'server2.c'
    file = os.path.join(folder_url, file_name)
    destination = os.path.join(folder_url, 'ser2')
    print('thread is working')
    try:
        server = os.system("ser2 8989 >myfile.txt")
        output_dic['output'] = server
        print('what the hell!')
        print(folder_url)
    except Exception as e:
        print(folder_url)
        print(e)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    popen.wait(2)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


if __name__ == '__main__':
    folder_url = r".\networking\Arjun Khetan_5176644_assignsubmission_file_"
    file_name = 'server2.c'
    file = os.path.join(folder_url, file_name)
    destination = os.path.join(folder_url, 'ser2')
    # Example
    for path in execute([destination, '8989']):
        print(path, end="")
    # output = {}
    # # Start foo as a process
    # p = multiprocessing.Process(target=foo, name="Foo", args=(10,output))
    # try:
    #     p.start()
    #     time.sleep(3)
    #     p.terminate()
    #     p.join()
    #
    # except Exception as e:
    #     print('exception from a thread')

    # Wait 10 seconds for foo
    # time.sleep(3)

    #
    # # Cleanup
    # p.join()
    # Terminate foo
    # p.terminate()
    # print(output)
    # print('finish')

