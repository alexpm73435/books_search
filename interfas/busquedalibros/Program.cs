using System;
using System.Net.Http;
using System.Net.Http.Json;

using var cliente = new HttpClient();

string titulo = "Don Quijote";
string url = $"http://127.0.0.1:8000/comprar?titulo={Uri.EscapeDataString(titulo)}";

Libro? libro = await cliente.GetFromJsonAsync<Libro>(url);

if (libro is not null)
{
    Console.WriteLine($"{libro.Titulo} cuesta {libro.Precio} {libro.Moneda}");
}

record Libro(string Tienda, string Titulo, decimal Precio, string Moneda);