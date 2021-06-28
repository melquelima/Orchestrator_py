import os
from app import app,socketio
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #socketio.init_app(app,cors_allowed_origins="*")
    #socketio.run(app, debug=True, host='0.0.0.0',port=port)
    #app.run()