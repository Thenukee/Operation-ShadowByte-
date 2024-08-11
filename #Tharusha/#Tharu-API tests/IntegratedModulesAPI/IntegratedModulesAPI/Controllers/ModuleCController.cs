using Microsoft.AspNetCore.Mvc;
using IntegratedModulesAPI.Services;

namespace IntegratedModulesAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ModuleCController : ControllerBase
    {
        private readonly IModuleCService _moduleCService;
        private readonly IModuleBService _moduleBService;

        public ModuleCController(IModuleCService moduleCService, IModuleBService moduleBService)
        {
            _moduleCService = moduleCService;
            _moduleBService = moduleBService;
        }

        [HttpGet("display/{id}")]
        public async Task<IActionResult> DisplayData(int id)
        {
            var data = await _moduleBService.GetScrapedDataAsync(id);
            if (data == null)
            {
                return NotFound();
            }
            var result = _moduleCService.DisplayData(data);
            return Ok(result);
        }
    }
}
