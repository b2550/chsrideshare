from app import app

if __name__ == '__main__':
    app.run(None, 8000)
    app.logger.info('App initializing')
