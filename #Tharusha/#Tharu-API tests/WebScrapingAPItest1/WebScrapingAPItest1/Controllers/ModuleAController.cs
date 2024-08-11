using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using WebScrapingAPItest1.Services;

[ApiController]
[Route("api/[controller]")]
public class ModuleAController : ControllerBase
{
    private readonly IModuleAService _moduleAService;
    private readonly IModuleBService _moduleBService;

    public ModuleAController(IModuleAService moduleAService, IModuleBService moduleBService)
    {
        _moduleAService = moduleAService;
        _moduleBService = moduleBService;
    }

    [HttpPost("scrape")]
    public async Task<IActionResult> ScrapeAndStoreData()
    {
        var result = await _moduleAService.ScrapeDataAsync();
        await _moduleBService.InsertScrapedDataAsync(result);
        return Ok(result);
    }
}
