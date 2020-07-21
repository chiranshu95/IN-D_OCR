# IN-D_OCR
Generic OCR API

It contains OCR.py
There are 3 classes for Text extraction 
  - google vision
  - azure cognitive service
  - pytesseract lib
  
 There is abstraction class .
 To use any type of OCR techniques
 make an instance of OCR_extraction class 
 eg:
 Argument that can be passed while creating object : {'google_ocr','azure_ocr','pytesseract_lib'} By default parameter: google_ocr
 obj=OCR_extraction("google_ocr")
 text=obj.get_text(image_path)
 
