import tensorflow as tf
import cv2
import os 
import numpy as np
from pyzbar.pyzbar import decode
from tensorflow.keras.models import load_model
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

model = load_model("server/model/qr.h5")

@csrf_exempt
def classify_qr_code(request):
    if request.method == "POST":
        try:
            qr_code_image = request.FILES["qr_code"]
            print(qr_code_image)

            file_path = os.path.join("server/images", qr_code_image.name)

            with open(file_path, "wb+") as destination:
                for chunk in qr_code_image.chunks():
                    destination.write(chunk)

            qr_code = cv2.imread(file_path)

            url = ""
            decoded_objects = decode(qr_code)
            for obj in decoded_objects:
                data = obj.data.decode("utf-8")
                url += str(data.split()[1])

            qr_code = cv2.resize(qr_code, (128, 128))
            qr_code = np.array(qr_code)
            qr_code = qr_code / 255.0

            test = np.expand_dims(qr_code, axis=0)
            prediction = model.predict(test)
            prediction = prediction.argmax()
            prediction = "Benign" if prediction == 0 else "Malicious"

            context = {"result": prediction, "url": url}
            return render(request, "predict.html", context)
        
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, "index.html")
