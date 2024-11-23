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
            filename = f"{int(time.time())}_{image.filename}"
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
    return render_template('play.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)