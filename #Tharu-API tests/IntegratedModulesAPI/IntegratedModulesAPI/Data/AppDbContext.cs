using IntegratedModulesAPI.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;

namespace IntegratedModulesAPI.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        // Define DbSets for your entities
        public DbSet<ScrapedData> ScrapedData { get; set; }
    }
}
