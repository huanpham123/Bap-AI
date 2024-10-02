from flask import Flask, render_template, request, jsonify
import requests
import logging
import urllib.parse

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')

    if message:
        # Mã hóa URL cho message
        encoded_message = urllib.parse.quote(message)
        
        # Phần URL cố định của API
        api_base_url = "https://deku-rest-api.gleeze.com/api/gpt-4o"
        
        # Tạo URL API với message đã được mã hóa
        api_url = f"{api_base_url}?q={encoded_message}&uid=unique_id"

        app.logger.debug(f"API URL: {api_url}")

        try:
            # Gọi API và nhận phản hồi với timeout
            response = requests.get(api_url, timeout=15)  # Tăng timeout

            # Log phản hồi từ API
            app.logger.debug(f"API Response: {response.text}")

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    app.logger.debug(f"Response Data: {response_data}")
                    return jsonify({'reply': response_data.get('result', 'No answer provided')})
                except ValueError:
                    app.logger.error("Invalid JSON response from API.")
                    return jsonify({'error': 'Invalid response from API.'})
            else:
                app.logger.error(f"API returned an error: {response.status_code} {response.text}")
                return jsonify({'error': f'API error: {response.status_code}'})
        except requests.exceptions.Timeout:
            app.logger.error("Request timed out.")
            return jsonify({'error': 'Request timed out. Please try again.'})
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request failed: {str(e)}")
            return jsonify({'error': 'Error connecting to the API.'})

    return jsonify({'error': 'No message provided'})

if __name__ == '__main__':
    app.run(debug=True)
