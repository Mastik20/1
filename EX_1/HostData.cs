using System;

namespace PacketDataAnalyzer
{
    public class HostData
    {
        public DateTime DateTime { get; set; }
        public string Host { get; set; }
        public int Packets { get; set; }
        public int Size { get; set; }
        public int TotalData => Packets * Size;
    }
}
