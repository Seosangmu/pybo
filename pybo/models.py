from django.db import models
from django.contrib.auth.models import User

class Question(models.Model): #model 은 데이터베이스 modle Qusetion이라는 테이블 생성
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.content

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 글쓴이
    content = models.TextField() # 댓글 내용
    create_date = models.DateTimeField() # 댓글 작성일시
    modify_date = models.DateTimeField(null=True, blank=True) #댓글 수정일시
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 질문
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 답변
