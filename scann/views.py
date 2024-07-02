from django.shortcuts import render

# Create your views here.
import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

import pytesseract
import re
from unidecode import unidecode
#from google.colab import files
import cv2
import pandas as pd

from datetime import datetime
import socket
import os
from django.core.files.storage import default_storage

from employe.models import Employe
from datetime import datetime

from django.http import JsonResponse

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from SystemConf.Back_Control_Access import is_admin







# Set the path to the Tesseract executable (update this with your path)
# LINUX
#pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
## WINDOWS
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@login_required(login_url="user_signin")
def import_cnib(request):
    data=[]
    if request.method=='POST':
        fichiers=request.FILES.getlist("fichier")#FILES['fichier']
        for fichier in fichiers:
            path='media/'+uploadFile(fichier, 'import/')
            result=extract_card_info(path)

            
            if result['nom'] and result['prenoms'] and result['sexe'] and result['date_naiss'] and result['profession']:
                employe=Employe()
                try:
                    employe.nom=result['nom']
                    employe.prenoms=result['prenoms']
                    employe.date_naissance=datetime.strptime(str(result['date_naiss']), "%d/%m/%Y").strftime("%Y-%m-%d")
                    employe.sexe=result['sexe']
                    employe.save()
                    result['enregistre']=True
                except:
                    result['enregistre']=False
            deleteFile(path)
            data.append(result)
    
    return render(request, 'scan/list.html', {'data':data})
    


def extract_card_info(image_path):
    # Open the image file
    img = cv2.imread(image_path)
    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)

    # Use Tesseract to do OCR on the image
    text1 = pytesseract.image_to_data(threshed, output_type='data.frame')
    text2 = pytesseract.image_to_string(threshed, lang="eng+ind")

    # Split the OCR result into lines
    lines = [line.strip() for line in text2.split('\n')]

    # Define patterns for extracting information using regular expressions
    patterns = {
        "nom": re.compile(r"Nom: (.+)", re.IGNORECASE),
        "prenoms": re.compile(r"Pr[ée]noms?: (.+)", re.IGNORECASE),
        "date_naiss": re.compile(r"N[ée]\(e\) le: (.+?) A", re.IGNORECASE),
        "sexe": re.compile(r"Sexe: (.+?) Taille:", re.IGNORECASE),
        "taille": re.compile(r"Taille: (.+)", re.IGNORECASE),
        "profession": re.compile(r"Profession: (.+)", re.IGNORECASE),
        "expire": re.compile(r"Expire le: (.+?) ([A-Z0-9]+)", re.IGNORECASE),
        "numero": re.compile(r"Expire le: .+? ([A-Z0-9]+)", re.IGNORECASE)
    }

    # Initialize variables to store extracted information
    extracted_info = {
        "nom": "",
        "prenoms": "",
        "date_naiss": "",
        "sexe": "",
        "taille": "",
        "profession": "",
        "expire": "",
        "numero": ""
    }

    # Loop through lines and extract information using regular expressions
    for line in lines:
        line = unidecode(line)
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                extracted_info[key] = match.group(1).strip()

    return extracted_info


#result= extract_card_info('image_test/img4.jpg')


def uploadFile(file_input, folder):
      #name=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str(extension)
    file_name=folder+str(file_input)
    return default_storage.save(file_name, file_input)


def deleteFile(link):
	exist=os.path.exists(link)
	if exist:
		os.remove(link)

def test(request):
       emp=Employe
       emp.nom='MILLOGO'
       emp.prenom='Alexander'
       emp.date_naissance=datetime.strptime('03/12/2000', "%d/%m/%Y").strftime("%Y-%m-%d")
       emp.sexe='M'
       emp.save()
       return JsonResponse(list(emp), safe=False)