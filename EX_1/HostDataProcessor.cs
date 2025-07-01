using System;
using System.Collections.Generic;
using System.Linq;

namespace PacketDataAnalyzer
{
    public class HostDataProcessor
    {
        public static List<HostData> FilterByDate(List<HostData> data, DateTime date)
        {
            return data.Where(d => d.DateTime.Date == date.Date).ToList();
        }

        public static long CalculateTotalData(List<HostData> data)
        {
            return data.Sum(d => (long)d.Packets * d.Size);
        }
    }
}
