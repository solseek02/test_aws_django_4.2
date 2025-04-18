# Red Hat UBI Python 3.9 이미지 사용
FROM registry.access.redhat.com/ubi8/python-39

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 패키지 설치 (root 권한으로 실행)
USER root
RUN dnf install -y \
    gcc \
    python3-devel \
    && dnf clean all

# 비루트 사용자로 전환
USER 1000800000

# Python 패키지 설치를 위한 requirements.txt 복사
COPY requirements.txt .

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사 (mydjango 디렉토리 내의 파일들만)
COPY myproject/ /app/myproject/
COPY myapp/ /app/myapp/
COPY manage.py /app/

# DB 디렉토리 생성 및 권한 설정
USER root
RUN mkdir -p /app/db && \
    chown -R 1000800000:0 /app && \
    chmod -R g+rw /app
USER 1000800000

# 정적 파일 수집
RUN python3 manage.py collectstatic --noinput

# 포트 설정
EXPOSE 8000

# 서버 실행
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 

