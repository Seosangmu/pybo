from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..formss import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST': # POST방식
        form = QuestionForm(request.POST) # POST방식일 경우 화면에서 전달받은 데이터로 폼의 값이 채워짐
        if form.is_valid(): # POST요청으로 받은 form이 유효한지 검사
            question = form.save(commit=False) # create_date값이 없으므로 오류방지를위해 임시저장
            question.author = request.user  # 추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else: # GET 방식
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return  redirect('pybo:detail', question_id = question.id)

# POST 방식과 GET 방식으로 나누어 if 문으로 걸러준다, form 의 값이 바뀐다는 말 #
    # POST 방식으로 호출 (수정 수행)
    if request.method == 'POST': # POST방식 (수정 수행)
        form = QuestionForm(request.POST, instance=question) # POST방식일 경우 화면에서 전달받은 데이터로 폼의 값이 채워짐
        if form.is_valid(): # POST요청으로 받은 form이 유효한지 검사
            question = form.save(commit=False) # create_date값이 없으므로 오류방지를위해 임시저장
            question.author = request.user  # 추가한 속성 author 적용
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question.id)

    else: # GET 방식 (그냥 uestion_form.html 띄우기)
        form = QuestionForm(instance=question)
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 질문 글쓴이와 로그인 사용자가 동일하면
        messages.error(request,'삭제권한이 없습니다')
        return  redirect('pybo:detail', question_id = question.id)
    question.delete()
    return  redirect('pybo:index')
