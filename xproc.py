import re
import subprocess

def checkProcessRunning(process):
    cmd = 'pidof %s' %(process)
    try:
        result = subprocess.check_output(cmd, shell=True).decode('utf8')
        return result
    except:
        return None

def checkOutput(cmd, patten=None):
    output = subprocess.check_output(cmd, shell=True).decode('utf8')
    if patten:
        m = re.search(patten, output)
        if m:
            return m.group(1)
        else:
            return None
    return output
