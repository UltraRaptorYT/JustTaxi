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
from tkinter.messagebox import showinfo

with open("tuned_dc.pkl", "rb") as f:
    clf = pkl.load(f)


def validate_data_input(x):
    if len(x) == 0:
        msg = "Cannot be empty"
    else:
        try:
            x = float(x)
            return True
        except Exception as ep:
            messagebox.showerror('error', 'Can only be integer/float')
            return False
    messagebox.showinfo('message', msg)


def callback():
    X = [data_input["%s" % features[0]].get()]
    for i in range(len(features) - 1):
        X += [data_input["%s" % features[i+1]].get()]
    X = pd.DataFrame([X], columns=features)
    y_pred = clf.predict(X)
    if y_pred[0] == 0:
        y_pred = 'Safe'
    else:
        y_pred = 'Not safe'
    result['text'] = y_pred
    if result['text'] == 'Not safe':
        result.config(fg="#FF0000")
    else:
        result.config(fg="#32CD32")
    prob = np.max(clf.predict_proba(X), axis=1)
    probability['text'] = "{:.2%}".format(prob[0])

table = None
data = None

def item_selected(event):
    global table
    global data
    for selected_item in table.selection():
        item = table.item(selected_item)
        record = item['values']
        print(data_input)
        for key, entry in data_input:
            print(data.iloc[record[0]][key])
            print(entry)
        # show a message
        showinfo(title='Information', message=','.join(map(str, record)))

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    if filename.endswith('.csv'):
        global data
        data = pd.read_csv(filename)
        data = data.set_index("bookingID")








        
        # need to check man
        y_pred = clf.predict(data)
        scroll = Scrollbar(table_frame)
        scroll.pack(side='right', fill='y')        
        global table
        table = ttk.Treeview(table_frame, yscrollcommand=scroll.set)
        table.bind('<<TreeviewSelect>>', item_selected)
        table.pack()
        scroll.config(command=table.yview)
        table['columns'] = ('bookingID', 'Label')
        # format our column
        table.column("#0", width=0,  stretch='no')
        table.column("bookingID", anchor='center', width=50)
        table.column("Label", anchor='center', width=50)

        # Create Headings
        table.heading("#0", text="", anchor='center')
        table.heading("bookingID", text="bookingID", anchor='center')
        table.heading("Label", text="Driving Behaviour", anchor='center')

        # Insert data
        bid = []
        pred_labels = []
        for i in range(len(data.index.values)):
            label = y_pred[i]
            if label == 0:
                label = 'Safe'
            else:
                label = 'Not safe'
            table.insert(parent='', index='end', iid=i, text='',
                         values=(data.index.values[i], label))
            bid.append(data.index.values[i])
            pred_labels.append(label)
        data_dict = {'bookingID': bid, 'Label': pred_labels}
        global df
        df = pd.DataFrame(data_dict, columns=['bookingID', 'Label'])
        dl_btn = tk.Button(
            master=export_frame, text='Export result', command=Download)
        dl_btn.pack()
    else:
        messagebox.showinfo('message', 'The file must be in .csv format!')


def Download():
    if isinstance(df, pd.DataFrame):
        print(df)
        now = datetime.now()
        a = now.strftime("%d-%m-%Y %H%M")
        df.to_csv(f'PredictionResult_{a}.csv', index=False)
    else:
        messagebox.showinfo('message', 'No result to be exported!')


def Clear():
    result['text'] = ''
    probability['text'] = ''
    for widget in table_frame.winfo_children():
        widget.destroy()
    for widget in export_frame.winfo_children():
        widget.destroy()


# Setup window
window = tk.Tk()
window.title('JustTaxi Drivers Safety Prediction')
window.geometry("960x768+{}+{}".format(
    int((window.winfo_screenwidth() - 960) / 2),
    int((window.winfo_screenheight() - 768) / 2)
))
window.resizable(False, False)

# Setup window grid
for i in range(12):
    window.columnconfigure(i, weight=1, minsize=50)
window.rowconfigure(0, weight=1, minsize=10)
for i in range(1,19):
    window.rowconfigure(i, weight=1, minsize=45)

frame = tk.Frame(master=window)
frame.grid(row=1, column=0, columnspan=12)
title = tk.Label(master=frame, text="JustTaxi Drivers Safety Prediction",
                 font=tkFont.Font(family="Lucida Grande", size=20))
title.pack()

features = ['accuracy_mean', 'accuracy_max', 'accuracy_min', 'accuracy_std',
            'accuracy_25%', 'accuracy_75%', 'bearing_mean', 'bearing_max',
            'bearing_min', 'bearing_std', 'bearing_25%', 'bearing_75%',
            'acceleration_x_mean', 'acceleration_x_max', 'acceleration_x_min',
            'acceleration_x_std', 'acceleration_x_25%', 'acceleration_x_75%',
            'acceleration_y_mean', 'acceleration_y_max', 'acceleration_y_min',
            'acceleration_y_std', 'acceleration_y_25%', 'acceleration_y_75%',
            'acceleration_z_mean', 'acceleration_z_max', 'acceleration_z_min',
            'acceleration_z_std', 'acceleration_z_25%', 'acceleration_z_75%',
            'gyro_x_mean', 'gyro_x_max', 'gyro_x_min', 'gyro_x_std', 'gyro_x_25%',
            'gyro_x_75%', 'gyro_y_mean', 'gyro_y_max', 'gyro_y_min', 'gyro_y_std',
            'gyro_y_25%', 'gyro_y_75%', 'gyro_z_mean', 'gyro_z_max', 'gyro_z_min',
            'gyro_z_std', 'gyro_z_25%', 'gyro_z_75%', 'second_mean', 'second_max',
            'second_min', 'second_std', 'second_25%', 'second_75%',
            'speed (km/h)_mean', 'speed (km/h)_max', 'speed (km/h)_min',
            'speed (km/h)_std', 'speed (km/h)_25%', 'speed (km/h)_75%', 'yaw_mean',
            'yaw_max', 'yaw_min', 'yaw_std', 'yaw_25%', 'yaw_75%', 'pitch_mean',
            'pitch_max', 'pitch_min', 'pitch_std', 'pitch_25%', 'pitch_75%',
            'roll_mean', 'roll_max', 'roll_min', 'roll_std', 'roll_25%', 'roll_75%',
            'turning_force_mean', 'turning_force_max', 'turning_force_min',
            'turning_force_std', 'turning_force_25%', 'turning_force_75%',
            'acceleration_mean', 'acceleration_max', 'acceleration_min',
            'acceleration_std', 'acceleration_25%', 'acceleration_75%']

# Map all the inputs values together
data_input = {}
for i in range(15):
    for j in range(6):
        frame = tk.Frame(master=window, height=25)
        frame.grid(row=i+2, column=j+1, padx=10, pady=2.5)
        data_input_label = tk.Label(master=frame, text=features[(i*6)+j], width=200)
        data_input["%s" %
                   features[(i*6)+j]] = tk.Entry(master=frame, validate="key", width=200)
        data_input["%s" % features[(i*6)+j]]['validatecommand'] = (data_input["%s" %
                                                                    features[(i*6)+j]].register(validate_data_input), '%P')

        data_input_label.pack()
        data_input["%s" % features[(i*6)+j]].pack()

# Submit btn
frame = tk.Frame(master=window)
frame.grid(row=9, column=8, columnspan=2)
submitBtn = tk.Button(master=frame, text='Submit', command=callback)
submitBtn.pack()

# Upload btn
frame = tk.Frame(master=window)
frame.grid(row=7, column=8, columnspan=2)
t = tk.Label(master=frame, text='Upload a csv')
t.pack()
uploadBtn = tk.Button(master=frame, text='Upload', command=UploadAction)
uploadBtn.pack()

# Probability and Prediction
frame = tk.Frame(master=window)
frame.grid(row=2, column=8, columnspan=2, rowspan=3)
prediction = tk.Label(frame, text=f'Prediction : ')
result = tk.Label(frame)
proba = tk.Label(frame, text=f'Probability : ')
probability = tk.Label(frame)
prediction.pack()
result.pack()
proba.pack()
probability.pack()
result.config(font=("Courier", 28))
probability.config(font=("Courier", 20))

# Table
table_frame = tk.Frame(master=window)
table_frame.grid(row=9, column=7, columnspan=5, rowspan=10)

# Export btn
df = None
export_frame = tk.Frame(master=window)
export_frame.grid(row=9, column=8, columnspan=2)

# Clear btn
frame = tk.Frame(master=window)
frame.grid(row=8, column=8, columnspan=2, rowspan=2)
clear_btn = tk.Button(master=frame, text='Clear', command=Clear)
clear_btn.pack()

window.mainloop()
