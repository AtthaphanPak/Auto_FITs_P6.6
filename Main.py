import os
import glob
import time
import shutil
import auto_FITs
import pandas as pd
import configparser
import tkinter as tk
from UI import GUI
from tkinter import messagebox

def AllFilePath(Source_path):
    allpath = []
    for patten in ["*_AB", "*_BB"]:
        for paths in glob.glob(os.path.join(Source_path, patten)):
            allpath.append(paths)

    if not allpath:
        # print("Empty")
        return 

    return allpath

def movefolder(serial, f, fullpath, des_path):
    newsnfolder = os.path.join(des_path, serial)
    new_filename = os.path.join(newsnfolder, os.path.basename(fullpath))
    if os.path.exists(newsnfolder) is False:
        os.makedirs(newsnfolder)
    if os.path.exists(new_filename):
        shutil.rmtree(new_filename)
    shutil.move(fullpath, new_filename)
    if len(os.listdir(f)) == 0:
        try:
            os.rmdir(f)
            return True
        except Exception as error:
            print(f"{error}:\n{f}")
            return False
    
if __name__ == "__main__":
    ##### INITIAL SETUP #####
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    config = configparser.ConfigParser()
    main_files = "C:\Projects\Auto_FITs_P6.6"
    try:
        config.read(os.path.join(main_files, "Properties\config.ini"))
        Source_path = config["DEFAULT"]["file_path"]
        Backup_path = config["DEFAULT"]["Backup_path"]
        model = config["DEFAULT"]["path_extend"]
        Query_parameters = config["DEFAULT"]["FITs"]
        
        model = config["FITS"]["model"]
        operation = config["FITS"]["operation"].split(";")
    except Exception as error:
        print("Please check config.ini")
        print(error)
        quit()
    sharedrive = r'\\fab2-fs13.luminartech.com\Departments\advmfg\P6-6'

    Blackup_BB = os.path.join(Backup_path,"Beforer_Bake")
    if os.path.exists(Blackup_BB) is False:
        os.makedirs(Blackup_BB) 
    arh_path_BB = os.path.join(Blackup_BB,"Arh")
    if os.path.exists(arh_path_BB) is False:
        os.makedirs(arh_path_BB)
    Handcheck_path_BB = os.path.join(Blackup_BB,"FAIL_Handcheck")
    if os.path.exists(Handcheck_path_BB) is False:
        os.makedirs(Handcheck_path_BB)
    Log_path_BB = os.path.join(Blackup_BB,"FAIL_Log")
    if os.path.exists(Log_path_BB) is False:
        os.makedirs(Log_path_BB)

    Blackup_AB = os.path.join(Backup_path,"After_Bake")
    if os.path.exists(Blackup_AB) is False:
        os.makedirs(Blackup_AB)
    arh_path_AB = os.path.join(Blackup_AB,"Arh")
    if os.path.exists(arh_path_AB) is False:
        os.makedirs(arh_path_AB)
    Handcheck_path_AB = os.path.join(Blackup_AB,"FAIL_Handcheck")
    if os.path.exists(Handcheck_path_AB) is False:
        os.makedirs(Handcheck_path_AB)
    Log_path_AB = os.path.join(Blackup_AB,"FAIL_Log")
    if os.path.exists(Log_path_AB) is False:
        os.makedirs(Log_path_AB)
        
    Backup_DEBUG = os.path.join(Backup_path,"DEBUG")
    if os.path.exists(Backup_DEBUG) is False:
        os.makedirs(Backup_DEBUG)
    
    ##### MAIN #####
    while True:
        allpath = AllFilePath(Source_path)
        if allpath:
            for f in allpath:
                list_of_files = glob.glob(os.path.join(f, "**\TestReport*.csv"))
                if list_of_files: 
                    latest_file = max(list_of_files, key=os.path.getctime)
                    fullpath = os.path.dirname(latest_file)
                    check_file_path = os.path.join(fullpath, "events.csv")
                    if os.path.exists(check_file_path):
                        with open(check_file_path, 'r') as file:
                            content = file.read()

                        if 'Auto Mode Disabled' in content:
                            listresult = glob.glob(os.path.join(fullpath, "TestReport*.csv"))
                            if not listresult:
                                continue
                            
                            df = pd.read_csv(listresult[0]).astype(str)

                            serial = df["Serial number"].squeeze().split("_")[0]
                            operation  = df["Serial number"].squeeze().split("_")[1]
                            if operation.upper() == "AB":
                                operation = "LT420"
                            elif operation.upper() == "BB":
                                operation = "LT400"
                            else:
                                operation = "DEBUG"
                                newsnfolder = os.path.join(Backup_DEBUG, serial)
                                if os.path.exists(newsnfolder) is False:
                                    os.makedirs(newsnfolder)
                                shutil.move(fullpath, os.path.join(newsnfolder, os.path.basename(fullpath)))
                                if len(os.listdir(f)) == 0:
                                    try:
                                        os.rmdir(f)
                                    except Exception as error:
                                        print(f"{error}:\n{f}")
                                continue
                                ##################################################### 
                            print("----------------------------------------------------------------------")
                            print("File:\t",latest_file)
                            FITsCheck = auto_FITs.Handshake(model, operation, serial)
                            if FITsCheck == True:
                                status = GUI(df)
                                df["Serial number"] = serial
                                df["MC"] = os.environ['COMPUTERNAME']
                                df = df.rename(columns={"Serial number": "SN  XCVR", "Machine": "Machine No.", "Optocast 3410 Lot no": "Optocast 3410  Lot no.",
                                                        "Site A X": "APD A Boresight X", "Site A Y": "APD A Boresight Y","Divergence A": "APD A Divergence (mRad)",
                                                        "Site B X": "APD B Boresight X", "Site B Y": "APD B Boresight Y","Divergence B": "APD B Divergence (mRad)",
                                                        " FPC temp": "Slim FPC TMP102 (Degree Celsius)", "Divergence Result": "Divergence Alignment",
                                                        " Boresight Result": "Boresight Alignment"
                                                        })
                                if status == True:
                                    df["WO#"] = auto_FITs.Query(model, "LT050", serial, "WO#")
                                    qvalues = auto_FITs.Query(model, "LT330", serial, "SN RCVR;S/N Laser EDFA").split(";")
                                    df["SN RCVR"] = qvalues[0]
                                    df["S/N Laser EDFA"] = qvalues[1]
                                    df["Result"] = "PASS"
                                    
                                    parameters = auto_FITs.Convert_Data(df.columns)
                                    values = auto_FITs.Convert_Data(df.to_numpy().tolist()[0])
                                    
                                    FITsLog = auto_FITs.Log(model, operation, parameters, values)
                                    if FITsLog == True:
                                        if operation == "LT400":
                                            movefolder(serial, f, fullpath, arh_path_BB)
                                        elif operation == "LT420":
                                            movefolder(serial, f, fullpath, arh_path_AB)
                                        print(f"operation: {operation} Serial: {serial} Sucessce Record to FITs")
                                        messagebox.showinfo("FITs MESSAGEs", f"operation: {operation} Serial: {serial} Sucessce Record to FITs")
                                    else:
                                        if operation == "LT400":
                                            movefolder(serial, f, fullpath, Log_path_BB)
                                        elif operation == "LT420":
                                            movefolder(serial, f, fullpath, Log_path_AB)
                                        print(f"operation: {operation} Serial: {serial} FAIL Record to FITs")
                                        messagebox.showwarning("FITs MESSAGEs", f"{FITsLog}")
                                    
                                else:
                                    movefolder(serial, f, fullpath, Backup_DEBUG)
                                    print(f"operation: {operation} Serial: {serial} Skip record by manual")
                                    messagebox.showwarning("FITs MESSAGEs", f"operation: {operation} Serial: {serial} Skip record by manual")                              
                                    
                            else:
                                if operation == "LT400":
                                    movefolder(serial, f, fullpath, Handcheck_path_BB)
                                elif operation == "LT420":
                                    movefolder(serial, f, fullpath, Handcheck_path_AB)
                                print(f"HandCheck Fail {FITsCheck}")
                                messagebox.showwarning("FITs MESSAGEs", f"{FITsCheck}")
                            print("----------------------------------------------------------------------")
        
        time.sleep(10)
        print("Sleep 10 sec")