import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/comprar")
def saludar(titulo: str):
    return [
        {"tienda": "Tienda A", "titulo": titulo, "precio": 179, "moneda": "MXN"},
        {"tienda": "Tienda B", "titulo": titulo, "precio": 67, "moneda": "MXN"},
    ]

@app.get("/comparar")
def comparar(isbn:str):
    isbn = isbn.strip()
    url="https://www.gandhi.com.mx/api/catalog_system/pub/products/search"
    try:
        respuesta = requests.get(
            url,
            params={"fq": f"alternateIds_Ean:{isbn}"},
            timeout=8,
            
        )
        respuesta.raise_for_status()
        productos = respuesta.json()
    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail="No se pudo consultar Gandhi.",
        ) from error

    for producto in productos:
        for libro in producto["items"]:
            if libro["ean"] != isbn:
                continue

            for vendedor in libro["sellers"]:
                oferta = vendedor["commertialOffer"]

                if oferta["IsAvailable"]:
                    return [
                        {
                            "tienda": "Gandhi",
                            "titulo": producto["productName"],
                            "precio": oferta["Price"],
                            "moneda": "MXN",
                        }
                    ]

    return []