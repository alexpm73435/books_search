import requests
import json
import time
from urllib.parse import quote, urlencode, urljoin
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/comprar")
def saludar(titulo: str):
    return [
        {"tienda": "Tienda A", "titulo": titulo, "precio": 179, "moneda": "MXN"},
        {"tienda": "Tienda B", "titulo": titulo, "precio": 67, "moneda": "MXN"},
    ]

def consultar_gandhi(isbn: str):
    isbn = isbn.strip()
    url = "https://www.gandhi.com.mx/api/catalog_system/pub/products/search"
    try:
        respuesta = requests.get(
            url,
            params={"fq": f"alternateIds_Ean:{isbn}"},
            timeout=8,
        )
        respuesta.raise_for_status()
        productos = respuesta.json()
    except requests.RequestException as error:
        print(f"Error de Gandhi al consultar el ISBN: {error!r}", flush=True)
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
                            "isbn": isbn,
                        }
                    ]

    return []


@app.get("/buscar")
def buscar(titulo: str):
    url = "https://www.gandhi.com.mx/api/catalog_system/pub/products/search"

    parametros = {"ft": titulo.strip(), "_from": 0, "_to": 4}
    url = f"{url}?{urlencode(parametros, quote_via=quote)}"

    try:
        try:
            respuesta = requests.get(url, timeout=8)
        except requests.ConnectionError:
            print("Se cortó la conexión con Gandhi. Reintentando...", flush=True)
            time.sleep(1)
            respuesta = requests.get(url, timeout=8)

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


def consultar_buscalibre(isbn: str):
    respuesta = requests.get(
        "https://www.buscalibre.com.mx/libros/search/",
        params={"q": isbn},
        timeout=8,
    )
    respuesta.raise_for_status()
    pagina = BeautifulSoup(respuesta.text, "html.parser")

    # La búsqueda puede abrir la ficha o mostrar una lista de resultados.
    if f"/{isbn}/p/" not in respuesta.url:
        enlace = pagina.select_one(
            f'a[href^="/libro-"][href*="/{isbn}/p/"], '
            f'a[href^="https://www.buscalibre.com.mx/libro-"][href*="/{isbn}/p/"]'
        )
        if enlace is None:
            return []

        ficha = requests.get(urljoin(respuesta.url, enlace["href"]), timeout=8)
        ficha.raise_for_status()
        pagina = BeautifulSoup(ficha.text, "html.parser")

    for bloque in pagina.select('script[type="application/ld+json"]'):
        try:
            datos = json.loads(bloque.string or "")
        except json.JSONDecodeError:
            continue

        if not isinstance(datos, dict) or datos.get("isbn") != isbn:
            continue

        ofertas = datos.get("offers", [])
        if isinstance(ofertas, dict):
            ofertas = [ofertas]

        for oferta in ofertas:
            if (
                oferta.get("availability", "").endswith("/InStock")
                and oferta.get("itemCondition", "").endswith("/NewCondition")
                and oferta.get("priceCurrency") == "MXN"
            ):
                return [{
                    "tienda": "BuscaLibre",
                    "titulo": datos["name"],
                    "precio": float(oferta["price"]),
                    "moneda": "MXN",
                    "isbn": isbn,
                }]

    return []


@app.get("/comparar")
def comparar(isbn: str):
    isbn = isbn.strip()
    if len(isbn) != 13 or not isbn.isascii() or not isbn.isdigit():
        raise HTTPException(422, "Escribe un ISBN de 13 dígitos.")

    ofertas = []
    hubo_error = False

    for consultar in (consultar_gandhi, consultar_buscalibre):
        try:
            ofertas.extend(consultar(isbn))
        except HTTPException:
            hubo_error = True
        except requests.RequestException as error:
            hubo_error = True
            print(f"Error de BuscaLibre en /comparar: {error!r}", flush=True)

    if hubo_error and not ofertas:
        raise HTTPException(502, "No se pudo completar la consulta de precios.")

    return sorted(ofertas, key=lambda oferta: oferta["precio"])