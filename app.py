import os
import csv
from io import StringIO
from datetime import datetime, timedelta

from flask import (
    Flask, render_template, redirect, url_for, 
    flash, request, Response, session, jsonify
)
from flask_login import (
    LoginManager, login_user, logout_user, 
    login_required, current_user
)
from flask_login.mixins import AnonymousUserMixin
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

from config import Config
from models import db, User, Complaint, Notice
from forms import LoginForm, RegisterForm, ComplaintForm, AddOfficerForm, NoticeForm

# =====================================================
# APPLICATION SETUP
# =====================================================

app = Flask(__name__)
app.config.from_object(Config)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='vaibhavbobade84@gmail.com',
    MAIL_PASSWORD='shaqdufntnfyxkpc',
    MAIL_DEFAULT_SENDER='vaibhavbobade84@gmail.com'
)

mail = Mail(app)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

# =====================================================
# TRANSLATIONS (Expanded for all features)
# =====================================================

TRANSLATIONS = {
    'en': {
        'welcome': 'Welcome to Shelgaon Gram Panchayat',
        'subtitle': 'Online complaint registration and efficient ward management.',
        'login': 'Login',
        'label_username': 'Username',
        'label_password': 'Password',
        'label_username_placeholder': 'Enter your username',
        'forgot_pw': 'Forgot Password?',
        'no_account': "Don't have an account?",
        'reg_link': 'Create Account',
        'btn_submit': 'Submit',
        'btn_send_link': 'Send Reset Link',
        'reset_msg': 'If account exists, a reset link has been sent to your email.',
        'status_pending': 'Pending',
        'status_in_progress': 'In Progress',
        'status_resolved': 'Resolved',
        'label_officers': 'Officers',
        'label_citizens': 'Citizens',
        'label_complaints_total': 'Total Complaints',
        'admin_dash': 'Admin Dashboard',
        'admin_subtitle': 'Manage complaints, officers & citizens efficiently',
        'officer_dash': 'Officer Dashboard',
        'officer_subtitle': 'Track and update assigned complaints',
        'nav_lang': 'Language',
        'logout': 'Logout',
        'register': 'Register',
        'my_complaints': 'My Complaints',
        'track_subtitle': 'Track your complaints and submit new ones',
        'comp_head': 'Register New Complaint',
        'history_head': 'Complaints History',
        'label_citizen': 'Citizen',
        'label_name': 'Full Name',
        'label_email': 'Email Address',
        'label_cat': 'Category',
        'label_ward': 'Ward Number',
        'label_ward_short': 'Ward',
        'label_desc': 'Description',
        'label_photo': 'Photo (Optional)',
        'label_photo_short': 'Photo',
        'label_status': 'Status',
        'label_date': 'Date',
        'label_action': 'Action',
        'btn_register': 'Create Account',
        'btn_reset': 'Reset',
        'btn_add': 'Add',
        'btn_view_complaints': 'View Complaints',
        'btn_filter': 'Filter',
        'btn_export': 'CSV Export',
        'btn_update': 'Update Status',
        'btn_delete': 'Delete',
        'no_complaints': 'No Complaints Found',
        'no_officers': 'No officers yet',
        'no_citizens': 'No citizens registered',
        'no_photo': 'No Photo',
        'all_cats': 'All Categories',
        'filter_title': 'Search & Filter',
        'filter_today': 'Today',
        'filter_week': 'Week',
        'filter_month': 'Month',
        'filter_all': 'All',
        'assigned_tasks': 'Assigned Tasks',
        'total_label': 'Total',
        'confirm_delete': 'Are you sure you want to delete?',
        'modal_add_officer': 'Add New Officer',
        'cat_water_supply': 'Water Supply',
        'cat_roads': 'Roads',
        'cat_sanitation': 'Sanitation',
        'cat_street_lights': 'Street Lights',
        'cat_electricity': 'Electricity',
        'cat_others': 'Others',
        'notice_board': 'Notice Board'
    },
    'hi': {
        'welcome': 'शेलगांव ग्राम पंचायत में आपका स्वागत है',
        'subtitle': 'ऑनलाइन शिकायत पंजीकरण और कुशल वार्ड प्रबंधन।',
        'login': 'लॉगिन',
        'label_username': 'उपयोगकर्ता नाम',
        'label_password': 'पासवर्ड',
        'label_username_placeholder': 'अपना उपयोगकर्ता नाम दर्ज करें',
        'forgot_pw': 'पासवर्ड भूल गए?',
        'no_account': 'क्या आपका खाता नहीं है?',
        'reg_link': 'नया खाता बनाएँ',
        'btn_submit': 'जमा करें',
        'btn_send_link': 'रीसेट लिंक भेजें',
        'reset_msg': 'यदि खाता मौजूद है, तो ईमेल पर लिंक भेज दिया गया है।',
        'status_pending': 'लंबित',
        'status_in_progress': 'प्रगति पर',
        'status_resolved': 'हल किया गया',
        'label_officers': 'अधिकारी',
        'label_citizens': 'नागरिक',
        'label_complaints_total': 'कुल शिकायतें',
        'admin_dash': 'एडमिन डैशबोर्ड',
        'admin_subtitle': 'शिकायतों, अधिकारियों और नागरिकों का प्रबंधन करें',
        'officer_dash': 'अधिकारी डैशबोर्ड',
        'officer_subtitle': 'सौंपी गई शिकायतों को ट्रैक और अपडेट करें',
        'nav_lang': 'भाषा',
        'logout': 'लॉगआउट',
        'register': 'पंजीकरण',
        'my_complaints': 'मेरी शिकायतें',
        'track_subtitle': 'अपनी शिकायतों को ट्रैक करें और नई सबमिट करें',
        'comp_head': 'नई शिकायत दर्ज करें',
        'history_head': 'शिकायत इतिहास',
        'label_citizen': 'नागरिक',
        'label_name': 'पूरा नाम',
        'label_email': 'ईमेल पता',
        'label_cat': 'श्रेणी',
        'label_ward': 'वॉर्ड नंबर',
        'label_ward_short': 'वॉर्ड',
        'label_desc': 'विवरण',
        'label_photo': 'फोटो (वैकल्पिक)',
        'label_photo_short': 'फोटो',
        'label_status': 'स्थिति',
        'label_date': 'दिनांक',
        'label_action': 'कार्रवाई',
        'btn_register': 'खाता बनाएं',
        'btn_reset': 'रीसेट',
        'btn_add': 'जोड़ें',
        'btn_view_complaints': 'शिकायतें देखें',
        'btn_filter': 'फिल्टर',
        'btn_export': 'CSV एक्सपोर्ट',
        'btn_update': 'स्थिति अपडेट करें',
        'btn_delete': 'हटाएं',
        'no_complaints': 'कोई शिकायत नहीं मिली',
        'no_officers': 'कोई अधिकारी नहीं',
        'no_citizens': 'कोई नागरिक नहीं',
        'no_photo': 'फोटो नहीं',
        'all_cats': 'सभी श्रेणियां',
        'filter_title': 'खोजें और फ़िल्टर करें',
        'filter_today': 'आज',
        'filter_week': 'इस सप्ताह',
        'filter_month': 'इस महीने',
        'filter_all': 'सभी',
        'assigned_tasks': 'सौंपे गए कार्य',
        'total_label': 'कुल',
        'confirm_delete': 'क्या आप वाकई हटाना चाहते हैं?',
        'modal_add_officer': 'नया अधिकारी जोड़ें',
        'cat_water_supply': 'जल आपूर्ति',
        'cat_roads': 'सड़कें',
        'cat_sanitation': 'स्वच्छता',
        'cat_street_lights': 'स्ट्रीट लाइट',
        'cat_electricity': 'बिजली',
        'cat_others': 'अन्य',
        'notice_board': 'सूचना पटल'
    },
    'mr': {
        'welcome': 'शेलगाव ग्रामपंचायत मध्ये आपले स्वागत आहे',
        'subtitle': 'ऑनलाइन तक्रार नोंदणी आणि कार्यक्षम वॉर्ड व्यवस्थापन.',
        'login': 'लॉगिन',
        'label_username': 'वापरकर्ता नाव',
        'label_password': 'पासवर्ड',
        'label_username_placeholder': 'तुमचे वापरकर्ता नाव प्रविष्ट करा',
        'forgot_pw': 'पासवर्ड विसरलात?',
        'no_account': 'तुमचे खाते नाही का?',
        'reg_link': 'नवीन खाते तयार करा',
        'btn_submit': 'सादर करा',
        'btn_send_link': 'रीसेट लिंक पाठवा',
        'reset_msg': 'खाते असल्यास, तुमच्या ईमेलवर लिंक पाठविली आहे.',
        'status_pending': 'प्रलंबित',
        'status_in_progress': 'प्रगतीपथावर',
        'status_resolved': 'निकाली काढले',
        'label_officers': 'अधिकारी',
        'label_citizens': 'नागरिक',
        'label_complaints_total': 'एकूण तक्रारी',
        'admin_dash': 'प्रशासक डॅशबोर्ड',
        'admin_subtitle': 'तक्रारी, अधिकारी आणि नागरिकांचे कार्यक्षमतेने व्यवस्थापन करा',
        'officer_dash': 'अधिकारी डॅशबोर्ड',
        'officer_subtitle': 'नियुक्त तक्रारींचा मागोवा घ्या आणि अपडेट करा',
        'nav_lang': 'भाषा',
        'logout': 'बाहेर पडा',
        'register': 'नोंदणी',
        'my_complaints': 'माझ्या तक्रारी',
        'track_subtitle': 'तुमच्या तक्रारींचा मागोवा घ्या आणि नवीन तक्रार करा',
        'comp_head': 'नवीन तक्रार नोंदवा',
        'history_head': 'तक्रार इतिहास',
        'label_citizen': 'नागरिक',
        'label_name': 'पूर्ण नाव',
        'label_email': 'ईमेल पत्ता',
        'label_cat': 'श्रेणी',
        'label_ward': 'वॉर्ड क्रमांक',
        'label_ward_short': 'वॉर्ड',
        'label_desc': 'तपशील',
        'label_photo': 'फोटो (पर्यायी)',
        'label_photo_short': 'फोटो',
        'label_status': 'स्थिती',
        'label_date': 'दिनांक',
        'label_action': 'कृती',
        'btn_register': 'खाते तयार करा',
        'btn_reset': 'रीसेट',
        'btn_add': 'जोडा',
        'btn_view_complaints': 'तक्रारी पहा',
        'btn_filter': 'फिल्टर करा',
        'btn_export': 'CSV एक्सपोर्ट',
        'btn_update': 'स्थिती बदला',
        'btn_delete': 'हटवा',
        'no_complaints': 'तक्रारी आढळल्या नाहीत',
        'no_officers': 'अद्याप कोणतेही अधिकारी नाहीत',
        'no_citizens': 'अद्याप कोणतेही नागरिक नाहीत',
        'no_photo': 'फोटो नाही',
        'all_cats': 'सर्व श्रेणी',
        'filter_title': 'शोधा आणि फिल्टर करा',
        'filter_today': 'आज',
        'filter_week': 'या आठवड्यात',
        'filter_month': 'या महिन्यात',
        'filter_all': 'सर्व',
        'assigned_tasks': 'नियुक्त तक्रारी',
        'total_label': 'एकूण',
        'confirm_delete': 'तुम्हाला खात्री आहे की तुम्ही हटवू इच्छिता?',
        'modal_add_officer': 'नवीन अधिकारी जोडा',
        'cat_water_supply': 'पाणी पुरवठा',
        'cat_roads': 'रस्ते',
        'cat_sanitation': 'स्वच्छता',
        'cat_street_lights': 'पथदिवे',
        'cat_electricity': 'वीज पुरवठा',
        'cat_others': 'इतर',
        'notice_board': 'सूचना फलक'
    }
}

# =====================================================
# HELPERS
# =====================================================

def send_resolution_email(citizen_email, complaint):
    now_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    lang = session.get('lang', 'en')
    msg = Message(f"Complaint #{complaint.id} RESOLVED", recipients=[citizen_email])
    
    if lang == 'mr':
        msg.body = (f"नमस्ते,\n\nतुमची तक्रार (ID: #{complaint.id}) यशस्वीरित्या सोडवण्यात आली आहे.\n\n"
                    f"तपशील:\nसमस्या: {complaint.category}\nवेळ: {now_str}\n\n"
                    f"तुम्ही डॅशबोर्डवर कामाचा फोटो पाहू शकता.\n\nधन्यवाद,\nशेलगाव ग्रामपंचायत")
    elif lang == 'hi':
        msg.body = (f"नमस्ते,\n\nआपकी शिकायत (ID: #{complaint.id}) का समाधान कर दिया गया है।\n\n"
                    f"विवरण:\nशिकायत: {complaint.category}\nसमय: {now_str}\n\n"
                    f"आप डैशबोर्ड पर फोटो देख सकते हैं।\n\nधन्यवाद,\nशेलगांव ग्रामपंचायत")
    else:
        msg.body = (f"Namaste,\n\nYour complaint (ID: #{complaint.id}) has been resolved.\n\n"
                    f"Details:\nIssue: {complaint.category}\nTime: {now_str}\n\n"
                    f"Check dashboard for resolution photo.\n\nRegards,\nShelgaon GP Team")

    try:
        mail.send(msg)
    except Exception as e:
        print(f"Email Error: {e}")

@app.context_processor
def inject_global_data():
    selected_lang = session.get('lang', 'en')
    return {
        'lang': TRANSLATIONS.get(selected_lang, TRANSLATIONS['en']),
        'current_lang': selected_lang
    }

# =====================================================
# LOGIN MANAGER
# =====================================================

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class AnonymousUser(AnonymousUserMixin):
    role = None

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def redirect_by_role():
    if current_user.role == 'admin':
        return redirect(url_for('admin_panel'))
    elif current_user.role == 'officer':
        return redirect(url_for('officer_panel'))
    return redirect(url_for('dashboard'))

# =====================================================
# CORE ROUTES
# =====================================================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect_by_role()
    notices = Notice.query.order_by(Notice.date_posted.desc()).limit(5).all()
    return render_template('index.html', notices=notices)

@app.route('/track_status')
def track_status():
    complaint_id = request.args.get('complaint_id')
    if not complaint_id:
        flash('Please enter a complaint ID', 'warning')
        return redirect(url_for('index'))
    
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        flash(f'No complaint found with ID: {complaint_id}', 'danger')
        return redirect(url_for('index'))
        
    return render_template('track_status.html', complaint=complaint)

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    if lang_code in ['en', 'hi', 'mr']:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_by_role()
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.role == form.role.data:
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect_by_role()
        flash('Invalid credentials or role', 'danger')
    return render_template('login.html', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        flash(inject_global_data()['lang']['reset_msg'], 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('User already exists', 'danger')
        else:
            user = User(name=form.name.data, username=form.username.data, email=form.email.data, role='citizen')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role != 'citizen':
        return redirect_by_role()
    
    form = ComplaintForm()
    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename) if file else None
        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        comp = Complaint(
            category=form.category.data, 
            ward_no=form.ward_no.data, 
            description=form.description.data, 
            photo=filename, 
            user_id=current_user.id
        )
        db.session.add(comp)
        db.session.commit()
        flash('Complaint submitted!', 'success')
        return redirect(url_for('dashboard'))
    
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('dashboard.html', form=form, complaints=complaints)

# =====================================================
# OFFICER PANEL
# =====================================================

@app.route('/officer')
@login_required
def officer_panel():
    if current_user.role != 'officer':
        return redirect_by_role()
    
    query = Complaint.query
    ward = request.args.get('ward')
    if ward:
        query = query.filter_by(ward_no=ward)
    cat = request.args.get('category')
    if cat:
        query = query.filter_by(category=cat)
    
    pending = query.filter_by(status='Pending').all()
    for c in pending:
        c.status = 'In Progress'
    if pending:
        db.session.commit()

    complaints = query.order_by(Complaint.created_at.desc()).all()
    stats = {
        'pending': Complaint.query.filter_by(status='Pending').count(),
        'in_progress': Complaint.query.filter_by(status='In Progress').count(),
        'resolved': Complaint.query.filter_by(status='Resolved').count()
    }
    
    return render_template('officer.html', complaints=complaints, stats=stats, now=datetime.utcnow())

@app.route('/officer/export_csv')
@login_required
def officer_export_csv():
    if current_user.role != 'officer':
        return redirect_by_role()
    
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Citizen', 'Category', 'Ward', 'Status', 'Date'])
    for c in complaints:
        cw.writerow([c.id, c.user.name, c.category, c.ward_no, c.status, c.created_at])
    
    return Response(
        si.getvalue(), 
        mimetype="text/csv", 
        headers={"Content-disposition": "attachment; filename=officer_complaints.csv"}
    )

@app.route('/resolve_complaint/<int:id>', methods=['POST'])
@login_required
def resolve_complaint(id):
    if current_user.role != 'officer':
        return redirect_by_role()
    
    comp = Complaint.query.get_or_404(id)
    file = request.files.get('resolution_photo')
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        comp.resolution_photo = filename
        comp.status = 'Resolved'
        comp.resolved_at = datetime.utcnow()
        db.session.commit()
        send_resolution_email(comp.user.email, comp)
        flash('Resolved and Citizen Notified!', 'success')
    else:
        flash('Please upload a resolution photo.', 'warning')
    return redirect(url_for('officer_panel'))

# =====================================================
# ADMIN PANEL FUNCTIONS
# =====================================================

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        return redirect_by_role()
    
    db.session.expire_all()
    now = datetime.utcnow()
    today_date = now.date()
    
    query = Complaint.query
    ward = request.args.get('ward')
    if ward:
        query = query.filter_by(ward_no=ward)
    cat = request.args.get('category')
    if cat:
        query = query.filter_by(category=cat)

    comp_list = query.order_by(Complaint.created_at.desc()).all()
    off_list = User.query.filter_by(role='officer').all()
    cit_list = User.query.filter_by(role='citizen').all()
    
    feedback_list = Complaint.query.filter(Complaint.feedback_rating.isnot(None)).order_by(Complaint.created_at.desc()).all()
    
    stats = {
        'total': len(comp_list),
        'today': Complaint.query.filter(db.func.date(Complaint.created_at) == today_date).count(),
        'week': Complaint.query.filter(Complaint.created_at >= now - timedelta(days=7)).count(),
        'month': Complaint.query.filter(Complaint.created_at >= now - timedelta(days=30)).count(),
        'officers_count': len(off_list),
        'citizens_count': len(cit_list)
    }

    if request.args.get('export') == 'csv':
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['ID', 'Citizen', 'Category', 'Ward', 'Status', 'Date', 'Rating', 'Feedback'])
        for c in comp_list:
            cw.writerow([c.id, c.user.name if c.user else 'N/A', c.category, c.ward_no, c.status, c.created_at, c.feedback_rating or '', c.feedback_msg or ''])
        return Response(si.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=admin_complaints.csv"})

    return render_template(
        'admin.html', 
        complaints=comp_list, 
        officers=off_list, 
        citizens=cit_list,
        feedbacks=feedback_list, 
        notices=Notice.query.all(), 
        stats=stats,
        now=now,
        total_officers=len(off_list), 
        total_citizens=len(cit_list), 
        total_complaints=len(comp_list), 
        pending_complaints=Complaint.query.filter_by(status='Pending').count(),
        add_officer_form=AddOfficerForm(), 
        notice_form=NoticeForm(),
        period_filter=request.args.get('period', 'all')
    )

@app.route('/update_status/<int:id>/<string:status>')
@login_required
def update_status(id, status):
    if current_user.role != 'admin':
        return redirect_by_role()
    complaint = Complaint.query.get_or_404(id)
    complaint.status = status
    db.session.commit()
    flash(f'Status updated to {status}!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/add_notice', methods=['POST'])
@login_required
def add_notice():
    form = NoticeForm()
    if form.validate_on_submit():
        db.session.add(Notice(title=form.title.data, content=form.content.data))
        db.session.commit()
        flash('Notice Added!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/add_officer', methods=['POST'])
@login_required
def add_officer():
    form = AddOfficerForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Officer Added!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_officer/<int:officer_id>', methods=['POST'])
@login_required
def delete_officer(officer_id):
    if current_user.role != 'admin':
        return redirect_by_role()
    officer = User.query.get_or_404(officer_id)
    if officer.role != 'admin':
        db.session.delete(officer)
        db.session.commit()
        flash('Officer deleted!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/delete_complaint/<int:complaint_id>', methods=['POST'])
@login_required
def delete_complaint(complaint_id):
    if current_user.role == 'admin':
        db.session.delete(Complaint.query.get_or_404(complaint_id))
        db.session.commit()
        flash('Complaint Deleted!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
@login_required
def delete_feedback(feedback_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    complaint = Complaint.query.get_or_404(feedback_id)
    complaint.feedback_msg = None
    complaint.feedback_rating = None
    db.session.commit()
    flash('Feedback removed successfully', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    complaint_id = request.form.get('complaint_id')
    rating = request.form.get('rating')
    message = request.form.get('message')
    complaint = Complaint.query.get_or_404(complaint_id)
    if complaint.user_id == current_user.id and complaint.status == 'Resolved':
        complaint.feedback_rating = int(rating) if rating else None
        complaint.feedback_msg = message
        db.session.commit()
        flash('Thank you for feedback!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', name='Admin', email='admin@shelgaon.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)