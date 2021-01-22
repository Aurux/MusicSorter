
import os
import shutil
import audio_metadata
import PySimpleGUI as sg



def Main(dir_path):

    wavCount = 0
    otherCount = 0
    count320 = 0

    wavPath = dir_path + "/lossless"

    try:
        os.mkdir(wavPath)
    except OSError:
        print ("Creation of the directory %s failed" % wavPath)
    else:
        print ("Successfully created the directory %s " % wavPath)

    path320 = dir_path + "/320mp3"

    try:
        os.mkdir(path320)
    except OSError:
        print ("Creation of the directory %s failed" % path320)
    else:
        print ("Successfully created the directory %s " % path320)

    otherPath = dir_path + "/Other"

    try:
        os.mkdir(otherPath)
    except OSError:
        print ("Creation of the directory %s failed" % otherPath)
    else:
        print ("Successfully created the directory %s " % otherPath)
    print(dir_path)
    # Searches, logs and moves files.

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            try:
                metadata = audio_metadata.load(root+'/'+str(file))
            except:
                pass
            if file.endswith('.mp3') and metadata.streaminfo.bitrate >= 320000:
                #fileName = file
                #print(fileName)
                #print (root+'/'+str(file))
                count320 += 1
                try:
                    shutil.move(root+'/'+str(file), path320)
                except:
                    pass
            if file.endswith('.wav') or file.endswith('.flac'):
                #print (root+'/'+str(file))
                wavCount += 1
                try:
                    shutil.move(root+'/'+str(file), wavPath)
                except:
                    pass
            else:
                if file.endswith('.py') == False:
                    otherCount += 1
                    try:
                        shutil.move(root+'/'+str(file), otherPath)
                    except:
                        pass
        if len(files) == 0:
            count320 = int(count320/2)
            otherCount = int(otherCount/2)
            nonWav = count320 + otherCount
            print("Lossless files found: {wav} \nMP3 files found: {mp3}\nOf which MP3 files {count320} are over 320kpbs".format(wav=wavCount, mp3=nonWav, count320=count320))
            break

    return(wavCount, nonWav, count320)

sg.theme('DarkTeal6')



layout = [[sg.T("")], [sg.Text("Choose a folder to sort: "), sg.Input(key="-IN2-" ,change_submits=True), sg.FolderBrowse(key="-IN-")],[sg.Button("Sort", bind_return_key=True)],[sg.Output(key='-OUT-', size=(80, 40))]]

window = sg.Window('Aurux Music Sorter', layout, size=(600,200)).Finalize()
window.Element('-OUT-')._TKOut.output.bind("<Key>", lambda e: "break")
while True:
    (event, values) = window.read()
    
    print("Selected folder:",values["-IN2-"])
    if event is None:
        break
    elif event == "Sort":
        global dir_path
        dir_path = str(values["-IN2-"])
        Main(dir_path)
    
    

window.close()