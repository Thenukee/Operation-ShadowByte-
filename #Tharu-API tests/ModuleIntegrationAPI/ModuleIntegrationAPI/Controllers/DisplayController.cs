using System.Collections.Generic;
using System.Web.Http;
using ModuleIntegrationAPI.Models;
using ModuleIntegrationApi.Models;

namespace IntegratedModulesApi.Controllers
{
    public class DisplayController : ApiController
    {
        private static List<ScrapeData> dataToDisplay = new List<ScrapeData>();

        // GET: api/display
        [HttpGet]
        [Route("api/display")]
        public IEnumerable<ScrapeData> GetDisplayData()
        {
            return dataToDisplay;
        }

        // This method is used by DataController to send data to be displayed
        public static void AddDataToDisplay(ScrapeData data)
        {
            dataToDisplay.Add(data);
        }
    }
}
