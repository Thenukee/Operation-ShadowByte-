import React, { useRef, useEffect } from "react";
import Cytoscape from "cytoscape";

const GraphWorkspace = () => {
  const cyRef = useRef(null);

  useEffect(() => {
    // Initialize Cytoscape
    cyRef.current = Cytoscape({
      container: document.getElementById("cy"), // HTML container
      elements: [
        { data: { id: "1", label: "Node 1" } },
        { data: { id: "2", label: "Node 2" } },
        { data: { id: "3", label: "Node 3" } },
        { data: { id: "4", label: "Node 4" } },
        { data: { source: "1", target: "2" } },
        { data: { source: "2", target: "3" } },
        { data: { source: "3", target: "4" } },
      ],
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#E87474",
            "label": "data(label)",
            "text-outline-color": "#1e1e2f",
            "text-outline-width": 2,
            "color": "#fff",
            "font-size": "10px",
          },
        },
        {
          selector: "edge",
          style: {
            "width": 2,
            "line-color": "#aaa",
            "target-arrow-color": "#aaa",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
          },
        },
      ],
      layout: {
        name: "cose",
        animate: true,
      },
    });

    return () => {
      // Cleanup Cytoscape instance on unmount
      cyRef.current.destroy();
    };
  }, []);

  return (
    <div id="cy" style={{ width: "100%", height: "100vh", background: "#1e1e2f" }}></div>
  );
};

export default GraphWorkspace;
