from flask import Flask, render_template, request, jsonify
import requests
import logging
import os  # Thêm import os để sử dụng biến môi trường

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
        api_url = os.getenv('API_URL', f"https://deku-rest-api.gleeze.com/api/gpt-4o?q={message}&uid=unique_id")
        
        try:
            response = requests.get(api_url)

            # Log phản hồi từ API
            app.logger.debug(f"API Response: {response.text}")

            # Kiểm tra mã trạng thái phản hồi
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    return jsonify({'reply': response_data.get('result', 'No answer provided')})
                except ValueError:
                    app.logger.error("Invalid JSON response from API.")
                    return jsonify({'error': 'Invalid response from API.'})
            else:
                app.logger.error(f"API returned an error: {response.status_code} {response.text}")
                return jsonify({'error': f'API error: {response.status_code}'})
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'error': str(e)})

    return jsonify({'error': 'No message provided'})

if __name__ == '__main__':
    app.run(debug=True)
