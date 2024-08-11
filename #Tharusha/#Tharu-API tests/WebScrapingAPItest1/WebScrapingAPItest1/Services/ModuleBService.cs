namespace WebScrapingAPItest1.Services
{
    using System.Text.Json;
    using System.Threading.Tasks;
    using WebScrapingAPItest1.Data;
    using WebScrapingAPItest1.Models;

    public class ModuleBService : IModuleBService
    {
        private readonly AppDbContext _context;

        public ModuleBService(AppDbContext context)
        {
            _context = context;
        }

        public async Task InsertScrapedDataAsync(string jsonData)
        {
            var book = JsonSerializer.Deserialize<Book>(jsonData);
            _context.Books.Add(book);
            await _context.SaveChangesAsync();
        }
    }

}
