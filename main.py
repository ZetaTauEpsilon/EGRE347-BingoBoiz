from server import socketio, app

# Run the Flask application
if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port='80')
    print("Started Server")