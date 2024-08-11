using IntegratedModulesAPI.Data;
using IntegratedModulesAPI.Models;

namespace IntegratedModulesAPI.Services
{
    public interface IModuleAService
    {
        Task ScrapeAndStoreDataAsync();
    }

    public class ModuleAService : IModuleAService
    {
        private readonly AppDbContext _context;

        public ModuleAService(AppDbContext context)
        {
            _context = context;
        }

        public async Task ScrapeAndStoreDataAsync()
        {
            // Perform web scraping and store data in the database
            var scrapedData = new ScrapedData
            {
                Data = "Scraped data",
                ScrapedAt = DateTime.Now
            };

            _context.ScrapedData.Add(scrapedData);
            await _context.SaveChangesAsync();
        }
    }
}
