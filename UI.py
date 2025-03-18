import tkinter as tk
from tkinter import messagebox, font

def GUI(dataframe):
    # print(dataframe)
    SN = str(dataframe["Serial number"][0])
    Boresight_X_A = str(dataframe["Site A X"][0])
    Boresight_Y_A = str(dataframe["Site A Y"][0])
    Boresight_X_B = str(dataframe["Site B X"][0])
    Boresight_Y_B = str(dataframe["Site B Y"][0])
    Divergence_A = str(dataframe["Divergence A"][0])
    Divergence_B = str(dataframe["Divergence B"][0])
    Temp_sensor = str(dataframe[" Temp sensor"][0])
    
    Spec_Boresight_X = "+/- 140"
    Spec_Boresight_Y = "+/- 325"
    Spec_Divergence = "0.9 - 1.1"

    if -140 <= float(Boresight_X_A) <= 140:
        C_Boresight_X_A = "white"
    else:
        C_Boresight_X_A = "FAIL"
    if -140 <= float(Boresight_X_B) <= 140:
        C_Boresight_X_B = "white"
    else:
        C_Boresight_X_B = "red"
    if -325 <= float(Boresight_Y_A) <= 325:
        C_Boresight_Y_A = "white"
    else:
        C_Boresight_Y_A = "red"
    if -325 <= float(Boresight_Y_B) <= 325:  
        C_Boresight_Y_B = "white"
    else:
        C_Boresight_Y_B = "red"
    if 0.9 <= float(Divergence_A) <= 1.1:
        C_Divergence_A = "white"
    else:
        C_Divergence_A = "red"
    if 0.9 <= float(Divergence_B) <= 1.1:
        C_Divergence_B = "white"
    else:
        C_Divergence_B = "red"

    if C_Boresight_X_A == "white" and C_Boresight_X_B == "white" and C_Boresight_Y_A == "white" and C_Boresight_Y_B == "white" and C_Divergence_A == "white" and C_Divergence_B == "white":
        C_Status_Result = "green"
        Status_Result = "PASS"
    else:
        C_Status_Result = "red"
        Status_Result = "FAIL"

    # Initialize the root Tkinter window
    root = tk.Tk()
    root.title("Data Collection Verify")
    root.attributes("-topmost", True)
    result = tk.BooleanVar(value=False)

    def center_window(win):
        win.update_idletasks()  # Ensure all dimensions are calculated
        width = win.winfo_width()
        height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def close_window():
        root.quit()
        root.destroy()
    
    def ok():
        if Status_Result == "FAIL":
            comfirm_fail = messagebox.askyesno("Comfirm FAIL", "คุณแน่ใจหรือไม่ว่าต้องการส่งข้อมูล FAIL ขึ้น FIT?")
            if comfirm_fail == True:
                result.set(True)
                close_window()   
        else:
            result.set(True)
            close_window()  
            
    def cancel():
        result.set(False)
        close_window()

    def on_close():
        comfirm = messagebox.askyesno("Comfirm Exit", "คุณแน่ใจหรือไม่ว่าต้องการปิดโปรแกรม?")
        if comfirm:
            result.set(False)
            close_window()
            print("Comfirm Exit Program")
        else:
            return
        
    big_font = font.Font(family="Helverica", size=24, weight="bold")
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Define the data for the table
    tk.Label(root,text=f'Serial', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=0, column=0, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{SN}', bg = "white", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=0, column=1, sticky='NSEW', columnspan=3)
    tk.Label(root,text=f'Temp sensor', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=1, column=0, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Temp_sensor}', bg = "white", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=1, column=1, sticky='NSEW', columnspan=3)
    tk.Label(root,text=f'', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=2, column=0, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'Site A', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=2, column=1, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'Site B', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=2, column=2, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'Limit spec', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=2, column=3, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'Boresight X', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=3, column=0, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Boresight_X_A}', bg = C_Boresight_X_A, border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=3, column=1, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Boresight_X_B}', bg = C_Boresight_X_B, border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=3, column=2, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Spec_Boresight_X}', bg = "white", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=3, column=3, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'Boresight Y', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=4, column=0, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Boresight_Y_A}', bg = C_Boresight_Y_A, border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=4, column=1, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Boresight_Y_B}', bg = C_Boresight_Y_B, border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=4, column=2, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Spec_Boresight_Y}', bg = "white", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=4, column=3, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'Divergence (mRad)', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=5, column=0, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Divergence_A}', bg = C_Divergence_A, border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=5, column=1, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Divergence_B}', bg = C_Divergence_B, border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=5, column=2, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'{Spec_Divergence}', bg = "white", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=5, column=3, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f'Status', bg = "gray", border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=6, column=0, sticky='NSEW', columnspan=1)
    tk.Label(root,text=f"{Status_Result}", bg = C_Status_Result, border=1, relief="solid", font=big_font, padx=5, pady=5).grid(row=6, column=1, sticky='NSEW', columnspan=3)
    tk.Button(root,text="OK", bg = "#00D25F", border=1, relief="raised", font=big_font, padx=5, pady=5, command=ok).grid(row=8, column=2, sticky='NSEW', columnspan=1)
    tk.Button(root,text="Cancel", bg = "#FF5B5B", border=1, relief="raised", font=big_font, padx=5, pady=5, command=cancel).grid(row=8, column=3, sticky='NSEW', columnspan=1)

    center_window(root)
    root.mainloop()

    return result.get()