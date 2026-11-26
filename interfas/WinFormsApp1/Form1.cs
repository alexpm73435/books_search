using System.Net.Http.Json;

namespace WinFormsApp1
{
    public partial class Form1 : Form
    {
        private readonly HttpClient cliente = new();
        public Form1()
        { 
        InitializeComponent();
        }

        private async void btnBuscar_Click(object sender, EventArgs e)
        {
            string busqueda = txtTitulo.Text.Trim();

            if (busqueda.Length == 0)
            {
                lblResultado.Text = "Escribe el ISBN del libro o el titulo del libro.";
                return;
            }

            bool esIsbn = busqueda.Length == 13 && busqueda.All(char.IsAsciiDigit);
            string valor = Uri.EscapeDataString(busqueda);

            string url = esIsbn
                ? $"http://127.0.0.1:8000/comparar?isbn={valor}"
                : $"http://127.0.0.1:8000/buscar?titulo={valor}";

            try
            {
                List<Libro>? ofertas = await cliente.GetFromJsonAsync<List<Libro>>(url);

                if (ofertas is null || ofertas.Count == 0)
                {
                    lblResultado.Text = "No se encontraron ofertas .";
                    return;
                }

                var filas = new List<string>();

                foreach (Libro oferta in ofertas)
                {
                    string isbnTexto = string.IsNullOrWhiteSpace(oferta.Isbn)
                        ? ""
                        : $" | ISBN: {oferta.Isbn}";

                    filas.Add($"{oferta.Titulo} — {oferta.Tienda}: {oferta.Precio} {oferta.Moneda}{isbnTexto}");
                }

                lblResultado.Text = string.Join(Environment.NewLine, filas);
            }
            catch (HttpRequestException)
            {
                lblResultado.Text = "No se pudo consultar el precio. Revisa la terminal de FastAPI.";
            }
        }
    }
}
