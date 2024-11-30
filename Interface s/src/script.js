const cy = cytoscape({
    container: document.getElementById('cy'), // container to render in
    elements: [
      // Nodes
      { data: { id: 'WannaCry', label: 'WannaCry' } },
      { data: { id: 'KillSwitch', label: 'Kill Switch' } },
      { data: { id: 'Domains', label: 'Contacted domains' } },
      { data: { id: 'IPs', label: 'Contacted IPs' } },
      { data: { id: 'Parents', label: 'Execution parents' } },
      { data: { id: 'Files', label: 'Dropped files' } },
      { data: { id: 'URLs', label: 'Itw URLs' } },
      { data: { id: 'Embedded', label: 'Embedded domains' } },
  
      // Edges
      { data: { source: 'WannaCry', target: 'KillSwitch' } },
      { data: { source: 'WannaCry', target: 'Domains' } },
      { data: { source: 'WannaCry', target: 'IPs' } },
      { data: { source: 'WannaCry', target: 'Parents' } },
      { data: { source: 'WannaCry', target: 'Files' } },
      { data: { source: 'WannaCry', target: 'URLs' } },
      { data: { source: 'WannaCry', target: 'Embedded' } },
    ],
    style: [
      {
        selector: 'node',
        style: {
          'background-color': '#E87474',
          'label': 'data(label)',
          'text-outline-color': '#1e1e2f',
          'text-outline-width': 2,
          'color': '#fff',
          'font-size': '12px',
        },
      },
      {
        selector: 'edge',
        style: {
          'width': 2,
          'line-color': '#aaa',
          'target-arrow-color': '#aaa',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier',
        },
      },
    ],
    layout: {
      name: 'cose',
      animate: true,
    },
  });
  
