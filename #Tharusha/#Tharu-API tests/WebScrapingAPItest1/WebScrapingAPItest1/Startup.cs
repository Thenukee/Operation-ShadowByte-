using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using System.Configuration;
using WebScrapingAPItest1.Data;
using WebScrapingAPItest1.Services;

namespace WebScrapingAPItest1
{
    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddDbContext<AppDbContext>(options =>
                options.UseSqlite(Configuration.GetConnectionString("DefaultConnection")));
            services.AddHttpClient();
            services.AddScoped<IModuleAService, ModuleAService>();
            services.AddScoped<IModuleBService, ModuleBService>();
            services.AddControllers();
        }



    }
}
