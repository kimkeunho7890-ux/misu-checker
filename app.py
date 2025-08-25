from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from flask_cors import CORS
import os

# Render는 정적 파일을 제공하는 별도 폴더를 사용하는 것이 좋습니다.
# 'static' 폴더를 만들어 그 안에 index.html을 넣는 것을 권장하지만,
# 편의를 위해 현재 구조를 유지합니다.
app = Flask(__name__)
CORS(app)

# CSV 파일 로딩
try:
    df = pd.read_csv('data.csv', encoding='utf-8-sig')
    print("✓ CSV 파일 로딩 성공!")
except Exception as e:
    print(f"✗ CSV 파일을 읽는 중 오류 발생: {e}")
    df = pd.DataFrame()

# API 서버 로직 (이전과 동일)
@app.route('/search', methods=['GET'])
def search_pos_code():
    pos_code_query = request.args.get('pos_code')
    print(f"→ 요청 받음: POS코드 = {pos_code_query}")
    if df.empty:
        return jsonify({"error": "서버에 데이터가 로드되지 않았습니다."}), 500
    try:
        result_df = df[df['POS코드'].astype(str).str.strip() == pos_code_query.strip()]
        if result_df.empty:
            return jsonify([])
        else:
            return result_df.to_json(orient='records', force_ascii=False)
    except Exception as e:
        print(f"✗ 데이터 처리 중 오류 발생: {e}")
        return jsonify({"error": "데이터 처리 중 서버 오류 발생"}), 500

# 웹 페이지 제공 로직
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Render에서 실행할 때는 이 부분은 사용되지 않습니다.
if __name__ == '__main__':
    app.run(debug=True)