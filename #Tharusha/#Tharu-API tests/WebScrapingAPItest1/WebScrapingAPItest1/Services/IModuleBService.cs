namespace WebScrapingAPItest1.Services
{
    public interface IModuleBService
    {
        Task InsertScrapedDataAsync(string jsonData);
    }

}
