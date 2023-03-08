import webbrowser
import shlex
from subprocess import Popen, PIPE

def execute_and_return(cmd):

    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err

if __name__ == "__main__":
    out, err = execute_and_return("python test.py")
    error_message = err.decode("utf-8").strip().split("\r\n")[-1]
    print(error_message)
er= error_message.split(":")[1]


stackoverflow_url = f"https://stackoverflow.com/search?q={er}"


webbrowser.open_new_tab(stackoverflow_url)
