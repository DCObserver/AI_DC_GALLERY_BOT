#!/bin/bash

# 스크립트 실행 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 디렉토리 설정
VENV_DIR="./galling-bot"

# 가상환경이 이미 설정되어 있는지 확인
if [ ! -d "$VENV_DIR" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv $VENV_DIR
    echo "Virtual environment created."
fi

# 가상환경 활성화
source "$VENV_DIR/bin/activate"

# 필요한 패키지 설치
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt -q
else
    echo "No requirements.txt found, skipping dependency installation."
fi

# 환경 변수 설정 (필요에 따라 수정)
export GOOGLE_API_KEY='your_google_api_key_here'

# Python 스크립트 실행
echo "Starting the bot..."
python3 src/main.py

# 가상환경 비활성화
deactivate
