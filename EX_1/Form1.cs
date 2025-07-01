using EX_1;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace PacketDataAnalyzer
{
    public partial class Form1 : Form
    {
        private List<HostData> allData = new List<HostData>();

        public Form1()
        {
            InitializeComponent();
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filePath = openFileDialog.FileName;
                string[] lines = File.ReadAllLines(filePath);
                allData.Clear();

                foreach (var line in lines)
                {
                    try
                    {
                        var parts = line.Split(' ', (char)StringSplitOptions.RemoveEmptyEntries);
                        if (parts.Length >= 7)
                        {
                            var time = TimeSpan.Parse(parts[0]);
                            var date = DateTime.Parse(parts[1]);
                            var dateTime = date.Date + time;
                            var host = parts[2];
                            var packets = int.Parse(parts[3]);
                            var size = int.Parse(parts[5]);

                            allData.Add(new HostData
                            {
                                DateTime = dateTime,
                                Host = host,
                                Packets = packets,
                                Size = size
                            });
                        }
                    }
                    catch { }
                }

                dataGridView1.DataSource = allData;
                lblTotal.Text = $"Загальний обсяг: {HostDataProcessor.CalculateTotalData(allData)} байт";
            }
        }

        private void btnFilter_Click(object sender, EventArgs e)
        {
            var selectedDate = dateTimePicker1.Value;
            var filtered = HostDataProcessor.FilterByDate(allData, selectedDate);
            dataGridView1.DataSource = filtered;
            lblTotal.Text = $"Загальний обсяг: {HostDataProcessor.CalculateTotalData(filtered)} байт";
        }

        private void dateTimePicker1_ValueChanged(object sender, EventArgs e)
        {

        }
    }
}
