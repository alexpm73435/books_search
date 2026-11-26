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
        print(f"Error de Gandhi en /buscar: {error!r}", flush=True)
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

    return []  # Aquí termina comparar


@app.get("/buscar")
def buscar(titulo: str):
    url = "https://www.gandhi.com.mx/api/catalog_system/pub/products/search"

    parametros = {"ft": titulo.strip(), "_from": 0, "_to": 4}

    try:
        try:
            respuesta = requests.get(url, params=parametros, timeout=8)
        except requests.ConnectionError:
            print("Se cortó la conexión con Gandhi. Reintentando...", flush=True)
            time.sleep(1)
            respuesta = requests.get(url, params=parametros, timeout=8)

        respuesta.raise_for_status()
        productos = respuesta.json()
    except requests.RequestException as error:
        print(f"Error de Gandhi en /buscar: {error!r}", flush=True)
        raise HTTPException(502, "No se pudo consultar Gandhi.") from error

    resultados = []

    for producto in productos:
        for libro in producto["items"]:
            for vendedor in libro["sellers"]:
                oferta = vendedor["commertialOffer"]

                if oferta["IsAvailable"]:
                    resultados.append({
                        "tienda": "Gandhi",
                        "titulo": producto["productName"],
                        "precio": oferta["Price"],
                        "moneda": "MXN",
                        "isbn": libro["ean"],
                    })
                    break

    return resultados