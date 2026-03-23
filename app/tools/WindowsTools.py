import tkinter as tk
from tkinter import ttk

import core.tools.Constant as cs
import app.tools.WindowsTools as wt   

INPUT_BASE_LABEL :int = 0
INPUT_BASE_CONTROL :int = 1
INPUT_BASE_VALUE :int = 2


class WindowsTools():
    
    def __init__(self):        
        pass
    
    def create_window_base(windows_title :str, windows_width :int, windows_height :int) -> tk.Tk:
        
        root = tk.Tk()
        
        root.title(windows_title)        
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x = (screen_width - windows_width) // 2
        y = int(((screen_height - windows_height) // 2) * 0.65)
        
        root.geometry(f"{windows_width}x{windows_height}+{x}+{y}") 

        root.resizable(False, False)
        root.attributes('-topmost', 1)
        root.configure(background=cs.GUI_COLOR_BASE_SCREEN_BACK_COLOR)
        
        return root
    
    def center_window(window :tk.Tk):
        
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = int(((screen_height - height) // 2) * 0.65)
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_button_base(root :tk.Tk, text_value :str, command_function :any, left :int, top :int) -> ttk.Button:
        
        new_button = ttk.Button(root,
                                text=text_value,
                                command=command_function)
        
        new_button.place(x=left, y=top)
        
        return new_button
    
    def create_button_detailed(root :tk.Tk, text_value :str, command_function :any, left :int, top :int, width_value :int, height_value :int) -> ttk.Button:
        
        new_button = ttk.Button(root,
                                text=text_value,
                                command=command_function)
        
        new_button.place(x=left, y=top, width=width_value, height=height_value)
        
        return new_button
    
    def create_frame_base(root :tk.Tk, back_color :str, left :int, top :int, width_value :int, height_value :int) -> tk.Frame:
        
        new_frame = tk.Frame(root, bg=back_color, width=width_value, height=height_value, bd=3, relief=tk.RIDGE)
        new_frame.place(x=left, y=top)
        
        return new_frame
    
    def create_label_base(root :tk.Tk, text_value :str, back_color :str, left :int, top :int, width_value :int, height_value :int) -> ttk.Label:
        
        new_label = ttk.Label(root, text=text_value, background=back_color)
        new_label.place(x=left,y=top, width=width_value, height=height_value)                
        
        return new_label
    
    def create_input_with_label_base(root :tk.Tk, text_value_label :str, text_value_record :str, back_color :str, left :int, top :int) -> list:
        '''
        Create a new base object list input text data 

                list definition:
                
                [INPUT_BASE_LABEL]      = [0] = Label definition display
                [INPUT_BASE_CONTROL]    = [1] = Control input data text 
                [INPUT_BASE_VALUE]      = [2] = Default data value to display to input text
        '''
        new_input_object_list :list[any] = []
        
        entry_text = tk.StringVar()
        entry_text.set(text_value_record)
        
        
        new_input_object_list.append(wt.WindowsTools.create_label_base(root, text_value_label, back_color, left, top, 200, 20))    
        
        new_input_text_value = tk.Entry(root, textvariable=entry_text)
        new_input_text_value.place(x=left+200+10, y=top, width=200, height=20)
        
        
        new_input_object_list.append(new_input_text_value)
        new_input_object_list.append(entry_text)
        
        return new_input_object_list
    
    def create_input_with_label_complex(root :tk.Tk, text_value_label :str, dict_value :dict, dict_key :str, back_color :str, left :int, top :int) -> dict:
        '''
        Create a new complex object list input text data 

                Dict definition:
                
                ["label"]   = Label definition display
                ["control"] = Control input data text 
                ["value"]   = Default data value to display to input text
                ["key_id"]  = Control key id
                ["default"] = Default value text 
                                
        '''
        new_input_object_dict :dict[any] = {}
        
        entry_text = tk.StringVar()
        entry_text.set(str(dict_value[dict_key]))
        
        new_input_object_dict["key_id"] = dict_key
        new_input_object_dict["label"] = wt.WindowsTools.create_label_base(root, text_value_label, back_color, left, top, 200, 20)
        
        new_input_text_value = tk.Entry(root, textvariable=entry_text)
        new_input_text_value.place(x=left+200+10, y=top, width=220, height=20)
        
        new_input_object_dict["control"] = new_input_text_value
        new_input_object_dict["value"] = entry_text
        new_input_object_dict["default"] = dict_value[dict_key]
        
        return new_input_object_dict
    
    
    def list_view_remove_all_row(tree :ttk.Treeview):
        
        for Parent in tree.get_children():                
            tree.delete(Parent)
    
