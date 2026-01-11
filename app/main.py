from fastapi import FastAPI

app = FastAPI(title="Warp FastAPI Demo AI")


@app.get("/")
async def read_root():
    return {"message": "Hello from warp-fastapi-demo-ai"}
