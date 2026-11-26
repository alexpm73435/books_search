namespace WinFormsApp1
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            lblTitulo = new Label();
            txtTitulo = new TextBox();
            btnBuscar = new Button();
            lblResultado = new Label();
            SuspendLayout();
            // 
            // lblTitulo
            // 
            lblTitulo.AutoSize = true;
            lblTitulo.Location = new Point(568, 40);
            lblTitulo.Name = "lblTitulo";
            lblTitulo.Size = new Size(170, 32);
            lblTitulo.TabIndex = 0;
            lblTitulo.Text = "Título del libro";
            // 
            // txtTitulo
            // 
            txtTitulo.Location = new Point(325, 174);
            txtTitulo.Name = "txtTitulo";
            txtTitulo.Size = new Size(331, 39);
            txtTitulo.TabIndex = 1;
            // 
            // btnBuscar
            // 
            btnBuscar.Location = new Point(752, 133);
            btnBuscar.Name = "btnBuscar";
            btnBuscar.Size = new Size(192, 97);
            btnBuscar.TabIndex = 2;
            btnBuscar.Text = "Buscar";
            btnBuscar.UseVisualStyleBackColor = true;
            btnBuscar.Click += btnBuscar_Click;
            // 
            // lblResultado
            // 
            lblResultado.AutoSize = true;
            lblResultado.Location = new Point(523, 297);
            lblResultado.Name = "lblResultado";
            lblResultado.Size = new Size(301, 32);
            lblResultado.TabIndex = 3;
            lblResultado.Text = "El resultado aparecerá aquí";
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(13F, 32F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1482, 721);
            Controls.Add(lblResultado);
            Controls.Add(btnBuscar);
            Controls.Add(txtTitulo);
            Controls.Add(lblTitulo);
            Name = "Form1";
            Text = "Form1";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label lblTitulo;
        private TextBox txtTitulo;
        private Button btnBuscar;
        private Label lblResultado;
    }
}
