from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..formss import AnswerForm
from ..models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST': # POST방식
        form = AnswerForm(request.POST) # POST방식일 경우 화면에서 전달받은 데이터로 폼의 값이 채워짐
        if form.is_valid(): # POST요청으로 받은 form이 유효한지 검사
            answer = form.save(commit=False) # create_date값이 없으므로 오류방지를위해 임시저장
            answer.author = request.user  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question_id)
    else: # GET 방식
        form = AnswerForm()
    context = {'question' : question,'form' : form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request,'수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id)

# POST 방식과 GET 방식으로 나누어 if 문으로 걸러준다, form 의 값이 바뀐다는 말 #
    # POST 방식으로 호출 (수정 수행)
    if request.method == "POST": # POST 라는것은 일단 폼에서 데이터가 넘어왔다는 말!
        form = AnswerForm(request.POST, instance=answer) #insrance변수에 기존값을 저장
        if form.is_valid():  # 데이터가 유효한지 아닌지를 검사
            answer = form.save(commit=False)
            # 임시저장한다 : answer 에 아직  author 값과 modify_date의 값이 없어 오류 발생할수있어서

            # 임시저장하고 나머지 값들을 넣어준다.
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save() # answer DB저장
            return  redirect('pybo:detail', question_id = answer.question.id)
    # GET 방식으로 호출
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return  render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer =get_object_or_404(Answer, pk=answer_id) # answer 안에 answer_id 인것의 답변을 대입
    if request.user != answer.author:   # 아이디와 글쓴이가 같으면
        messages.error(request,'삭제권한이 없습니다.') # 삭제권한인 없습니다. 출력
    else: # 그렇지않으면
        answer.delete() # 해당 답변 삭제하고 DB에 저장
    return  redirect('pybo:detail', question_id = answer.question.id)
