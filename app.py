from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)

categories = ["keys", "coffee_mug", "kitchen_table", "bed"]
uploads_folder = os.path.join("static", "uploads")
for category in categories:
    os.makedirs(os.path.join(uploads_folder, category), exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            image = request.files['image']
            category_of_image = request.form['category']
            filename = f"{int(time.time() *1000) % 10000}_{image.filename}"
            if category_of_image not in categories:
                return jsonify({"error": "This category doesn't exist"}), 400
            save_path = os.path.join(uploads_folder, category_of_image, filename)
            image.save(save_path)
            return jsonify({"message": "Photo saved successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('home.html', categories=categories)

@app.route('/play')
def play():
    title = "Who do I belong to?"
    category_images = {}
    array_test = [1, 2, 3]
    for category in categories:
        file_path = os.path.join(uploads_folder, category)
        images = os.listdir(file_path) #list all images in the file_path
        #file_paths = [os.path.join(file_path, image) for image in images]
        #file_paths = [os.path.join('uploads', category, image) for image in images] #an array with a filepath to each image
        file_paths = [os.path.join(category, image) for image in images]
        category_images[category] = file_paths
    return render_template('play.html', title=title, categories=categories, category_images=category_images, file_path=file_path, images=images, file_paths=file_paths, array_test=array_test)

if __name__ == '__main__':
    app.run(debug=True)