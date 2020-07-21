#!/usr/bin/env python
# coding: utf-8

# In[16]:


import json
import os
import sys
import requests
import time
from google.cloud import vision
from google.cloud.vision import types
import traceback
import pytesseract


# In[15]:
''' Class for OCR extraction using Azure Cognitive services'''

class Azure_ocr:
    
    def __init__(self):
        azure_config="config/azure_config.json"
        # Reading endpoint and subscription key from azure_config file
        self.ocr_url=azure_config['endpoint']+"vision/v3.0/ocr"
        self.subscription_key=azure_config['subscription_key']
        self.headers={'Ocp-Apim-Subscription-Key': self.subscription_key, 'Content-Type': 'application/octet-stream'}
        self.param={'language': 'unk', 'detectOrientation': 'true'}
        
    def get_ocr_text(self,image_path):
        try:
            image_data=open(image_path,"rb").read()
            response=requests.post(self.ocr_url,headers=self.headers,params=self.param,data=image_data)
            self.analysis=response.json()
            text=[]
            for line_info in self.analysis['regions']:
            # extracting words and froming line 
                line=[words_info['text'] for w in line_info['lines'] for words_info in w['words']]
    #             print(line)
                text.append(" ".join(line))
        except:
            print('OCR exception occured')
            traceback.print_exc()
            text=None
        finally:
            return text,_
            


# In[12]:

''' Class for OCR extraction using Google Vision services'''
class Google_ocr:
    def __init__(self):
        google_vision_key="config/google-vision-key.json"
        ''' read google vision credential from google vision'''
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_vision_key
        self.vision_client = vision.ImageAnnotatorClient()
    def get_ocr_text(self,image_path):
        try:
            image_data=open(image_path,"rb").read()
            image = types.Image(content=content)

            kwargs = {}
            if lang_hint:
                kwargs = {"image_context": {"language_hints": ["en", "hi", "mr", "bn", "ta",'te','kn','gu','or']}}

            response = self.vision_client.text_detection(image=image,**kwargs)
            texts = response.text_annotations

            bboxes = []
            for text in texts:
                bbox = []
                bbox.append(text.description)
                for vertice in text.bounding_poly.vertices:
                    bbox.extend([vertice.x,vertice.y])
                bboxes.append(bbox)

            document = response.full_text_annotation

            paratext = ""
            blocktext = ""
            blocks = []

            for page in document.pages:
                for block in page.blocks:
                    blocktext = ""
                    for paragraph in block.paragraphs:
                        paratext = ""
                        for word in paragraph.words:
                            strWord = ""
                            for symbol in word.symbols:
                                strWord = strWord + symbol.text
                            paratext = paratext + " " + strWord
                        blocktext = blocktext + " " + paratext
                    blocks.append(blocktext.strip())
        except:
            print(" OCR_exception")
            traceback.print_exc()
            bboxes=None
            blocks=None
        finally:
            return bboxes,blocks
            
    


# In[ ]:
''' Simple pytesseract class for text extraction'''

class Pytesseract_lib:
    def __init__(self):
        pass
    def get_ocr_text(self,image_path):
        try:
            text=pytesseract.image_to_string(image_path)
        except:
            print("OCR error in Pytesseract_lib class")
            text=None
        finally:
            return text,_
        


# In[ ]:


''' Abstract factory Class
Default parameter is google ocr'''

class OCR_extraction:
    def __init__(self,extract_using="google_ocr"):
        extractor={
            "google_ocr":Google_ocr,
            "azure_ocr":Azure_ocr,
            "pytesseract_lib":Pytesseract_lib,
        }
        self.extract=extractor[extract_using]()
        
    def get_text(self,image_path):
        return self.extract.get_ocr_text(image_path)






