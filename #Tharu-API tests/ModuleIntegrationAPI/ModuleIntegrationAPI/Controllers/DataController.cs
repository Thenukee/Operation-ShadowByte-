using System.Collections.Generic;
using System.Linq;
using System.Web.Http;
using IntegratedModulesApi.Controllers;
using Microsoft.AspNetCore.Mvc;
using ModuleIntegrationApi.Models;
using ModuleIntegrationAPI.Models;

namespace ModuleIntegrationApi.Controllers
{
    public class DataController : ApiController
    {
        private DataContext db = new DataContext();

        // GET: api/data
        [System.Web.Http.HttpGet]
        [System.Web.Http.Route("api/data")]
        public IEnumerable<ScrapeData> GetScrapedData()
        {
            return db.ScrapedDatas.ToList();
        }

        // POST: api/data
        [System.Web.Http.HttpPost]
        [System.Web.Http.Route("api/data")]
        public IHttpActionResult SendData([System.Web.Http.FromBody] ScrapeData data)
        {
            if (data == null)
            {
                return BadRequest("Data cannot be null");
            }

            DisplayController.AddDataToDisplay(data);
            return Ok();
        }
    }
}
