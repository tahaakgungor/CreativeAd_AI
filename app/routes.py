import uuid
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from app.stable_diffusionize import generate_image
from app.create_ad_template import generate_dynamic_ad

bp = Blueprint("main", __name__)

# Bellekte geçici depolama alanı
temp_files = {}

# Define generated_image_path globally
generated_image_path = None

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/.netlify/functions/generate', methods=['POST'])
def generate():
    global generated_image_path

    try:
        # Gerekli bilgileri al
        uploaded_image = request.files['image']
        uploaded_logo = request.files['logo']
        user_id = str(uuid.uuid4())

        # Dosyayı bellekte geçici bir depolama alanına kaydet
        temp_files[user_id] = {
            'uploaded_image': uploaded_image.read(),
            'uploaded_logo': uploaded_logo.read()
        }

        # Kullanıcının girdiği prompt ve renk bilgilerini al
        prompt = request.form['prompt']
        color_hex = request.form['color']
        temp_data = temp_files.get(user_id)
        uploaded_image_content = temp_data['uploaded_image']


        generated_image_result = generate_image(uploaded_image_content, prompt, color_hex)
        generated_image_path = generated_image_result["output_image_path"]
        print(f"Generated image path: {generated_image_path}")

        # Diğer inputlardan gerekli değerleri al
        punchline = request.form['punchline']
        punchline_color = request.form['punchline_color']
        button_text = request.form['button_text']
        button_color = request.form['button_color']

        uploaded_logo_content = temp_data['uploaded_logo']

        output_ad_result = generate_dynamic_ad(
            generated_image_path, uploaded_logo_content, punchline, punchline_color, button_text, button_color
        )

        output_ad_path = output_ad_result["output_path"]

        return render_template('generate.html', generated_image_path=generated_image_path, ad_template_path=output_ad_path)

    except Exception as e:
        print(f"Error in generate route: {str(e)}")
        return {"message": f"Error: {str(e)}"}, 400
