import os
import matplotlib 
import tkinter as tk        
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

from tkinter import ttk
from PIL import Image
from pathlib import Path
from tkinter.filedialog import askopenfilename
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg
        )

matplotlib.use('TkAgg')

import core.tools.Constant as cs
import app.tools.WindowsTools as wt   

class WindowsMain():
  
    def __init__(self,  common_root_ini_path: str): 
        
        self.common_root_ini_path = common_root_ini_path
        self.file_path :str = ""
        self.model_selected :str = ""
        self.filename :str = ""
        
    def get_windows(self):
        
        windows_width :int = 1200 
        windows_height :int = 510
        
        root = wt.WindowsTools.create_window_base(cs.ASCDEV_SYSTEM_COPYRIGHT + "  " + 
                                                  cs.WIN_TENSORFLOW_TITLE_WINDOWS , 
                                                  windows_width, windows_height)
        
        cs.INIT_ICON_NAME
        root.iconbitmap(os.path.join(self.common_root_ini_path, cs.INIT_ICON_PATH, 
                                                                cs.INIT_ICON_NAME))
        
        model_lm_file_name :list = []
        model_lm_label :dict = {}
        model_directory:str = Path(os.path.join(self.common_root_ini_path, 
                                                cs.INIT_DIRECTORY_TENSORFLOW_MODEL))
        model_file_name :list = [f.name for f in model_directory.iterdir() if f.is_file()]
        for i in range(len(model_file_name)):
            
            if str(model_file_name[i])[-2:] == "h5":
                model_lm_file_name.append(model_file_name[i])
                
            if str(model_file_name[i])[-5:] == "label":
                label_file_name :str = os.path.join(self.common_root_ini_path, 
                                                cs.INIT_DIRECTORY_TENSORFLOW_MODEL
                                                ,str(model_file_name[i]))
                
                label_name :str = str(model_file_name[i])[:int(len(str(model_file_name[i]))-5)] + "h5"
                label_list :list = []
                
                with open(label_file_name, 'r', encoding='utf-8') as f:
                    for ligne in f:
                        label_list.append(str(ligne.strip()))
                        
                model_lm_label[label_name] = label_list

        def event_close_main_windows():
            root.quit()
        
        root.protocol("WM_DELETE_WINDOW", event_close_main_windows)
        
        def event_select_image_path():
            
            if len(self.filename) == 0:
                self.filename = askopenfilename(initialdir="\\",                                                             
                                                filetypes=[("IMAGE","*.jpg"),
                                                           ("IMAGE","*.jpeg"),
                                                           ("IMAGE","*.png")], 
                                                title="Select DPRM_Web.py full path name ...")
            
            if len(self.filename) > 0:
                label_display_image_path.config(text=self.filename)   
                
                fig = Figure(figsize=(5, 4))
                ax = fig.add_subplot(111)
                
                img = mpimg.imread(self.filename)  
                ax.imshow(img)  
                ax.axis('off')  
                
                canvas = FigureCanvasTkAgg(fig, master=root)  
                canvas.draw()
                canvas.get_tk_widget().place(x=0, y=50, height=390, width=550)
                
                self.file_path = self.filename
                self.filename = ""
                
                event_execute_image_prediction()
                
        wt.WindowsTools.create_button_detailed(root, 'Image Selection', event_select_image_path, 
                                               10, 10, 120, 25)                              
        
        label_display_image_path = wt.WindowsTools.create_label_base(root, 
                                                                      "", 
                                                                      'gray58', 138, 10, 1050, 25)
        def event_execute_image_prediction():
            
            if self.file_path != None:
                
                image = Image.open(self.file_path)
            
                resized_image = image.resize((32, 32))
                image_arr = np.array(resized_image) / 255
                image_arr = image_arr.reshape(1, 32, 32, 3)
                
                model = tf.keras.models.load_model(os.path.join(self.common_root_ini_path, 
                                                                cs.INIT_DIRECTORY_TENSORFLOW_MODEL, 
                                                                selected_backup_cycle.get()))                
                
                prediction = model.predict(image_arr)
                
                cifar10_classes = model_lm_label[selected_backup_cycle.get()]
                prediction_text = cifar10_classes[np.argmax(prediction)]
                
                prediction_list :list = list(prediction)
                val_max :float = np.max(prediction_list[0])
                
                fig, ax = plt.subplots()
                y_pos = np.arange(len(cifar10_classes))
                
                ax.barh(y_pos, prediction[0], align="center")
                ax.set_yticks(y_pos)
                ax.set_yticklabels(cifar10_classes)
                ax.invert_yaxis()
                ax.set_xlabel("Probability")
                ax.set_title("Cifar 10 Prediction")
                
                canvas = FigureCanvasTkAgg(fig, master=root)  
                canvas.draw()
                
                canvas.get_tk_widget().place(x=500, y=50, height=390, width=750)
                
                label_display_prediction.config(text=" PREDICTION: " + str(prediction_text).upper() + 
                                                     " For: " + str(round(val_max*100, 2)) + "%")   
                
            else:
                label_display_prediction.config(text=" PREDICTION: Error [no image]")   
        
        label_display_prediction = wt.WindowsTools.create_label_base(root, 
                                                                    " PREDICTION: ...", 
                                                                    'gray58', 20, 
                                                                    windows_height - 35, 
                                                                    250, 25)        
        
        wt.WindowsTools.create_label_base(root, " IA MODEL SELECTION:", 
                                                'gray58', 277, windows_height - 35, 130, 25)        
        
        selected_backup_cycle = tk.StringVar(root)
        backup_cycle_selection = ttk.Combobox(root, textvariable=selected_backup_cycle)

        backup_cycle_selection['values'] = tuple(model_lm_file_name)
        backup_cycle_selection['state'] = 'readonly'
        backup_cycle_selection.place(x=410, y=windows_height - 35, height=25, width=138)
        
        def backup_cycle_changed(event):
            self.model_selected = selected_backup_cycle.get()

        backup_cycle_selection.bind('<<ComboboxSelected>>', backup_cycle_changed)
        if len(model_lm_file_name) > 0:
            selected_backup_cycle.set(model_lm_file_name[0])          
            
        def event_reload_image_prediction():
            
            if self.file_path != None:
                if len(self.file_path) > 0:
                    event_execute_image_prediction()
                                  
        wt.WindowsTools.create_button_detailed(root, 'MAKE PREDICTION', event_reload_image_prediction, 
                                               555, windows_height - 35, 150, 25)      
          
        
        # def event_execute_create_new_model_ia():
            
        #     # ... In Corse ...
        #     pass
        
        # wt.WindowsTools.create_button_detailed(root, 'CREATE NEW MODEL IA', 
        #                                        event_execute_create_new_model_ia, 
        #                                        windows_width - 170, 
        #                                        windows_height - 35, 150, 25)                              
        
        self.filename = os.path.join(self.common_root_ini_path, cs.INIT_IMAGE_TENSORFLOW_PATH, 
                                                                cs.INIT_IMAGE_TENSORFLOW_NAME)
        event_select_image_path()
        
        root.mainloop()    