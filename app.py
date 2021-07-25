from flask import Flask, request, jsonify
from api import get_image_info, save_data
import os


app = Flask(__name__)

@app.route('/image', methods=['GET', 'POST'])
def image():
    
    image_sent = request.files['image']
    filename = image_sent.filename
    company = request.form['company']
    
    img_file_path = os.path.join('tmp', filename)
    image_sent.save(img_file_path)
    
    image_info = get_image_info.execute(filename, img_file_path, company)
        
    is_file_saved = save_data.execute(image_sent.filename, img_file_path, image_info)
    
    os.remove(img_file_path)
    
    if is_file_saved:
        return jsonify(image_info)
    else:
        return 'Error'
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',  port=8080)
