import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
import pickle as pkl
import pandas as pd
from tkinter import filedialog
from tkinter import Scrollbar
import numpy as np
import imblearn
import sklearn
import lightgbm
from datetime import datetime

# with open("LGBM.pkl", "rb") as f:
#     clf = pkl.load(f)

def validate_input(x):
    if len(x) == 0:
        msg = "Cannot be empty"
    else:
        try:
            x = float(x)
            return True
        except Exception as ep:
            messagebox.showerror('error','Can only be integer/float')
            return False
    messagebox.showinfo('message', msg)

def callback():
    X = [input["%s" %features[0]].get()]
    for i in range(39):
        X += [input["%s" %features[i+1]].get()]
    X = pd.DataFrame([X], columns=["Second_mean","Second_max","Second_min","Second_std","Accuracy_mean","Accuracy_max","Accuracy_min","Accuracy_std","Bearing_mean","Bearing_max","Bearing_min","Bearing_std","Acceleration_x_mean",
"Acceleration_x_max","Acceleration_x_min","Acceleration_x_std","Acceleration_y_mean","Acceleration_y_max","Acceleration_y_min","Acceleration_y_std","Acceleration_z_mean","Acceleration_z_max","Acceleration_z_min","Acceleration_z_std","Gyro_x_mean","Gyro_x_max","Gyro_x_min","Gyro_x_std",
"Gyro_y_mean","Gyro_y_max","Gyro_y_min","Gyro_y_std","Gyro_z_mean","Gyro_z_max","Gyro_z_min","Gyro_z_std","Speed_mean","Speed_max","Speed_min","Speed_std"])
    y_pred = clf.predict(X)
    if y_pred[0] == 0:
        y_pred = 'Safe'
    else:
        y_pred = 'Dangerous'
    result['text'] = y_pred
    if result['text'] == 'Dangerous':
        result.config(fg="#FF0000")
    else:
        result.config(fg="#32CD32")
    prob = np.max(clf.predict_proba(X), axis=1)
    probability['text'] = "{:.2%}".format(prob[0])

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    if filename.endswith('.csv'):
        test = pd.read_csv(filename)
        test = test.set_index("BookingID")
        y_pred = clf.predict(test)
        scroll = Scrollbar(table_frame)
        scroll.pack(side='right', fill='y')
        table = ttk.Treeview(table_frame, yscrollcommand=scroll.set)
        table.pack()
        scroll.config(command=table.yview)
        table['columns'] = ('BookingID', 'Label')
        # format our column
        table.column("#0", width=0,  stretch='no')
        table.column("BookingID",anchor='center', width=120)
        table.column("Label",anchor='center',width=120)

        #Create Headings 
        table.heading("#0",text="",anchor='center')
        table.heading("BookingID",text="BookingID",anchor='center')
        table.heading("Label",text="Driving Behaviour",anchor='center')

        #Insert data
        bid = []
        pred_labels = []
        for i in range(len(test.index.values)):
            label = y_pred[i]
            if label == 0:
                label = 'Safe'
            else:
                label = 'Dangerous'
            table.insert(parent='',index='end',iid=i,text='',values=(test.index.values[i], label))
            bid.append(test.index.values[i])
            pred_labels.append(label)
        data_dict = {'BookingID':bid, 'Label':pred_labels}
        global df
        df = pd.DataFrame(data_dict, columns=['BookingID','Label'])
        dl_btn = tk.Button(master=dl_frame, text='Export result', command=Download)
        dl_btn.pack()
    else:
        messagebox.showinfo('message', 'The file must be in .csv format!')

def Download():
    if isinstance(df, pd.DataFrame):
        print(df)
        now = datetime.now()
        a = now.strftime("%d-%m-%Y %H%M")
        df.to_csv(f'PredictionResult_{a}.csv', index = False)
    else:
         messagebox.showinfo('message', 'No result to be exported!')

def Clear():
    result['text'] = ''
    probability['text'] = ''
    for widget in table_frame.winfo_children():
        widget.destroy()
    for widget in dl_frame.winfo_children():
        widget.destroy()

window = tk.Tk()
window.title('Driving Behavior Prediction')
for i in range(6):
    window.columnconfigure(i, weight=1, minsize=50)
for i in range(13):
    window.rowconfigure(i, weight=1, minsize=30)

frame = tk.Frame(master=window)
frame.grid(row=0, column=0, columnspan=5)
title = tk.Label(master=frame, text="Driving Behaviour Prediction", font=tkFont.Font(family="Lucida Grande", size=20))
title.pack()

features = ["Second_mean","Second_max","Second_min","Second_std","Accuracy_mean","Accuracy_max","Accuracy_min","Accuracy_std","Bearing_mean","Bearing_max","Bearing_min","Bearing_std","Accuracy_x_mean",
"Accuracy_x_max","Accuracy_x_min","Accuracy_x_std","Accuracy_y_mean","Accuracy_y_max","Accuracy_y_min","Accuracy_y_std","Accuracy_z_mean","Accuracy_z_max","Accuracy_z_min","Accuracy_z_std","Gyro_x_mean","Gyro_x_max","Gyro_x_min","Gyro_x_std",
"Gyro_y_mean","Gyro_y_max","Gyro_y_min","Gyro_y_std","Gyro_z_mean","Gyro_z_max","Gyro_z_min","Gyro_z_std","Speed_mean","Speed_max","Speed_min","Speed_std"]

input = {}
for i in range(10):
    for j in range(4):
        frame = tk.Frame(master=window)
        frame.grid(row=i+1, column=j)
        input_label = tk.Label(master=frame, text=features[(i*4)+j])
        input["%s" %features[(i*4)+j]] = tk.Entry(master=frame, validate="key")
        input["%s" %features[(i*4)+j]]['validatecommand'] = (input["%s" %features[(i*4)+j]].register(validate_input), '%P')

        input_label.pack()
        input["%s" %features[(i*4)+j]].pack()

frame = tk.Frame(master=window)
frame.grid(row=12, column=2, columnspan=2)
submit = tk.Button(master=frame, text='Submit', command=callback)
submit.pack()

frame = tk.Frame(master=window)
frame.grid(row=12, column=0, columnspan=2)
t = tk.Label(master=frame, text='Upload a csv')
t.pack()
upload = tk.Button(master=frame, text='Upload', command=UploadAction)
upload.pack()

frame = tk.Frame(master=window)
frame.grid(row=0, column=4, columnspan=2)
dashboard = tk.Label(frame, text='Dashboard')
dashboard.pack()

frame = tk.Frame(master=window)
frame.grid(row=1, column=4, columnspan=2, rowspan=2)
prediction = tk.Label(frame, text=f'Prediction : ')
result = tk.Label(frame)
proba = tk.Label(frame, text=f'Probability : ')
probability = tk.Label(frame)
prediction.pack()
result.pack()
proba.pack()
probability.pack()

table_frame = tk.Frame(master=window)
table_frame.grid(row=4, column=4, columnspan=2, rowspan=5)

df = None
dl_frame = tk.Frame(master=window)
dl_frame.grid(row=9, column=4, columnspan=2)

frame = tk.Frame(master=window)
frame.grid(row=12, column=4, columnspan=2, rowspan=2)
clear_btn = tk.Button(master=frame, text='Clear', command=Clear)
clear_btn.pack()


result.config(font=("Courier", 28))
probability.config(font=("Courier", 20))
window.mainloop()
