# ベースイメージ（軽量）
FROM python:3.11-slim

# 必要な OS パッケージをインストール
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-jpn \
    ghostscript \
    poppler-utils \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app

# アプリファイルをコピー
COPY app/ /app
COPY requirements.txt /app/requirements.txt

# Python ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI を起動するポート
EXPOSE 8000

# コンテナ起動時のコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
