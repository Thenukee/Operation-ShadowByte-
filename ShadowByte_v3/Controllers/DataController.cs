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
            // Fetch nodes and links from the database
            var nodes = _context.Nodes
                .Select(n => new
                {
                    id = n.Id,
                    name = n.Name
                })
                .ToList();

            var links = _context.Links
                .Select(l => new
                {
                    source = l.SourceId,
                    target = l.TargetId
                })
                .ToList();

            // Return the data in the expected format
            return Ok(new { nodes, links });
        }
    }
}
