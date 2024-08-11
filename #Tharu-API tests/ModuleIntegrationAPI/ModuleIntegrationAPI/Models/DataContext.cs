using Microsoft.EntityFrameworkCore;
using ModuleIntegrationApi.Models;

namespace ModuleIntegrationAPI.Models
{
    public class DataContext : DbContext
    {
        public DbSet<ScrapeData> ScrapedDatas { get; set; }
    }
}
