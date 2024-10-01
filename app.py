from flask import Flask, render_template, request, jsonify
import requests
import logging
import os  # Import os để sử dụng biến môi trường

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Route để render HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route xử lý API request cho câu hỏi văn bản
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')

    if message:
        # Lấy URL API từ biến môi trường
        api_url = os.getenv('API_URL', "https://deku-rest-api.gleeze.com/api/gpt-4o")
        api_url = f"{api_url}?q={message}&uid=unique_id"
        
        try:
            # Gọi API và nhận phản hồi
            response = requests.get(api_url)

            # Log phản hồi từ API
            app.logger.debug(f"API URL: {api_url}")
            app.logger.debug(f"API Response: {response.text}")

            # Kiểm tra mã trạng thái phản hồi
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    # Kiểm tra nếu có kết quả
                    reply = response_data.get('result')
                    if reply:
                        return jsonify({'reply': reply})
                    else:
                        return jsonify({'reply': 'Không có phản hồi từ API.'})
                except ValueError:
                    app.logger.error("Invalid JSON response from API.")
                    return jsonify({'error': 'Đã nhận được phản hồi không hợp lệ từ API.'})
            else:
                app.logger.error(f"API returned an error: {response.status_code} {response.text}")
                return jsonify({'error': f'Lỗi từ API: {response.status_code}'})
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request failed: {str(e)}")
            return jsonify({'error': 'Lỗi khi kết nối đến API.'})

    return jsonify({'error': 'Không có tin nhắn nào được cung cấp.'})

if __name__ == '__main__':
    app.run(debug=True)
