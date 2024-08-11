using ModuleIntegrationApi.Models;
using ModuleIntegrationAPI.Models;
using System.Data.Entity;

namespace IntegratedModulesApi.Models
{
    public class DatabaseInitializer : DropCreateDatabaseIfModelChanges<DataContext>
    {
        protected override void Seed(DataContext context)
        {
            var data = new List<ScrapeData>
            {
                new ScrapeData { Data = "Sample data 1" },
                new ScrapeData { Data = "Sample data 2" }
            };

            data.ForEach(d => context.ScrapedDatas.Add(d));
            context.SaveChanges();
        }
    }
}
