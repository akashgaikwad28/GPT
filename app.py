import os
from app import create_app

print("Current working directory:", os.getcwd())  # Print current working directory

# Create an instance of the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the Flask application on all available IPs and specify the port
    print("Flask app is running on http://127.0.0.1:5000/")
    app.run(host='127.0.0.1', port=5000, debug=True)  # Use 127.0.0.1 for local access
