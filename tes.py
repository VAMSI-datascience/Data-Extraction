from PIL import Image
import PIL.Image
import os
import base64
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from pytesseract import image_to_string
import pytesseract
import re
from io import BytesIO

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class ExtractDateFromImage(Resource):

    def post(self):

        parser.add_argument('base_64_image_content')
        args = parser.parse_args()

        byte_data = base64.b64decode(args['base_64_image_content'])
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        img.save("sample.jpeg")

        pytesseract.pytesseract.tesseract_cmd = 'tesseract'
        #TESSDATA_PREFIX = 'Tesseract-OCR'
        output = pytesseract.image_to_string(Image.open("sample.jpeg"))
        os.remove("sample.jpeg")

        try:
            op = str(output)
        except:
            op = str(output.encode('utf-8'))

        #print op

        all = re.findall(
            r"[ADFJMNOS]\w*[\d]{1,2}, [\d]{4}|[\d]{1,2} [ADFJMNOS]\w* [\d]{4}|[\d]{1,2}/[\d]{1,2}/[\d]{2}|[\d]{1,2}/[\d]{1,2}/[\d]{2,}|[\d]{1,2}-[\d]{1,2}-[\d]{2}|[ADFJMNOS]\w*[\d]{2}.? [\d]{2}",
            op)
        if all:
            return {'date': all[0]}
        else:
            return {'date': 'null'}


api.add_resource(ExtractDateFromImage, '/')

if __name__ == '__main__':
    app.run(debug=False)