import cv2
import numpy as np
import matplotlib.pyplot as plt
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

def seperate_each_line(img) -> list:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Getting the threshold
    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    
    # minAreaRect on the nozeros
    pts = cv2.findNonZero(threshed)
    ret = cv2.minAreaRect(pts)

    (cx,cy), (w,h), ang = ret
    if w>h:
        w,h = h,w
        ang += 90
    
    # Find and draw the upper and lower boundary of each lines
    hist = cv2.reduce(threshed,1, cv2.REDUCE_AVG).reshape(-1)

    th = 2
    H,W = img.shape[:2]
    uppers_y = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
    lowers_y = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

    threshed = cv2.cvtColor(threshed, cv2.COLOR_GRAY2BGR)
    
    # Crop the image
    cropped_images = []
    i = 0
    while(i < len(uppers_y)):
        cropped_img = threshed[uppers_y[i]:lowers_y[i], 0:W]
        cropped_images.append(abs(255-cropped_img))
        i += 1

    return cropped_images

def get_answer_text(img) -> str:
    # 1) Seperate each image into seperate lines
    line_images = seperate_each_line(img)

    # 2) For each line call the OCR model
    answer_text = ""
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
    for line in line_images:
        pixel_values = processor(images=line, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        answer_text += generated_text + " \n"

    return answer_text

def __test_seperate_each_line(lineNo=0):
    img = cv2.imread("C:\Harsh Rao Dhanyamraju\Projects\AIfinity Hackathon\AutoRegressive-Alliance\Test\MultiLine_OCR_Test2.jpeg")
    line_images = seperate_each_line(img)
    plt.imshow(line_images[lineNo])
    plt.show()

def __test_get_answer_text():
    img = cv2.imread("C:\Harsh Rao Dhanyamraju\Projects\AIfinity Hackathon\AutoRegressive-Alliance\Test\MultiLine_OCR_Test3.jpeg")
    results = get_answer_text(img)
    print("------------ Multiline Results ---------- \n ", results)

# __test_seperate_each_line(3)
__test_get_answer_text()