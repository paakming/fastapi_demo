from app.core import host, port, reload

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app.core:app', host=host, port=port, reload=reload)
