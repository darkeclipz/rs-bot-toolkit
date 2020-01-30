import subprocess

def get_window_size():
    sp = subprocess.run(['window_size/window_size.exe'], stdout=subprocess.PIPE)
    result = str(sp.stdout)
    if(sp.returncode != 0):
        raise Exception(result)
    width, height, left, top, right, bottom = map(float, result[2:len(result)-5].split(','))
    return width, height, left, top, right, bottom
