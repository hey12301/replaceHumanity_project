import pyautogui as p
import sys
from time import sleep as t
import cv2
import re
import numpy as np
from PIL import Image
import pytesseract
import random
import soundfile as sf
import sounddevice as sd
from misaki import en, espeak
from kokoro_onnx import Kokoro
from playsound import playsound


p.PAUSE = 0.01


def ocrImageDetectionUI(x1, y1, x2 , y2, variableText, variableText1):
    # print("please wait extracting text")
    global text
    global OCR_value
    global text_array
    global all_num_value
    all_num_value = False
    text_array = []
    global all_num
    OCR_value = False
    all_num = ""
    global xAxis, yAxis
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    screenshot = p.screenshot()
    screenshot.save(main_path + r"\screenshot.png")
    bigImage = (main_path + r"\screenshot.png")
    
    img = cv2.imread(bigImage)    #(r'C:\Users\aman\Desktop\ocrCode\screenshot.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    global image
    image = Image.open(bigImage) 

    image_arr = np.array(image) 
    image_arr = image_arr[y1:y2, x1:x2]
    image = Image.fromarray(image_arr)
    image.save(main_path + r"\small_screenshot.png")
    smallImg = image.save(main_path + r"\small_screenshot.png")
    OCR_value = False

    smallImg = cv2.imread(r"C:\Users\aman\Desktop\small_screenshot.png")
    img = cv2.cvtColor(smallImg, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(img, -1, sharpen_kernel)
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
#def OCRFunction(image):
    boxes = pytesseract.image_to_data(thresh, lang='eng', config='--psm 6')
    ##print(boxes)
    a = 0
    for x, b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                a = a + 1
                text = str(b[11])
                text_array.append(text)
                y = re.findall(r"\d", text)
                all_num = "".join(y)
                # OCR_value = False
                # print(text)
                if(variableText in text or variableText1 in text):
                    xAxis = int(b[6]) + x1
                    yAxis = int(b[7]) + y1
                    OCR_value = True
                    # print(xAxis, ',' , yAxis)
                    return False
##                print(text)
                # OCR_value = False
                if(all_num != ""):
                    xAxis = int(b[6]) + x1
                    yAxis = int(b[7]) + y1
                    all_num_value = True
                    # print(all_num)
                    # print(xAxis, ',' , yAxis)
                    return False
            a = a + 1
    return OCR_value
    return xAxis
    return yAxis
    return text
    return all_num
    return all_num_value

        
def ocrImageDetection(x1, y1, x2 , y2, variableText, variableText1):
    # print("please wait extracting text")
    global text
    global text_array
    text_array = []
    global OCR_value
    OCR_value = False
    global xAxis, yAxis
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\aman\Desktop\ocrCode\Tesseract-OCR\tesseract.exe'

    screenshot = p.screenshot()
    screenshot.save(main_path + r"\screenshot.png")
    bigImage = (main_path + r"\screenshot.png")
    
    img = cv2.imread(bigImage)    #(r'C:\Users\aman\Desktop\ocrCode\screenshot.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    global image
    image = Image.open(bigImage) 

    image_arr = np.array(image) 
    image_arr = image_arr[y1:y2, x1:x2]
    image = Image.fromarray(image_arr)
    OCR_value = False
#def OCRFunction(image):
    boxes = pytesseract.image_to_data(image, lang='eng', config='--psm 7')
    ##print(boxes)
    a = 0
    for x, b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                a = a + 1
                text = str(b[11])
                # print(text)
                text_array.append(text)
                # OCR_value = False
                if(variableText in text or variableText1 in text):
                    xAxis = int(b[6]) + x1
                    yAxis = int(b[7]) + y1
                    OCR_value = True
                    # print(xAxis, ',' , yAxis)
                    return False
            a = a + 1
    return OCR_value
    return xAxis
    return yAxis
    return text
    return text_array


def ocrImageDetection_delimeter(xAxis, yAxis, delimiterx, delimitery, variableText, bigImage):
    #mainImg, 
    # delimiterx, delimitery = 25, 25
    x1, y1, x2, y2 = xAxis - int(delimiterx), yAxis - int(delimitery), xAxis + int(delimiterx), yAxis + int(delimitery)
    # #print(x1, y1, x2, y2)
    if(x1 <= 0):
       x1 ,x2 = 0, x2 + -(x1)
    if(y1 <= 0):
       y1 ,y2 = 0, y2 + -(y1)
    if(x2 <= 0):
       x2, x1 = 0, x1 + -(x2)
    if(y2 <= 0):
       y2, y1  = 0, y1 + -(y2)
    if(x1 > 1919):
       x2, x1 = -(x1 - 1919 - x2), 1919
    if(y1 > 1079 ):
       y2, y1 = -(y1 - 1079 - y2), 1079
    if(x2 > 1919):
       x1, x2 = -(x2 - 1919 - x1), 1919
    if(y2 > 1079 ):
       y1, y2 = -(y2 - 1079 - y1), 1079
    # #print(x1, y1, x2, y2)
    # img = cv2.imread(mainImg)
    
    # print("please wait extracting text")
    global text
    global OCR_value
    OCR_value = False
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\aman\Desktop\ocrCode\Tesseract-OCR\tesseract.exe'

    img = cv2.imread(bigImage)    #(r'C:\Users\aman\Desktop\ocrCode\screenshot.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    global image
    image = Image.open(bigImage) 

    image_arr = np.array(image) 
    image_arr = image_arr[y1:y2, x1:x2]
    image = Image.fromarray(image_arr)

#def OCRFunction(image):
    boxes = pytesseract.image_to_data(image)
    ##print(boxes)
    a = 0
    for x, b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                a = a + 1
                text = str(b[11])
                # print(text)
                if(variableText in text):
                    xAxis = int(b[6]) + x1
                    yAxis = int(b[7]) + y1
                    OCR_value = True
            a = a + 1
    return OCR_value
    return text


main_path = r"C:\Users\aman\Desktop"



def image_cropper(screenshot_path, xAxis, yAxis, delimiterx, delimitery):       #mainImg, 
    # delimiterx, delimitery = 25, 25
    x1, y1, x2, y2 = xAxis - int(delimiterx), yAxis - int(delimitery), xAxis + int(delimiterx), yAxis + int(delimitery)
    # #print(x1, y1, x2, y2)
    if(x1 <= 0):
       x1 ,x2 = 0, x2 + -(x1)
    if(y1 <= 0):
       y1 ,y2 = 0, y2 + -(y1)
    if(x2 <= 0):
       x2, x1 = 0, x1 + -(x2)
    if(y2 <= 0):
       y2, y1  = 0, y1 + -(y2)
    if(x1 > 1919):
       x2, x1 = -(x1 - 1919 - x2), 1919
    if(y1 > 1079 ):
       y2, y1 = -(y1 - 1079 - y2), 1079
    if(x2 > 1919):
       x1, x2 = -(x2 - 1919 - x1), 1919
    if(y2 > 1079 ):
       y1, y2 = -(y2 - 1079 - y1), 1079
    # #print(x1, y1, x2, y2)
    # img = cv2.imread(mainImg)
    img = cv2.imread(screenshot_path)

    image_arr = np.array(img)       
    # Crop image
    image_arr = image_arr[y1:y2, x1:x2]    #250:350, 735:1174
    # Convert array to image 
    image = Image.fromarray(image_arr)
    image.save(screenshot_path)
    # Resizing the image

def imageIdentifier(codeName, screenshot_path, image_path, comparisonInt, xAxis, yAxis, delimiterx, delimitery):
    global comparisonNumber
    global error
    global error_value
    error_value = False
    comparisonNumber = comparisonInt
    screenshot = p.screenshot()
    screenshot.save(screenshot_path)
    image_cropper(screenshot_path, xAxis, yAxis, delimiterx, delimitery)
    # load the input images
    img2 = cv2.imread(image_path)
    img1 = cv2.imread(screenshot_path)
    # convert the images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # define the function to compute MSE between two images
    def mse(img1, img2):
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        return mse, diff
    error, diff = mse(img1, img2)
    if(error <= comparisonInt):
        error_value = True
    else:
        error_value = False
        # print("Image matching Error between the two images:",error, "\nHere's the code Name that's showing more errors", codeName)
    return error_value


## Code starts here onwards ##
def upper(numb):
    a = 0
    p.click(x=965, y=187)
    while a < numb:
        p.press('up')
        a = a + 1

def lower(numb):
    a = 0
    p.click(x=965, y=187)
    while a < numb:
        p.press('down')
        a = a + 1
        
        
# def tool_kit():
#     p.click(button='middle',x=396, y=21)
#     t(1)
#     p.click(button='left',x=143, y=16)
#     ocrImageDetection(x1,y1,x2,y2, "FOLLOW", 'NOODLEHEAD')
#     if(OCR_value == True):
#         p.click(button='left',x=xAxis, y=yAxis)
#         #p.moveTo(x=xAxis, y=yAxis)

def clear_python_file():
    with open(r"C:\Users\Amanjyot\Desktop\python\eob_reader\data_store.py", "w") as file_object:
        file_object.write("")
        

def start_writing_data(variableName, text_content_add):
    with open(r"C:\Users\Amanjyot\Desktop\python\eob_reader\data_store.py", "a") as file_object:
        if not text_content_add.strip():
            print(f"{variableName} IS empty")
            text_content_add = ""
            file_object.write(f"{variableName} = '{text_content_add}'\n\n")
        else:
            text_content_add = text_content_add.strip()
            text_content_add = text_content_add.replace("\n", "")
            file_object.write(f"{variableName} = '{text_content_add}'\n\n")

def start_reading_data():
    with open(r"C:\Users\Amanjyot\Desktop\python\eob_reader\texts\content.txt", "r") as file_object:
        global content
        content = file_object.read()
    text_content = content
    t(1)
    clear_python_file()
    return text_content
    






## Calling code starts from here ##
## Calling variables starts from here ##
# variables here
move = True
XList = ["do", "does", "is", "am", "are", "has", "have", "did", "was", "were", "had", "been", "will", "shall", "must", "would", "should", "may", "can", "could", "might", "okay", "sure", "right", "correct"]
YList = ["don't", "doesn't", "isn't", "aren't", "hasn't", "haven't", "didn't", "wasn't", "weren't", "hadn't", "mustn't", "wouldn't", "shouldn't", "can't", "couldn't", "sorry"]
positive_list = []
conversation_array = []
# Billing_corp = "Home aid medical supply" #"Ultima medical supply"
# patient_name = "Michael Smith"
# insurance_name = "Blue cross blue shield"
# member_id_ending_with = "8 5 4 3"
# call_back_number = "2 1 4 7 6 4 7 7 0 0"
# patient_address = "565 New Brunswick Ave, Floor 2, Fords, NJ, 07847"
Billing_corp = r"voice_commands/outbound_calls/Billing_corp.wav"
patient_name = r"voice_commands/outbound_calls/patient_name.wav"
insurance_name = r"voice_commands/outbound_calls/insurance_name.wav"
member_id_ending_with = r"voice_commands/outbound_calls/member_id_ending_with.wav"
call_back_number = r"voice_commands/outbound_calls/call_back_number.wav" 
patient_address = r"voice_commands/outbound_calls/patient_address.wav"

# Basic voices are here.
mmhm = r"voice_commands/general_audios/mmhm.wav"
can_not_hear = r"voice_commands/general_audios/can_not_hear.wav"
hung_up_no_response = r"voice_commands/general_audios/hung_up_no_response.wav"
ask_human_not_understanding = r"voice_commands/general_audios/ask_human_not_understanding.wav"
allow_me_a_minute = r"voice_commands/general_audios/allow_me_a_minute.wav"
good_morning = r"voice_commands/general_audios/good_morning.wav"
IVR_intro1 = r"voice_commands/general_audios/IVR_intro1.wav"
IVR_intro2 = r"voice_commands/general_audios/IVR_intro2.wav"
give_intro_confirm_pt_name1 = r"voice_commands/general_audios/give_intro_confirm_pt_name1.wav"
give_intro_confirm_pt_name2 = r"voice_commands/general_audios/give_intro_confirm_pt_name2.wav"
leave_vm1 = r"voice_commands/general_audios/leave_vm1.wav"
leave_vm2 = r"voice_commands/general_audios/leave_vm2.wav"
leave_vm3 = r"voice_commands/general_audios/leave_vm3.wav"
leave_vm4 = r"voice_commands/general_audios/leave_vm4.wav"
leave_vm5 = r"voice_commands/general_audios/leave_vm5.wav"
leave_vm6 = r"voice_commands/general_audios/leave_vm6.wav"
ask_them_to_talk_or_call_back = r"voice_commands/general_audios/ask_them_to_talk_or_call_back.wav"
ask_active_ins_term1 = r"voice_commands/general_audios/ask_active_ins_term1.wav"
ask_active_ins_term2 = r"voice_commands/general_audios/ask_active_ins_term2.wav"
ask_active_ins_term3 = r"voice_commands/general_audios/ask_active_ins_term3.wav"
okay_ill_arrange_cb = r"voice_commands/general_audios/okay_ill_arrange_cb.wav"




## Calling functions starts from here ##
def say_it(sound_file_list):
    # Path to the sound file
    # sound_file = r'voice_commands/inbound_calls/michelle_intro_how_I_help.wav'
    a = 0
    while a < len(sound_file_list):
    # Play the sound file
        playsound(sound_file_list[a])
        print(sound_file_list[a])
        a = a + 1

def allow_me_a_minute():
    say_it([allow_me_a_minute])

def IVR_intro():
    say_it([IVR_intro1, Billing_corp, IVR_intro2])

def give_intro_confirm_pt_name():
    say_it([give_intro_confirm_pt_name1, Billing_corp, give_intro_confirm_pt_name2, patient_name])

def leave_vm():
    say_it([leave_vm1, Billing_corp, leave_vm2 ,patient_name, leave_vm3, insurance_name, leave_vm4, member_id_ending_with, leave_vm5, call_back_number, leave_vm6])

def ask_active_ins_term():
    say_it([ask_active_ins_term1, insurance_name, ask_active_ins_term2, member_id_ending_with, ask_active_ins_term3])
    


def meaning_finder_old(sentence):
    sentence = sentence.lower()
    txt = re.sub(r"\.|,|!", "", sentence)
    x = re.split(r"\s", txt)
    sentence = x
    print(x)
    global meaning
    meaning = "negative"
    if("not" in sentence):
        meaning = "negative"
        print(x)
    else:
        a = 0
        while a < len(YList):
            if(YList[a] in sentence):
                meaning = "negative"
                break
            else:
                b = 0
                while b < len(XList):
                    if(XList[b] in sentence):
                        meaning = "positive"
                        break
                    else:
                        if("no" in sentence or "nope" in sentence):
                            meaning = "negative"
                        elif("yes" in sentence or "yeah" in sentence):
                            meaning = "positive"
                    b = b + 1
            a = a + 1
    print(meaning)
    return meaning



def key_finder_sentence_old(sentence, keys):
    sentence = sentence.lower()
    txt = re.sub(r"\.|,|!", "", sentence)
    x = re.split(r"\s", txt)
    sentence = x
    #print(sentence)
    a = 0
    global meaning
    while a < len(keys):
        current_key = keys[a]
        if current_key in sentence:
            meaning = "positive"
            print(sentence, ": I am here 4" , keys)
            print("meaning: ",meaning)
            break
        else:
            meaning = "negative"
            #print(current_key)
            print(sentence, ": I am here 5", keys)
            a = a + 1
    print(meaning)



def dataset_key_finder_sentence(sentence, keys):
    sentence = sentence.lower()
    txt = re.sub(r"\.|,|!", "", sentence)
    x = re.split(r"\s", txt)
    sentence = x
    all(item.lower() in sentence for item in keys)   


def main():
    if move == True:
        path1()
##    if move == True:
##        path2()
##    if move == True:
##        path3()













# other functions
def call_human_on_teams(error):
## send a text to the manager with the error so that they can come and fix it.
    print("Calling human on teams for: ", error)

def send_audios_to_kokoro_TTS(variables_array_names, variables_array_values):
    global audio_convertion_completed
    audio_convertion_completed = False
    a = 0
    while len(variables_array_names) > a:
        # Misaki G2P with espeak-ng fallback
        fallback = espeak.EspeakFallback(british=False)
        g2p = en.G2P(trf=False, british=False, fallback=fallback)

        # Kokoro
        kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

        # Phonemize
        # text = "[Misaki](/misˈɑki/) is a G2P engine designed for [Kokoro](/kˈOkəɹO/) models."
        text = str(variables_array_values[a])
        audio = str(variables_array_names[a])
        phonemes, _ = g2p(text)

        # Create
        samples, sample_rate = kokoro.create(phonemes, "af_heart", is_phonemes=True, speed=1.0, lang="en-us")

        # print("Playing audio...")
        # sd.play(samples, sample_rate)
        # sd.wait()

        print("Saving file")
        # path = r"voice_commands/outbound_calls/"
        path = r"voice_commands/general_audios/"
        sf.write(f"{path}{audio}.wav", samples, sample_rate)
        print(f"Created {audio}.wav")
        a = a + 1
    audio_convertion_completed = True
    print("All files has been converted to audio files.")


def general_audios_generator():
    mmhm = "mmhm"
    can_not_hear = "Hello, I cannot hear you. can you hear me?"
    hung_up_no_response = "Because of no response you call is being disconnected, Good Bye!"
    ask_human_not_understanding = "Actually I didn't get that I'll ask for a human"
    allow_me_a_minute = "[Allow me a minute](/ əˈlaʊ miː ə maɪˈnjuːt /). I'll check it for you."
    good_morning = "[Hello!](/ həˈləʊ /) [Good morning](gʊ ˈmɔːnɪŋ /)."
    IVR_intro1 = "I am michelle, from "
    IVR_intro2 = ". calling about your cpap supplies."
    give_intro_confirm_pt_name1 = "Hello, good morning! my name is michelle. I am a ai voice assistant and I am calling from "
    give_intro_confirm_pt_name2 = ", am I speaking to ,"
    leave_vm1 = "Hello, good morning! my name is michelle. I am a ai voice assistant and I am calling from "
    leave_vm2 = ", this call is for "
    leave_vm3 = ", it's about your cpap supplies order but we need your active insurance because the member ID for "
    leave_vm4 = ", ending with "
    leave_vm5 = ", is showing inactive, Please call us at "
    leave_vm6 = ", and ask for michelle. Thanks Bye!"
    ask_them_to_talk_or_call_back = "I see, so will it be okay for me to speak with you? actually It's about their cpap supplies, else I can call you back sometime tomorrow!"
    ask_active_ins_term1 = "So, It's about your cpap supplies, actually we need your active insurance because "
    ask_active_ins_term2 = ", member id ending with "
    ask_active_ins_term3 = ". is showing inactive, so do you have any active insurance?"
    okay_ill_arrange_cb = "I see, I'll call you back then. Thanks for attending the call! bye!"
    variables_array_names = ["mmhm"]
    # ("good_morning", "IVR_intro1", "IVR_intro2", "give_intro_confirm_pt_name1", "give_intro_confirm_pt_name2", "leave_vm1", "leave_vm2", "leave_vm3", "leave_vm4",
                            # "leave_vm5", "leave_vm6", "ask_them_to_talk_or_call_back", "ask_active_ins_term1", "ask_active_ins_term2", "ask_active_ins_term3", "okay_ill_arrange_cb")
    variables_array_values = [mmhm]
    # (good_morning, IVR_intro1, IVR_intro2, give_intro_confirm_pt_name1, give_intro_confirm_pt_name2, leave_vm1, leave_vm2, leave_vm3, leave_vm4,
                                # leave_vm5, leave_vm6, ask_them_to_talk_or_call_back,  ask_active_ins_term1, ask_active_ins_term2, ask_active_ins_term3,  okay_ill_arrange_cb)
    send_audios_to_kokoro_TTS(variables_array_names, variables_array_values)

#1st step Done
def remember_content_before_calling_patient():
    #In This step, gather all the information and convert it into voice audio files.
    #eg: $Billing_corp, $patient_name, $insurance_name, $member_id, $call_back_number, $patient_address
    #This process will be called everytime before making a call,
    #once all these informations are gathered, It will send them to KOKORO TTS for audion files.
    Billing_corp = "Home aid medical supply" #"Ultima medical supply"
    patient_name = "Michael Smith"
    insurance_name = "Blue cross blue shield"
    member_id_ending_with = "8 5 4 3"
    call_back_number = "2 1 4 7 6 4 7 7 0 0"
    patient_address = "565 New Brunswick Ave, Floor 2, Fords, NJ, 07847"
    
    # variables_array_names, variables_array_values = [], []
    variables_array_names = ("Billing_corp", "patient_name", "insurance_name", "member_id_ending_with", "call_back_number", "patient_address")
    variables_array_values = (Billing_corp, patient_name, insurance_name, member_id_ending_with, call_back_number, patient_address)
    send_audios_to_kokoro_TTS(variables_array_names, variables_array_values)

    #send these to KOKORO TTS for audio files.
    if(len(variables_array_names) == len(variables_array_values)):
        send_audios_to_kokoro_TTS(variables_array_names, variables_array_values)
    else:
        print("Length of variables are not same please re-check code here.")


#2nd step Done
def on_call_finder():
    #check if the ringcx status is in interception or not.
    #see the status everytime before moving to next path(), if on_call == True or False.
    #If it's True, call main().
    #If it's false stay on look out for the status.
    global call_status
    global on_call
    ocrImageDetectionUI(1539, 944, 1904, 1017, "Available", "available")
    if(OCR_value == True):
        call_status = "available"
        on_call = False
    else:
        ocrImageDetectionUI(1539, 944, 1904, 1017, "Engaged", "engaged")
        if(OCR_value == True):
            call_status = "engaged"
            on_call = True
        else:
            call_status = "Unable to find the status contacting humans to help out"
            call_human_on_teams(call_status)
            on_call = False


#3rd step
def path1():
    def key_finder_sentence(sentence, keys):
        sentence = sentence.lower()
        txt = re.sub(r"\.|,|!", "", sentence)
        x = re.split(r"\s", txt)
        sentence = x
        #print(sentence)
        a = 0
        nonlocal meaning
        while a < len(keys):
            current_key = keys[a]
            if current_key in sentence:
                meaning = "positive"
                print(sentence, ": I am here 4" , keys)
                print("meaning: ",meaning)
                break
            else:
                meaning = "negative"
                #print(current_key)
                print(sentence, ": I am here 5", keys)
                a = a + 1
        print(meaning)

    def meaning_finder(sentence):
        sentence = sentence.lower()
        txt = re.sub(r"\.|,|!|‘|-", "", sentence)
        x = re.split(r"\s", txt)
        sentence = x
        print(x)
        nonlocal meaning
        meaning = "negative"
        if("not" in sentence):
            meaning = "negative"
            print(x)
        else:
            a = 0
            while a < len(YList):
                if(YList[a] in sentence):
                    meaning = "negative"
                    break
                else:
                    b = 0
                    while b < len(XList):
                        if(XList[b] in sentence):
                            meaning = "positive"
                            break
                        else:
                            if("no" in sentence or "nope" in sentence):
                                meaning = "negative"
                            elif("yes" in sentence or "yeah" in sentence):
                                meaning = "positive"
                        b = b + 1
                a = a + 1
        print(meaning)
        return meaning

    meaning = "neutral"
    t(0.5)
    say_it([good_morning])
    ## sentence = input()
    get_sentence()
    #Returns sentence
# 6th step
    Intro_keys = ["hello", "hella", "hi", "yes", "who", "this", "good"]
    VM_keys = ["voicemail", "unable", "person", "message", "leave", "voice"]
    IVR_keys = ["see", "connect", "say", "what"]
    Ask_active_ins_keys = []
    # If it returns meaning = positive, then proceed with it. else meaning = negative.

    key_finder_sentence(sentence, IVR_keys)
    print(meaning, "I am here my friend 1")
    if(meaning == "positive"):
        IVR_intro()
        move = True
        path1()
        # Add things here.
        meaning = "negative"
    else:
        key_finder_sentence(sentence, VM_keys)
        print(meaning, "I am here my friend 2")
        if(meaning == "positive"):
            leave_vm()
            move = False
            meaning = "negative"
        else:
            key_finder_sentence(sentence, Intro_keys)
            if meaning != "positive":
                meaning_finder(sentence)
            print(meaning, "I am here my friend 3")
            if(meaning == "positive"):
                print(meaning, "I am here my friend 4")
                give_intro_confirm_pt_name()
                move = True
                meaning = "negative"

# PROBLEM: ** 70% project Achieved, now to get 5% more you need to work on all the paths and database adding and checking.
# Make it compatible with all the examples present on the folder that it doesn't give any error and works acurately.
# If I succeed I will get 75% completion rate of this project. rest of the 5% includes letting it see and process the data before making the call. **

                get_sentence()
                # key_finder_sentence(sentence, Ask_active_ins_keys)
                meaning_finder(sentence)
                print(meaning, "I am here my friend 5")
                if meaning == "positive":
                    ask_active_ins_term()
                    meaning = "negative"
                    


                else:
                    say_it([ask_them_to_talk_or_call_back])
                    print(meaning, "I am here my friend 6")
                    meaning = "negative"
            elif(meaning == "negative"):
                say_it([okay_ill_arrange_cb])
                meaning = "negative"





# 6th step
def remove_old_list_from_new_one(newlist, oldlist):
#find if list1[-3], list1[-2] and list1[-1]
#are present in the newlist and if their positions are like this or not.
    global sentence
    if(oldlist != [] and len(newlist) != []):
        target_item1 = oldlist[-1]
        target_item0 = oldlist[0]
        target_item = newlist[0]
    if len(oldlist) > 1:
        target_item2 = oldlist[-2]
    if len(oldlist) > 2:
        target_item3 = oldlist[-3]
    elif len(newlist) == []:
        print("Live caption is not present please check it out.")
        return False

    index_len = len(oldlist)
    new_index_len = len(newlist)

    if index_len >= new_index_len:
        looper = new_index_len
    elif index_len < new_index_len:
        looper = index_len
        
    a = 0
    indexes1, indexes2, indexes3 = [], [], []
    while a < looper:
        if(oldlist != [] and newlist[a] == target_item1 and newlist != []):
            indexes1.append(a)
        elif(len(oldlist) > 1 and newlist[a] == target_item2):
            indexes2.append(a)
        elif(len(oldlist) > 2 and newlist[a] == target_item3):
            indexes3.append(a)
        a = a + 1

    # print(indexes1, target_item1)
    # print(indexes2, target_item2)
    # print(indexes3, target_item3)
##    print((index_len -1), (new_index_len -1))
    if(target_item != target_item0):
        x = oldlist.index(target_item)
        extra_newlist = newlist[-x:]
        print(extra_newlist)
    if(indexes3 != []):
        numb = indexes3[-1] + 3
        del newlist[0:numb]
    elif(indexes2 != []):
        numb = indexes2[-1] + 2
        del newlist[0:numb]
    elif(indexes1 != []):
        numb = indexes1[-1] + 1
        del newlist[0:numb]

    sentence = newlist
    if sentence == [] and target_item != target_item0:
        sentence = extra_newlist
    print(sentence, ": I am here 2")



# 5th step
def take_live_caption_screenshots():
    # def check_live_caption():
    # if(len(conversation_array) > 1):
    #     prev_sentence = conversation_array[-1]
    #     print(prev_sentence, ": I am here 1")
    global not_speaking
    ocrImageDetectionUI(1371, 789, 1915 , 1025, "Text", "Text")
    #print(text_array)
    b = []
    for x in text_array:
        txt = re.sub(r"\.|,|!|`|~|;", "", x)
        b.append(txt)
    conversation_array.append(b)
    # conversation_array.append(text_array)
    # sentence = conversation_array[-1]
    # if sentence != [] and prev_sentence != []:
    #     remove_old_list_from_new_one(sentence, prev_sentence)
    #     print(conversation_array, "I am here 17")

    if len(conversation_array) > 1:
        not_speaking = conversation_array[-1] == conversation_array[-2]
    else:
        not_speaking = False
    speaking_array.append(not_speaking)


# 4th step
def get_sentence():
    meaning = "negative"
    global prev_sentence
    prev_sentence = []
    global sentence
    global conversation_array
    global speaking_array
    sentence = []
    a = 0
    global speak_allowed
    not_speaking = False
    if(len(conversation_array) > 1):
      prev_sentence = conversation_array[-1]
      print(prev_sentence, ": I am here 1")
    conversation_array = []
    speaking_array = []
    while a < 41:
        take_live_caption_screenshots()
        sentence = conversation_array[-1]
        # print(sentence, ": I am here 10") 
        # print(prev_sentence, ": I am here 11") 
        
        if(len(speaking_array) > 3):
            print(sentence, ": I am here 12") 
            print(conversation_array, ": I am here 13")
            print(speaking_array)
            if(speaking_array[-3] == True and speaking_array[-2] == True and speaking_array[-1] == True and sentence != []):
                speak_allowed = True
                # path1()
                if sentence != [] and prev_sentence != []:
                    remove_old_list_from_new_one(sentence, prev_sentence)
                    print(sentence, ": I am here 20")
                print(sentence, ": I am here 21")
                # returns sentence = ['Live', 'Caption', 'Hello']
                if sentence != []:
                    sentence = ' '.join(conversation_array[-1])
                    print(sentence, ": I am here 3")
                    # say_it([allow_me_a_minute])
                    break

        #For making it wait for 10 seconds and if no response received it will take following actions.    
        if(sentence == [] and a % 8 == 0 and a > 0):
            say_it([can_not_hear])
            print(a)

        if(sentence == [] and a == 40 and a > 0):
            say_it([hung_up_no_response])
            return False

        if(a % 15 == 0 and a > 0 and sentence != []):
            say_it([mmhm])

        t(0.5)
        a = a + 1
    #say_it([allow_me_a_minute])
    print(speaking_array)
    if sentence == []:
        say_it([can_not_hear])
        call_human_on_teams(sentence)
    sentence = ' '.join(conversation_array[-1])  












##remember_content_before_calling_patient()
##on_call_finder()
##if on_call == True and move == True:
##    path1()
##if on_call == True and move == True:
##    path2()
##if on_call == True and move == True:
##    path3()






path1()


