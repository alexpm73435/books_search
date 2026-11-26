from fastapi import FastAPI

app = FastAPI()

@app.get("/comprar")
def saludar(titulo: str):
    return {"tienda": "Tienda de prueba",
            "titulo": titulo,
            "precio": 199.00,
            "moneda": "MXN",
            }