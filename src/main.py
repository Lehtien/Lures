from fastapi import FastAPI

app = FastAPI()


@app.get("/gettt")
async def root():
    return {"message": "Hello World"}