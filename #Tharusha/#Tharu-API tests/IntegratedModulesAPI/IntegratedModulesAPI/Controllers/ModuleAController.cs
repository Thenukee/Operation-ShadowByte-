using Microsoft.AspNetCore.Mvc;
using IntegratedModulesAPI.Services;

namespace IntegratedModulesAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ModuleAController : ControllerBase
    {
        private readonly IModuleAService _moduleAService;

        public ModuleAController(IModuleAService moduleAService)
        {
            _moduleAService = moduleAService;
        }

        [HttpPost("scrape")]
        public async Task<IActionResult> ScrapeAndStoreData()
        {
            await _moduleAService.ScrapeAndStoreDataAsync();
            return Ok();
        }
    }
}
