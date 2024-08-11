using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

namespace CytoscapeTestWebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GraphDataController : ControllerBase
    {
        [HttpGet]
        public IActionResult Get()
        {
            var filePath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot/data/graphData.json");
            var jsonData = System.IO.File.ReadAllText(filePath);
            var elements = JsonSerializer.Deserialize<object[]>(jsonData);

            return Ok(elements);
        }
    }
}
