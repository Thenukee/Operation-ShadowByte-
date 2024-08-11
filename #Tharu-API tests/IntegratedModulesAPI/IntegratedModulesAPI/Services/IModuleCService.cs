using IntegratedModulesAPI.Models;

namespace IntegratedModulesAPI.Services
{
    public interface IModuleCService
    {
        string DisplayData(ScrapedData data);
    }

    public class ModuleCService : IModuleCService
    {
        public string DisplayData(ScrapedData data)
        {
            // Display logic
            return $"Data: {data.Data}, Scraped At: {data.ScrapedAt}";
        }
    }
}
