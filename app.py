from flask import Flask, render_template, request, jsonify, redirect, session, flash, url_for, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
import replicate
import requests
import bcrypt
import os
import base64
import subprocess
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VEO_MODEL = "veo-3.1-generate-preview"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta1"

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
    
    def __init__(self, name, email, password, credits=10):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.credits = credits  # Initialize credits correctly

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class UserVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class UserImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

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

@app.route('/gen_image')
def gen_image():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('gen_image.html', user=user)
    flash('Please log in to access the Studio.', 'warning')
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
    if 'email' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    data = request.json
    email = data['email']
    image_url = data['image_url']

    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a unique filename
            timestamp = int(db.func.current_timestamp().property.columns[0].type.python_type().now().timestamp())
            filename = f"user_{user.id}_img_{timestamp}.png"
            img_path = os.path.join("generated_images", filename)
            
            # Ensure directory exists
            os.makedirs("generated_images", exist_ok=True)
            
            with open(img_path, 'wb') as f:
                f.write(image_data)
                
            # Save to UserImage table
            new_img = UserImage(user_id=user.id, filename=filename)
            db.session.add(new_img)
            db.session.commit()
            
            return jsonify({"status": "success", "message": "Image saved to gallery."})
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
            # Fetch new filesystem images
            new_images = UserImage.query.filter_by(user_id=user.id).order_by(UserImage.created_at.desc()).all()
            
            # Fetch videos
            videos = UserVideo.query.filter_by(user_id=user.id).order_by(UserVideo.created_at.desc()).all()
            
            return render_template('gallery.html', new_images=new_images, videos=videos, user=user)
    
    flash('Please log in to access the gallery.', 'warning')
    return redirect('/login')

@app.route('/delete_image', methods=['POST'])
def delete_image():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        image_id = request.form.get('image_id')
        
        if user and image_id:
            img = UserImage.query.filter_by(id=image_id, user_id=user.id).first()
            if img:
                # Delete file
                try:
                    os.remove(os.path.join("generated_images", img.filename))
                except:
                    pass
                db.session.delete(img)
                db.session.commit()
    return redirect('/gallery')

@app.route('/save_image_v2', methods=['POST'])
def save_image_v2():
    if 'email' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.json
    image_base64 = data.get('image_base64')
    if not image_base64:
        return jsonify({"status": "error", "message": "No image data"}), 400
    
    user = User.query.filter_by(email=session['email']).first()
    image_binary = base64.b64decode(image_base64)
    
    # Ensure directory exists
    os.makedirs("generated_images", exist_ok=True)
    
    # Generate filename
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_{user.id}_gen_{timestamp}.png"
    img_path = os.path.join("generated_images", filename)
    
    with open(img_path, 'wb') as f:
        f.write(image_binary)
        
    # Save to table
    new_img = UserImage(user_id=user.id, filename=filename)
    db.session.add(new_img)
    db.session.commit()
    
    return jsonify({"status": "success"})

@app.route('/delete_video', methods=['POST'])
def delete_video():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        video_id = request.form.get('video_id')
        if user and video_id:
            video = UserVideo.query.filter_by(id=video_id, user_id=user.id).first()
            if video:
                db.session.delete(video)
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


# Model Capabilities Mapping
MODEL_CAPABILITIES = {
    "gemini-3.1-flash-image-preview": {
        "supportsThinking": False,
        "supportsImages": True,
        "supportsTools": True,
        "supportsImageConfig": True
    },
    "gemini-2.0-flash": {
        "supportsThinking": False,
        "supportsImages": False,
        "supportsTools": True,
        "supportsImageConfig": False
    },
    "gemini-3.1-pro": {
        "supportsThinking": True,
        "supportsImages": False,
        "supportsTools": True,
        "supportsImageConfig": False
    }
}

@app.route('/generate_image_gemini', methods=['POST'])
def generate_image_gemini():
    try:
        if 'email' not in session:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
            
        data = request.json
        prompt = data.get('prompt')
        model = data.get('model', 'gemini-3.1-flash-image-preview')
        
        # Get Model Capabilities
        capabilities = MODEL_CAPABILITIES.get(model, {
            "supportsThinking": False,
            "supportsImages": True,
            "supportsTools": True,
            "supportsImageConfig": True
        })
        
        ratio = data.get('ratio', '1:1')
        size = data.get('size', '1K')
        
        # Tools / Grounding
        tools_config = data.get('tools', {})
        web_search = tools_config.get('webSearch', False)
        image_search = tools_config.get('imageSearch', False)
        
        # Thinking Config
        thinking = data.get('thinking', {})
        include_thoughts = thinking.get('includeThoughts', False)
        thinking_level = thinking.get('level', 'HIGH')
        
        # Multimodal Inputs
        ref_image = data.get('ref_image') # Base64
        
        user = User.query.filter_by(email=session['email']).first()
        if user.credits <= 0:
            return jsonify({"status": "error", "message": "Insufficient credits"}), 403
            
        user.credits -= 1
        db.session.commit()
        
        # 1. Construct contents[]
        parts = [{"text": prompt}]
        if ref_image and (capabilities["supportsImages"] or capabilities["supportsImageConfig"]):
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": ref_image
                }
            })
            
        payload = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "responseModalities": ["IMAGE"] if capabilities["supportsImageConfig"] else ["TEXT"]
            }
        }
        
        # 2. Add imageConfig if supported
        if capabilities["supportsImageConfig"]:
            payload["generationConfig"]["imageConfig"] = {
                "aspectRatio": ratio,
                "imageSize": size
            }
        
        # 3. Add Tools (Grounding) only if supported
        if capabilities["supportsTools"] and (web_search or image_search):
            search_types = {}
            if web_search: search_types["webSearch"] = {}
            if image_search: search_types["imageSearch"] = {}
            
            payload["tools"] = [{
                "google_search": {
                    "searchTypes": search_types
                }
            }]
        elif (web_search or image_search):
            print(f"WARNING: tools are not supported for model {model} and will be ignored.")
            
        # 4. Add Thinking Config only if supported
        if include_thoughts:
            if capabilities["supportsThinking"]:
                payload["thinkingConfig"] = {
                    "thinkingLevel": thinking_level,
                    "includeThoughts": True
                }
            else:
                print(f"WARNING: thinkingConfig is not supported for model {model} and will be ignored.")

        # Call Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        res = requests.post(url, json=payload)
        
        if res.status_code != 200:
            print(f"DEBUG: Gemini API Error: {res.text}")
            return jsonify({"status": "error", "message": f"API Error {res.status_code}"})
            
        result = res.json()
        
        # Extract Image from generateContent response
        candidates = result.get('candidates', [])
        if not candidates:
            return jsonify({"status": "error", "message": "Generation blocked or failed."})
            
        parts = candidates[0].get('content', {}).get('parts', [])
        image_base64 = None
        thoughts = None
        
        for part in parts:
            if 'inlineData' in part:
                image_base64 = part['inlineData'].get('data')
            if 'thought' in part:
                thoughts = part['thought']
                
        if not image_base64:
            return jsonify({"status": "error", "message": "No image data in response"})
            
        return jsonify({
            "status": "success",
            "image_base64": image_base64,
            "thoughts": thoughts
        })
        
    except Exception as e:
        print(f"DEBUG: Exception: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})
        
    except Exception as e:
        print(f"DEBUG: Exception in image gen: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

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
    data = request.get_json()
    prompt = data.get('prompt')
    aspect_ratio = data.get('aspect_ratio', '16:9')
    resolution = data.get('resolution', '720p')
    
    ref_image = data.get('ref_image')
    first_frame = data.get('first_frame')
    last_frame = data.get('last_frame')

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required"}), 400
    
    user = User.query.filter_by(email=session['email']).first()
    if user.credits <= 0:
        return jsonify({"status": "error", "message": "Insufficient credits"}), 403
    
    user.credits -= 1
    db.session.commit()

    # Construct Gemini Veo 3.1 Request
    instance = {"prompt": prompt}
    parameters = {
        "aspectRatio": aspect_ratio,
        "resolution": resolution
    }

    if ref_image:
        instance["referenceImages"] = [{
            "image": {"inlineData": {"mimeType": "image/png", "data": ref_image}},
            "referenceType": "asset"
        }]
    
    if first_frame:
        instance["image"] = {"inlineData": {"mimeType": "image/png", "data": first_frame}}
    
    if last_frame:
        parameters["lastFrame"] = {"inlineData": {"mimeType": "image/png", "data": last_frame}}

    payload = {
        "instances": [instance],
        "parameters": parameters
    }

    try:
        url = f"{BASE_URL}/models/{VEO_MODEL}:predictLongRunning?key={GEMINI_API_KEY}"
        response = requests.post(url, json=payload)
        
        print(f"DEBUG: Veo Predict Request Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"DEBUG: Veo Predict Error: {response.text}")
            return jsonify({"status": "error", "message": f"API Error {response.status_code}: {response.text}"}), 500

        res_data = response.json()
        print(f"DEBUG: Veo Predict Response: {res_data}")

        if "name" in res_data:
            return jsonify({
                "status": "success", 
                "operation_id": res_data["name"]
            })
        else:
            return jsonify({"status": "error", "message": res_data.get("error", {}).get("message", "API Error")}), 500

    except Exception as e:
        print(f"DEBUG: Exception in generate_video: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/video_status/<path:operation_id>')
def video_status(operation_id):
    try:
        url = f"{BASE_URL}/{operation_id}?key={GEMINI_API_KEY}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"DEBUG: Operation Status Error {response.status_code}: {response.text}")
            return jsonify({"status": "failed", "message": f"API Error {response.status_code}"})

        data = response.json()
        
        if data.get("done"):
            # Operation complete
            if "error" in data:
                return jsonify({"status": "failed", "message": data["error"]["message"]})
            
            # Extract video URI
            try:
                res = data.get("response", {})
                # Try all possible keys for the video samples
                samples = res.get("generateVideoResponse", {}).get("generatedSamples", [])
                if not samples:
                    samples = res.get("generatedVideos", [])
                if not samples:
                    samples = res.get("videoSamples", [])
                
                # Download the video
                # Check if URI already has parameters
                if not samples:
                    print(f"DEBUG: No samples found in response: {data}")
                    return jsonify({"status": "failed", "message": "No video samples in response"})

                video_uri = samples[0].get("video", {}).get("uri")
                
                # Download the video
                # Check if URI already has parameters
                sep = "&" if "?" in video_uri else "?"
                video_res = requests.get(f"{video_uri}{sep}key={GEMINI_API_KEY}", stream=True)
                
                if video_res.status_code != 200:
                    print(f"DEBUG: Video Download Error {video_res.status_code}: {video_res.text}")
                    return jsonify({"status": "failed", "message": f"Download Error {video_res.status_code}"})

                # Sanitize filename (replace slashes with underscores)
                safe_id = operation_id.replace('/', '_')
                video_filename = f"veo_{safe_id}.mp4"
                video_save_path = os.path.join(output_path, video_filename)
                
                with open(video_save_path, 'wb') as f:
                    for chunk in video_res.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Auto-save to database
                user = User.query.filter_by(email=session['email']).first()
                new_video = UserVideo(user_id=user.id, filename=video_filename)
                db.session.add(new_video)
                db.session.commit()

                return jsonify({
                    "status": "done", 
                    "video_url": f"/generated_videos/{video_filename}"
                })
            except Exception as e:
                print(f"DEBUG: Exception in status download: {str(e)}")
                return jsonify({"status": "failed", "message": f"Error downloading video: {str(e)}"})
        
        return jsonify({"status": "pending"})

    except Exception as e:
        print(f"DEBUG: Exception in video_status: {str(e)}")
        return jsonify({"status": "failed", "message": str(e)})


# Serve the generated video file
# Serve the generated video file (Secure)
@app.route('/generated_videos/<filename>')
def serve_video(filename):
    if 'email' not in session:
        return abort(401)
    
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return abort(401)
        
    # Verify ownership in database
    video = UserVideo.query.filter_by(user_id=user.id, filename=filename).first()
    if not video:
        return abort(403) # Forbidden
        
    return send_from_directory(output_path, filename)

# Serve the generated image file (Secure)
@app.route('/generated_images/<filename>')
def serve_image(filename):
    if 'email' not in session:
        return abort(401)
        
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return abort(401)
        
    # Verify ownership in database
    image = UserImage.query.filter_by(user_id=user.id, filename=filename).first()
    if not image:
        return abort(403) # Forbidden
        
    return send_from_directory('generated_images', filename)


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


@app.route('/start_portfolio')
def start_portfolio():
    # Path to the AI portfolio folder
    portfolio_folder_path = os.path.join(os.getcwd(), 'templates', 'WebsiteBuilder')

    try:
        # Run npm run dev inside WebsiteBuilder folder on localhost:3000
        subprocess.Popen(['npm', 'run', 'dev'], cwd=portfolio_folder_path, shell=True)
        # Optional: Redirect to portfolio URL
        return jsonify({
            "status": "success",
            "message": "AI Portfolio Generator started successfully.",
            "portfolio_url": "http://localhost:3000/generate-portfolio"
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
