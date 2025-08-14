# auth.py
from flask import Blueprint, render_template, redirect, url_for, request, session, g
from data_manager import save_data_User, load_data_User
from models import User
import os

# Blueprint를 생성하여 인증 관련 라우트를 관리합니다.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    회원가입 페이지를 처리합니다.
    GET 요청: 회원가입 폼을 렌더링합니다.
    POST 요청: 회원가입 정보를 처리하고 로그인 페이지로 리디렉션합니다.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users_data = load_data_User()
        
        # 새로운 사용자 ID를 생성합니다.
        new_user_id = len(users_data) + 1
        
        # 새로운 사용자 객체를 생성합니다.
        new_user = User(user_id=new_user_id, username=username, password=password)
        
        # 기존 사용자 데이터 리스트에 새로운 사용자 추가
        users_data.append(new_user)
        
        # 전체 사용자 리스트를 저장합니다.
        save_data_User(users_data)
        
        # 회원가입 후 로그인 페이지로 이동합니다.
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    로그인 페이지를 처리합니다.
    GET 요청: 로그인 폼을 렌더링합니다.
    POST 요청: 로그인 정보를 확인하고 메인 페이지로 리디렉션합니다.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users_data = load_data_User()
        
        # 사용자 이름과 비밀번호가 일치하는 사용자를 찾습니다.
        user = next((u for u in users_data if u.username == username and u.password == password), None)
        
        if user:
            # 로그인 성공 시 세션에 user_id를 저장하고 메인 페이지로 리디렉션합니다.
            session['user_id'] = user.user_id
            return redirect(url_for('index'))
        else:
            # 로그인 실패 시 오류 메시지를 포함하여 로그인 페이지로 리디렉션합니다.
            return render_template('login.html', error="Invalid username or password")
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """
    로그아웃 기능을 처리합니다.
    세션에서 user_id를 제거하고 메인 페이지로 리디렉션합니다.
    """
    session.pop('user_id', None)
    return redirect(url_for('index'))