using IntegratedModulesAPI.Data;
using IntegratedModulesAPI.Services;
using Microsoft.EntityFrameworkCore;

public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers();
        services.AddDbContext<AppDbContext>(options =>
            options.UseInMemoryDatabase("ScrapedDataDb"));

        services.AddScoped<IModuleAService, ModuleAService>();
        services.AddScoped<IModuleBService, ModuleBService>();
        services.AddScoped<IModuleCService, ModuleCService>();
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }

        app.UseRouting();

        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
    }
}
