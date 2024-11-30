import React, { useState } from "react";
import GraphWorkspace from "./components/GraphWorkspace";
import Toolbar from "./components/Toolbar";
import SidePanel from "./components/SidePanel";

const App = () => {
  const [selectedNode, setSelectedNode] = useState(null);

  return (
    <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
      <GraphWorkspace onNodeSelect={setSelectedNode} />
      <Toolbar />
      <SidePanel selectedNode={selectedNode} />
    </div>
  );
};

export default App;
