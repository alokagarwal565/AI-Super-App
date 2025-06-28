from flask import Flask, render_template, request, jsonify, redirect, session, flash, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import replicate
import requests
import bcrypt
import os
import base64
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, default=10)  # Add credits column
    
    # Define columns for up to 10 images
    image1 = db.Column(db.LargeBinary, nullable=True)
    image2 = db.Column(db.LargeBinary, nullable=True)
    image3 = db.Column(db.LargeBinary, nullable=True)
    image4 = db.Column(db.LargeBinary, nullable=True)
    image5 = db.Column(db.LargeBinary, nullable=True)
    image6 = db.Column(db.LargeBinary, nullable=True)
    image7 = db.Column(db.LargeBinary, nullable=True)
    image8 = db.Column(db.LargeBinary, nullable=True)
    image9 = db.Column(db.LargeBinary, nullable=True)
    image10 = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, name, email, password, image1=None, image2=None, image3=None, image4=None, image5=None, image6=None, image7=None, image8=None, image9=None, image10=None, credits=10):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.image4 = image4
        self.image5 = image5
        self.image6 = image6
        self.image7 = image7
        self.image8 = image8
        self.image9 = image9
        self.image10 = image10
        self.credits = credits  # Initialize credits correctly

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

def download_image(image_url, filename): 
    response = requests.get(image_url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print("FAILURE!!!!")

@app.route('/')
def index():
    if 'email' in session:
        return redirect('/dashboard')  # Redirect to dashboard if logged in
    return render_template('index.html')  # For visitors

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in or use a different email.', 'error')
            return redirect('/register')

        # Ensure that the credits argument is included
        new_user = User(name=name, email=email, password=password, image1=None, image2=None, image3=None, image4=None, image5=None, image6=None, image7=None, image8=None, image9=None, image10=None, credits=10)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            # flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)

    flash('Please log in to access the AI Super App.', 'warning')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logged out successfully.', 'success')
    return redirect('/login')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data['prompt']
    hf_lora = data.get('hf_lora')  # Using .get() to avoid KeyError if 'hf_lora' is missing

    user = User.query.filter_by(email=session['email']).first()
    
    if user.credits != 0:
            # Deduct one credit
        user.credits -= 1
        db.session.commit()

    # Check if hf_lora is provided
    if hf_lora:
    # If hf_lora is not empty, use the first model
     if hf_lora == "alokagarwal/dipto":
        input_data = {
            "prompt": prompt,
            "hf_lora": hf_lora
        }
        output = replicate.run(
            "itsiiie/dipto-lora:9246adc23e2bd44f1a1e7a1aee6650840cd7ed2a6f9f0d56b787d19c429c35ca",
            input={
                "model": "dev",
                "lora_scale": 1,
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "webp",
                "guidance_scale": 3.5,
                "output_quality": 90,
                "prompt_strength": 0.8,
                "extra_lora_scale": 1,
                "num_inference_steps": 28,
                "prompt": prompt  # Corrected syntax
            }
        )
     else:
        input_data = {
            "prompt": prompt,
            "hf_lora": hf_lora
        }
        output = replicate.run(
            "lucataco/flux-dev-lora:091495765fa5ef2725a175a57b276ec30dc9d39c22d30410f2ede68a3eab66b3",
            input=input_data
        )

            
    else:
        # If hf_lora is empty, use the second model
        output = replicate.run(
            # "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            "xlabs-ai/flux-dev-realism:39b3434f194f87a900d1bc2b6d4b983e90f0dde1d5022c27b52c143d670758fa",
            input={"prompt": prompt}
        )

    # Fetch the latest predictions
    predictions = replicate.predictions.list()

    if predictions.results:
        latest_prediction = predictions.results[0]
        output_url = latest_prediction.output[0] if latest_prediction.output else None

        if output_url:
            download_image(output_url, "static/output.jpg")
            return jsonify({"status": "success", "image_url": "static/output.jpg"})

    return jsonify({"status": "error", "message": "No predictions available."})


@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json
    email = data['email']
    image_url = data['image_url']

    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        user = User.query.filter_by(email=email).first()
        if user:
            # Find the first empty image slot
            for i in range(1, 11):
                column_name = f"image{i}"
                if getattr(user, column_name) is None:
                    setattr(user, column_name, image_data)
                    db.session.commit()
                    return jsonify({"status": "success", "message": f"Image saved in {column_name}."})
            
            # All image columns are filled
            return jsonify({"status": "error", "message": "All image slots are full. Buy premium to save more images."})
        else:
            return jsonify({"status": "error", "message": "User not found."})
    else:
        return jsonify({"status": "error", "message": "Failed to fetch image."})


@app.template_filter('b64encode')
def b64encode(data):
    return base64.b64encode(data).decode('utf-8') if data else None

@app.route('/gallery')
def gallery():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            images = [getattr(user, f"image{i}") for i in range(1, 11) if getattr(user, f"image{i}") is not None]
            if images:
                return render_template('gallery.html', images=images, user=user)
            else:
                return render_template('gallery.html', message="No image saved yet.", user=user)
    
    flash('Please log in to access the gallery.', 'warning')
    return redirect('/login')

@app.route('/delete_image', methods=['POST'])
def delete_image():
    user = User.query.filter_by(email=session['email']).first()
    image_index = int(request.form['image_data'])  # Get image index from form data
    if user:
        # Delete the selected image
        column_name = f"image{image_index}"
        setattr(user, column_name, None)

        # Gather all image column names
        image_columns = [f"image{i}" for i in range(1, 11)]  # Assuming 10 images max

        # Get the images and shift non-empty images to the left
        images = [getattr(user, col) for col in image_columns]
        non_empty_images = [img for img in images if img is not None]
        shifted_images = non_empty_images + [None] * (len(images) - len(non_empty_images))

        # Update the user's images in the database
        for col, new_value in zip(image_columns, shifted_images):
            setattr(user, col, new_value)

        db.session.commit()

    return redirect('/gallery')

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user = User.query.filter_by(email=session['email']).first()
    if user:
        db.session.delete(user)  # Delete the user from the database
        db.session.commit()
        # flash('User deleted successfully.', 'success')
        session.pop('email', None)  # Log the user out after deletion
    
    return redirect('/home')  # Redirect to home or any other page

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/gen_video')
def gen_video():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('gen_video.html', user=user)

    flash('Please log in to access the AI Super App.', 'warning')
    return redirect('/login')

# Path where generated videos will be stored
output_path = 'generated_videos'
os.makedirs(output_path, exist_ok=True)

@app.route('/generate_video', methods=['POST'])
def generate_video():
    # Get the input prompt from the frontend
    data = request.get_json()
    prompt = data.get('prompt')
    
    # Ensure prompt is provided
    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required"}), 400
    
    # Prepare input for the model
    input_data = {
        "seed": 255224557,
        "n_prompt": "badhandv4, easynegative, ng_deepnegative_v1_75t, verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
        "prompt": prompt
    }
    
    user = User.query.filter_by(email=session['email']).first()

    if user.credits != 0:
            # Deduct one credit
        user.credits -= 1
        db.session.commit()

    try:
        # Call replicate model to generate video
        output = replicate.run(
            "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48a9f",
            input=input_data
        )

        # Save the video output to file
        video_path = os.path.join(output_path, 'output.mp4')
        with open(video_path, "wb") as file:
            file.write(output.read())

        # Return the URL to the video
        video_url = f"/generated_videos/output.mp4"
        return jsonify({"status": "success", "video_url": video_url})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Serve the generated video file
@app.route('/generated_videos/<filename>')
def serve_video(filename):
    return send_from_directory(output_path, filename)

@app.route('/start_chatbot')
def start_chatbot():
    # Path to the AI chatbot folder
    chatbot_folder_path = os.path.join(os.getcwd(), 'templates', 'ai_chatbot')

    try:
        # Run npm run dev inside ai_chatbot folder on localhost:5173
        subprocess.Popen(['npm', 'run', 'dev'], cwd=chatbot_folder_path, shell=True)
        # Optional: Redirect to chatbot URL
        return jsonify({
            "status": "success",
            "message": "Chatbot started successfully.",
            "chatbot_url": "http://localhost:5173/"
        })
    except FileNotFoundError as e:
        print("Error:", e)
        return jsonify({
            "status": "error",
            "message": "FileNotFoundError: Ensure Node.js and npm are correctly installed."
        }), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
