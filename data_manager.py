# data_manager.py
import csv
import os
import datetime
from models import User, Post, Like

def ensure_data_directory_exists():
    """
    데이터 파일을 저장할 'data' 디렉토리가 없으면 생성합니다.
    """
    if not os.path.exists('data'):
        os.makedirs('data')

# 데이터 저장 함수들
def save_data_User(users):
    """
    User 객체 리스트를 CSV 파일에 저장합니다.
    """
    ensure_data_directory_exists()
    with open('data/users.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "username", "password"])
        for user in users:
            writer.writerow([user.user_id, user.username, user.password])

def save_data_Post(posts):
    """
    Post 객체 리스트를 CSV 파일에 저장합니다.
    """
    ensure_data_directory_exists()
    with open('data/posts.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['post_id', 'user_id', 'content', 'timestamp', 'is_retweet', 'original_post_id'])
        for post in posts:
            writer.writerow([post.post_id, post.user_id, post.content, post.timestamp.isoformat(), post.is_retweet, post.original_post_id])

def save_data_Like(likes):
    """
    Like 객체 리스트를 CSV 파일에 저장합니다.
    """
    ensure_data_directory_exists()
    with open('data/likes.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['like_id', 'post_id', 'user_id', 'timestamp'])
        for like in likes:
            writer.writerow([like.like_id, like.post_id, like.user_id, like.timestamp.isoformat()])

# 데이터 로드 함수들
def load_data_User():
    """
    CSV 파일에서 User 객체 리스트를 불러옵니다. 파일이 없으면 빈 리스트를 반환합니다.
    """
    users = []
    if not os.path.exists('data/users.csv'):
        return users
    try:
        with open('data/users.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = User(user_id=int(row["user_id"]), username=row["username"], password=row["password"])
                users.append(user)
    except (FileNotFoundError, KeyError):
        print("경고: 'data/users.csv' 파일이 없어 빈 사용자 목록을 로드합니다.")
    return users

def load_data_Post():
    """
    CSV 파일에서 Post 객체 리스트를 불러옵니다. 파일이 없으면 빈 리스트를 반환합니다.
    """
    posts = []
    if not os.path.exists('data/posts.csv'):
        return posts
    try:
        with open('data/posts.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                is_retweet_bool = row['is_retweet'].lower() == 'true'
                original_post_id_val = int(row['original_post_id']) if row.get('original_post_id') and row['original_post_id'].isdigit() else None
                post = Post(post_id=int(row["post_id"]), user_id=int(row["user_id"]), content=row["content"], 
                            timestamp=datetime.datetime.fromisoformat(row['timestamp']), is_retweet=is_retweet_bool,
                            original_post_id=original_post_id_val)
                posts.append(post)
    except (FileNotFoundError, KeyError):
        print("경고: 'data/posts.csv' 파일이 없어 빈 게시글 목록을 로드합니다.")
    return posts

def load_data_Like():
    """
    CSV 파일에서 Like 객체 리스트를 불러옵니다. 파일이 없으면 빈 리스트를 반환합니다.
    """
    likes = []
    if not os.path.exists('data/likes.csv'):
        return likes
    try:
        with open('data/likes.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                like = Like(like_id=int(row["like_id"]), post_id=int(row["post_id"]), user_id=int(row["user_id"]), timestamp=datetime.datetime.fromisoformat(row['timestamp']))
                likes.append(like)
    except (FileNotFoundError, KeyError):
        print("경고: 'data/likes.csv' 파일이 없어 빈 좋아요 목록을 로드합니다.")
    return likes