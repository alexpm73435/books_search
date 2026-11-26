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
            string titulo = txtTitulo.Text.Trim();
            string url = $"http://127.0.0.1:8000/comprar?titulo={Uri.EscapeDataString(titulo)}";

            Libro? libro = await cliente.GetFromJsonAsync<Libro>(url);

            if (libro is not null)
            {
                lblResultado.Text = $"{libro.Titulo} cuesta {libro.Precio} {libro.Moneda}";
            }
        }
    }
}
