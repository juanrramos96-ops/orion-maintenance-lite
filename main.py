from fastapi import FastAPI

app = FastAPI(
    title="ORION Maintenance Lite API",
    description="API para la gestion de activos y mantenimiento ITS",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "ORION Maintenance Lite API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }