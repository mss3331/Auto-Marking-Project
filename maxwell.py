#this code taken from https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout

from os import kill, path
from subprocess import PIPE, Popen

def run(args, cwd = None, shell = False, kill_tree = True, timeout = -1, env = None):
    '''
    Run a command with a timeout after which it will be forcibly
    killed.
    '''

    def alarm_handler(signum, frame):
        raise Exception
    p = Popen(args, shell = shell, cwd = cwd, stdout = PIPE, stderr = PIPE, env = env)
    if timeout != -1:
        signal(SIGALRM, alarm_handler)
        alarm(timeout)
    try:
        stdout, stderr = p.communicate()
        if timeout != -1:
            alarm(0)
    except Exception as e:
        pids = [p.pid]
        if kill_tree:
            pids.extend(get_process_children(p.pid))
        for pid in pids:
            # process might have died before getting to this line
            # so wrap to avoid OSError: no such process
            try:
                kill(pid, SIGKILL)
            except OSError:
                pass
        return -9, '', ''
    return p.returncode, stdout, stderr

def get_process_children(pid):
    p = Popen('ps --no-headers -o pid --ppid %d' % pid, shell = True,
              stdout = PIPE, stderr = PIPE)
    stdout, stderr = p.communicate()
    return [int(p) for p in stdout.split()]

if __name__ == '__main__':
    folder_url = r'.\networking\Arjun Khetan_5176644_assignsubmission_file_'
    file_name = 'server2.c'
    file = path.join(folder_url, file_name)
    destination = path.join(folder_url, 'ser2')

    print (run(destination, shell = True, timeout = 3))
    print (run('find', shell = True))