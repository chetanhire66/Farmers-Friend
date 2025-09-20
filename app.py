from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from models import db, Farmer, Advisory
from config import Config
import utils
from Chatbot import gimini

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Farmer.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    location = request.form.get('location')
    land_size = request.form.get('land_size')
    preferred_crops = request.form.get('preferred_crops', '')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not all([name, mobile, location, land_size, password, confirm_password]):
        flash("Please fill all required fields.")
        return redirect(url_for('home'))

    if password != confirm_password:
        flash("Passwords do not match.")
        return redirect(url_for('home'))

    if Farmer.query.filter_by(mobile=mobile).first():
        flash("Mobile number already registered.")
        return redirect(url_for('home'))

    # Updated password hashing method
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    farmer = Farmer(
        name=name,
        mobile=mobile,
        location=location,
        land_size=float(land_size),
        preferred_crops=preferred_crops,
        password=hashed_password
    )
    db.session.add(farmer)
    db.session.commit()
    flash("Registration successful. Please login.")
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    user = Farmer.query.filter_by(mobile=mobile).first()
    if not user or not check_password_hash(user.password, password):
        flash("Invalid mobile number or password.")
        return redirect(url_for('home'))
    login_user(user)
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    weather = utils.get_weather(current_user.location)
    season = utils.get_season()
    soil_type = 'loamy'
    crop_recommendations = utils.recommend_crops(season, soil_type, weather)
    preferred_crops_list = [c.strip() for c in (current_user.preferred_crops or '').split(',') if c.strip()]
    crop_for_guidance = preferred_crops_list[0] if preferred_crops_list else crop_recommendations[0]
    fertilizer_guidance = utils.fertilizer_guidance(crop_for_guidance)
    pest_control_guidance = utils.pest_control_guidance(crop_for_guidance)
    return render_template('dashboard.html',
                           weather=weather,
                           crop_recommendations=crop_recommendations,
                           fertilizer_guidance=fertilizer_guidance,
                           pest_control_guidance=pest_control_guidance)

@app.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    data = request.get_json()
    user_message = data.get('message', '').lower() if data else ''
    if 'yellow leaves' in user_message or 'yellow leaf' in user_message:
        reply = utils.translate_text('yellow_leaves_response', 'en', load_lang('en'))
    else:
        reply = gimini(user_message)
    return jsonify({'reply': reply})

@app.route('/lang/<lang_code>')
def get_language_data(lang_code):
    if lang_code not in ['en', 'hi', 'mr']:
        lang_code = 'en'
    data = load_lang(lang_code)
    return jsonify(data)

def load_lang(lang_code):
    try:
        with open(f'static/lang/{lang_code}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

