# app.py
# git

from flask import Flask, render_template, request, redirect, url_for, session, g
from models import User, Post, Like
from data_manager import (
    save_data_Like, save_data_Post, save_data_User,
    load_data_Like, load_data_Post, load_data_User
)
from auth import auth_bp
import datetime
import os

# Flask 애플리케이션을 초기화합니다.
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_and_complex_key_that_no_one_can_guess')
app.register_blueprint(auth_bp)
# 커밋111
@app.before_request
def load_logged_in_user():
    """
    각 요청 전에 실행되어 현재 로그인한 사용자 ID를 전역(g) 객체에 저장합니다.
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        users_data = load_data_User()
        g.user = next((u for u in users_data if u.user_id == user_id), None)

@app.route('/')
def index():
    """
    메인 피드 페이지를 렌더링합니다.
    로그인하지 않은 경우 로그인 페이지로 리디렉션합니다.
    """
    if g.user is None:
        return redirect(url_for('auth.login'))

    posts_data = load_data_Post()
    users_data = load_data_User()
    likes_data = load_data_Like()

    # 게시글 데이터를 최신순으로 정렬
    posts_data.sort(key=lambda x: x.timestamp, reverse=True)

    # 게시글에 작성자 이름과 좋아요 수를 추가합니다.
    posts = []
    for post in posts_data:
        # 작성자 찾기
        username = next((u.username for u in users_data if u.user_id == post.user_id), '알 수 없음')
        
        # 좋아요 수 계산
        like_count = len([l for l in likes_data if l.post_id == post.post_id])

        # 리트윗인 경우 원본 게시글 정보를 찾습니다.
        original_post_username = None
        if post.is_retweet and post.original_post_id:
            original_post = next((p for p in posts_data if p.post_id == post.original_post_id), None)
            if original_post:
                original_post_username = next((u.username for u in users_data if u.user_id == original_post.user_id), '알 수 없음')
        
        posts.append({
            'post_id': post.post_id,
            'user_id': post.user_id,
            'username': username,
            'content': post.content,
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M'),
            'like_count': like_count,
            'is_retweet': post.is_retweet,
            'original_post_username': original_post_username
        })
    return render_template('index.html', posts=posts)


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    """
    새 게시글을 작성하는 페이지를 처리합니다.
    """
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        content = request.form['content']
        posts_data = load_data_Post()
        new_post_id = len(posts_data) + 1
        new_post = Post(post_id=new_post_id, user_id=g.user.user_id, content=content, timestamp=datetime.datetime.now())
        posts_data.append(new_post)
        save_data_Post(posts_data)
        return redirect(url_for('index'))
    return render_template('create_post.html')


@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """
    게시글에 좋아요를 처리합니다.
    """
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    likes_data = load_data_Like()
    user_id = g.user.user_id

    # 이미 좋아요를 눌렀는지 확인
    existing_like = next((l for l in likes_data if l.post_id == post_id and l.user_id == user_id), None)

    if existing_like:
        # 이미 좋아요를 눌렀으면 좋아요 취소
        likes_data.remove(existing_like)
    else:
        # 새로운 좋아요 객체를 생성하고 저장
        new_like_id = len(likes_data) + 1
        new_like = Like(like_id=new_like_id, post_id=post_id, user_id=user_id, timestamp=datetime.datetime.now())
        likes_data.append(new_like)
    
    save_data_Like(likes_data)
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/retweet/<int:post_id>', methods=['POST'])
def retweet_post(post_id):
    """
    특정 게시글을 리트윗하는 기능을 처리합니다.
    """
    if g.user is None:
        return redirect(url_for('auth.login'))

    posts_data = load_data_Post()
    original_post = next((p for p in posts_data if p.post_id == post_id), None)

    if original_post:
        user_id = g.user.user_id
        new_post_id = len(posts_data) + 1
        
        # 리트윗 게시글 내용 생성
        # 원본 게시글의 작성자 이름을 가져와서 'RT @username: content' 형식으로 만듭니다.
        users_data = load_data_User()
        original_username = next((u.username for u in users_data if u.user_id == original_post.user_id), '알 수 없음')
        retweet_content = f"RT @{original_username}: {original_post.content}"
        
        timestamp = datetime.datetime.now()

        new_post = Post(post_id=new_post_id, user_id=user_id, content=retweet_content, timestamp=timestamp, is_retweet=True, original_post_id=original_post.post_id)
        posts_data.append(new_post)
        save_data_Post(posts_data)
    
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    """
    특정 게시글을 보여주는 페이지를 렌더링합니다.
    """
    if g.user is None:
        return redirect(url_for('auth.login'))

    posts_data = load_data_Post()
    users_data = load_data_User()
    likes_data = load_data_Like()
    
    # post_id와 일치하는 게시글을 찾습니다.
    post = next((p for p in posts_data if p.post_id == post_id), None)

    if post:
        # 게시글 작성자 찾기
        username = next((u.username for u in users_data if u.user_id == post.user_id), '알 수 없음')
        
        # 좋아요 수 계산
        like_count = len([l for l in likes_data if l.post_id == post_id])

        # 현재 사용자가 이 게시글에 좋아요를 눌렀는지 확인
        is_liked = any(l.post_id == post_id and l.user_id == g.user.user_id for l in likes_data)

        # 템플릿에 전달할 데이터 구성
        post_data = {
            'post_id': post.post_id,
            'user_id': post.user_id,
            'username': username,
            'content': post.content,
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M'),
            'like_count': like_count,
            'is_liked': is_liked,
            'is_retweet': post.is_retweet,
            'original_post_id': post.original_post_id
        }
        return render_template('view_post.html', post=post_data)
    else:
        return "게시글을 찾을 수 없습니다.", 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)