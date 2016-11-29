

from routes import create_rido_application


if __name__ == '__main__':
    create_rido_application().run(host='0.0.0.0',port=5000,debug=True)
