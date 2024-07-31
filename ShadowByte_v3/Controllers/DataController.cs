using Microsoft.AspNetCore.Mvc;
using ShadowByte_v3.Data;
using ShadowByte_v3.Models;
using System.Linq;

namespace ShadowByte_v3.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DataController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public DataController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult GetData()
        {
            var nodes = _context.Nodes.ToList();
            var links = _context.Links.ToList();

            return Ok(new { nodes, links });
        }
    }
}
