import os, shutil, glob

historyfile = './HistoryRecord/woodlandwalkpattern'
'''target = r'*.json'
copy_filename = glob.glob(target)
for file in copy_filename:
    shutil.copy(file,historyfile)'''
print(historyfile.isspace())
historyfile = ''
print(historyfile.isspace())
print(len(historyfile))