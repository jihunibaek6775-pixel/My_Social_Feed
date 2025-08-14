# models.py
import datetime

class User:
    """
    사용자 정보를 담는 클래스입니다.
    """
    def __init__(self, user_id, username, password):
        self.user_id = user_id       # 고유 사용자 ID
        self.username = username     # 사용자 이름 (로그인 ID 역할)
        self.password = password     # 사용자 비밀번호

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}')"

class Post:
    """
    게시글 정보를 담는 클래스입니다.
    """
    def __init__(self, post_id, user_id, content, timestamp, is_retweet=False, original_post_id=None):
        self.post_id = post_id                  # 고유 게시글 ID
        self.user_id = user_id                  # 게시글 작성자 ID
        self.content = content                  # 게시글 내용
        self.timestamp = timestamp              # 게시글 작성 시간
        self.is_retweet = is_retweet            # 리트윗 여부
        self.original_post_id = original_post_id  # 리트윗된 원본 게시글 ID

    def __repr__(self):
        return (f"Post(post_id={self.post_id}, user_id={self.user_id}, "
                f"content='{self.content}', is_retweet={self.is_retweet}, "
                f"original_post_id={self.original_post_id})")

class Like:
    """
    좋아요 정보를 담는 클래스입니다.
    """
    def __init__(self, like_id, post_id, user_id, timestamp):
        self.like_id = like_id     # 고유 좋아요 ID
        self.post_id = post_id     # 좋아요가 눌린 게시글 ID
        self.user_id = user_id     # 좋아요를 누른 사용자 ID
        self.timestamp = timestamp # 좋아요를 누른 시간
    
    def __repr__(self):
        return (f"Like(like_id={self.like_id}, post_id={self.post_id}, "
                f"user_id={self.user_id}, timestamp='{self.timestamp}')")