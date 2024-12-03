import os, shutil
t_file_path = "P:pax_temp.txt"
tr_file_path = "P:pax_temp_raw.txt"
tp_file_path = "P:temperature.py"

git_dir = "C:/Users/T/Documents/Work/WWW/TT/Paxman/Paxman_Demo/Raspberry_Pi_Network_Files/"

t_git_path = git_dir + "pax_temp.txt"
tr_git_path = git_dir + "pax_temp_raw.txt"
tp_git_path = git_dir + "temperature.py"

def run():
    if os.path.exists(t_git_path):
        os.remove(t_git_path)
    shutil.copy2(t_file_path, t_git_path)
    
    if os.path.exists(tr_git_path):
        os.remove(tr_git_path)
    shutil.copy2(tr_file_path, tr_git_path)
    
    if os.path.exists(tp_git_path):
        os.remove(tp_git_path)
    shutil.copy2(tp_file_path, tp_git_path)
    
run()