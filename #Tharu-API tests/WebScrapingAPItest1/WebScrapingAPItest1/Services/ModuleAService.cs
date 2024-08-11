namespace WebScrapingAPItest1.Services
{
    using System.Net.Http;
    using System.Threading.Tasks;
    using Microsoft.Extensions.Configuration;

    public class ModuleAService : IModuleAService
    {
        private readonly HttpClient _httpClient;
        private readonly IConfiguration _configuration;

        public ModuleAService(HttpClient httpClient, IConfiguration configuration)
        {
            _httpClient = httpClient;
            _configuration = configuration;
        }

        public async Task<string> ScrapeDataAsync()
        {
            var pythonServiceUrl = _configuration["PythonServiceUrl"];
            var response = await _httpClient.GetStringAsync($"{pythonServiceUrl}/scrape");
            return response;
        }
    }

}
