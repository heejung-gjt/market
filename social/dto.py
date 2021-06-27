from dataclasses import dataclass
from django.contrib.auth.models import User

@dataclass
class CommentDto():
  content:str
  article_pk:str
  writer_pk:str
  owner_pk:str


@dataclass
class ReCommentDto():
  content:str
  writer: User
  created_at: int
  user_pk:str
  comment_pk:str
  article_pk:str
