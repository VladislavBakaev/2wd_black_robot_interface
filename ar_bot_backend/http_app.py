from flask import send_file
from robot_control_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)