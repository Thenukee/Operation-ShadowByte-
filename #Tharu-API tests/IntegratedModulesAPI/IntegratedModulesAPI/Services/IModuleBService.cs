using IntegratedModulesAPI.Data;
using IntegratedModulesAPI.Models;

namespace IntegratedModulesAPI.Services
{
    public interface IModuleBService
    {
        Task<ScrapedData> GetScrapedDataAsync(int id);
    }

    public class ModuleBService : IModuleBService
    {
        private readonly AppDbContext _context;

        public ModuleBService(AppDbContext context)
        {
            _context = context;
        }

        public async Task<ScrapedData> GetScrapedDataAsync(int id)
        {
            return await _context.ScrapedData.FindAsync(id);
        }
    }
}
