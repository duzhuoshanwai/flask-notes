from flask import Flask, render_template, request, redirect, url_for, abort, make_response
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import jwt
from functools import wraps
from flask_wtf.csrf import CSRFProtect

from services.note_service import NoteService
from services.auth_service import AuthService


load_dotenv()
DB_PATH = os.environ.get("DATABASE_PATH", "database.db")
APP_URL = os.environ.get("APP_URL", "http://127.0.0.1:5000")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback_secret")
csrf = CSRFProtect(app)
note_service = NoteService(DB_PATH)

oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.environ.get('GITHUB_CLIENT_ID'),
    client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

def login_required(func):
    """保护路由的装饰器"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt_token')
        if not token:
            return redirect(url_for('login'))
        try:
            # 验证 JWT Token
            auth_service = AuthService()
            auth_service.verify_token(token)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/github-login', methods=['GET'])
def github_login():
    redirect_uri = f'{APP_URL}/auth/github/callback'
    return oauth.github.authorize_redirect(redirect_uri)

@app.route('/auth/github/callback', methods=['GET'])
def callback():
    oauth.github.authorize_access_token()
    user_info = oauth.github.get('user').json()
    
    # 检查用户是否在 ADMIN_ID 列表中
    admin_ids = os.environ.get('ADMIN_ID', '').split(',')
    if user_info.get('login') not in admin_ids:
        return redirect(request.referrer or url_for('index'))  # 跳转回上一个页面或首页

    # 生成 JWT 并存入 Cookie
    auth_service = AuthService()
    token = auth_service.generate_token(user_info)
    response = make_response(redirect(url_for('index')))
    response.set_cookie('jwt_token', token, httponly=True, secure=True, max_age=86400)  # 24小时过期
    return response

@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('jwt_token', '', expires=0)
    return response

@app.route("/static/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)


@app.route("/")
def index():
    notes = note_service.get_notes(page=1)
    total_notes = note_service.get_total_notes()
    total_pages = (total_notes + 10 - 1) // 10  # 假设每页10条
    return render_template("index.html", notes=notes, page=1, total_pages=total_pages)

@app.route("/page/<int:page>")
def page(page):
    notes = note_service.get_notes(page=page)
    total_notes = note_service.get_total_notes()
    total_pages = (total_notes + 10 - 1) // 10  # 假设每页10条
    return render_template("index.html", notes=notes, page=page, total_pages=total_pages)


@app.route("/<string:id>")
def note_detail(id):
    note = note_service.get_note_by_id(id, md_type=False)
    if not note:
        abort(404)
    return render_template("detail.html", note=note)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content and note_service.create_note(title, content):
            return redirect(url_for("index"))
    return render_template(
        "edit.html",
        action_title="创建新笔记",
        action_url=url_for("create"),
        submit_button="保存",
    )


@app.route("/<string:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content and note_service.update_note(id, title, content):
            return redirect(url_for("index"))

    note = note_service.get_note_by_id(id, md_type=True)
    if not note:
        abort(404)
    return render_template(
        "edit.html",
        action_title="编辑笔记",
        action_url=url_for("update", id=id),
        submit_button="更新",
        note=note,
    )