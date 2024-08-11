namespace WebScrapingAPItest1.Data
{
    using Microsoft.EntityFrameworkCore;
    using WebScrapingAPItest1.Models;

    public class AppDbContext : DbContext
    {
        public DbSet<Book> Books { get; set; }

        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }
    }

}
