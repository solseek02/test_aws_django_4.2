from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm
import requests
import os
import json

# ✅ 랜딩 페이지 뷰
def landing_view(request):
    return render(request, 'landing.html')

# ✅ 회원가입 뷰 (회원가입 후 로그인 페이지로 이동)
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # DB 저장하지 않고 세션에만 저장
            request.session['user'] = form.cleaned_data['username']
            return redirect('service_choice')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# ✅ 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # DB 인증하지 않고 세션에만 저장
            request.session['user'] = form.cleaned_data['username']
            return redirect('service_choice')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# ✅ 서비스 선택 페이지 뷰
def service_choice_view(request):
    if not request.session.get('user'):
        return redirect('login')
    return render(request, 'service_choice.html', {
        'JANUS_PRO_URL': os.environ.get('JANUS_PRO_URL')
    })

# ✅ 채팅 페이지 뷰
def chat_view(request):
    if not request.session.get('user'):
        return redirect('login')
    return render(request, 'chat.html')

# ✅ DeepSeek 챗봇 API 엔드포인트
@csrf_exempt
def chat_api(request):
    if 'user' not in request.session:
        return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            
            if not prompt:
                return JsonResponse({"error": "prompt 값이 없습니다."}, status=400)

            # DeepSeek API URL 설정
            DEEPSEEK_API_URL = os.environ.get("DEEPSEEK_API_URL", "http://localhost:11434/api/generate")
            
            # DeepSeek API 요청
            payload = {
                "model": "deepseek-r1:8b",
                "prompt": prompt,
                "stream": False
            }
            
            try:
                response = requests.post(DEEPSEEK_API_URL, json=payload, timeout=30)
                response.raise_for_status()  # HTTP 오류 발생시 예외 발생
                
                answer = response.json().get('response', '응답이 없습니다.')
                # HTML 특수 문자 처리
                answer = answer.replace("\u003c", "<").replace("\u003e", ">")
                
                return JsonResponse({"response": answer})
                
            except requests.RequestException as e:
                return JsonResponse({
                    "error": f"DeepSeek API 오류: {str(e)}"
                }, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 JSON 형식"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)
            
    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)

