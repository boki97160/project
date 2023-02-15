import tkinter, tkinter.filedialog

root = tkinter.Tk()
root.withdraw()
file_path = tkinter.filedialog.askopenfilename(parent=root, title='選擇檔案', filetypes=(("application/pdf","*.pdf"),("all files","*.*")))
print(file_path)