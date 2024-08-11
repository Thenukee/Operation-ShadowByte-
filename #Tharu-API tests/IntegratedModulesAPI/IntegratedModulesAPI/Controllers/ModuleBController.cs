using Microsoft.AspNetCore.Mvc;
using IntegratedModulesAPI.Services;

namespace IntegratedModulesAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ModuleBController : ControllerBase
    {
        private readonly IModuleBService _moduleBService;

        public ModuleBController(IModuleBService moduleBService)
        {
            _moduleBService = moduleBService;
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetScrapedData(int id)
        {
            var data = await _moduleBService.GetScrapedDataAsync(id);
            if (data == null)
            {
                return NotFound();
            }
            return Ok(data);
        }
    }
}
