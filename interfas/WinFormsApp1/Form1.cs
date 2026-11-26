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
            string isbn = txtTitulo.Text.Trim();

            if (isbn.Length == 0)
            {
                lblResultado.Text = "Escribe el ISBN del libro.";
                return;
            }

            string url = $"http://127.0.0.1:8000/comparar?isbn={Uri.EscapeDataString(isbn)}";

            try
            {
                List<Libro>? ofertas = await cliente.GetFromJsonAsync<List<Libro>>(url);

                if (ofertas is null || ofertas.Count == 0)
                {
                    lblResultado.Text = "No se encontraron ofertas para ese ISBN.";
                    return;
                }

                var filas = new List<string>();

                foreach (Libro oferta in ofertas)
                {
                    filas.Add($"{oferta.Titulo} — {oferta.Tienda}: {oferta.Precio} {oferta.Moneda}");
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
