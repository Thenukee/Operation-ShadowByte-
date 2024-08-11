using Microsoft.AspNetCore.Mvc;

namespace CytoscapeTestWebApp.Controllers
{
    public class GraphController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
