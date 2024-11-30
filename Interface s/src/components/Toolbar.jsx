import React from "react";

const Toolbar = ({ cy }) => {
  const handleZoomIn = () => {
    cy.zoom(cy.zoom() + 0.1);
  };

  const handleZoomOut = () => {
    cy.zoom(cy.zoom() - 0.1);
  };

  const handleFit = () => {
    cy.fit();
  };

  const handleExport = () => {
    const pngData = cy.png();
    const link = document.createElement("a");
    link.href = pngData;
    link.download = "graph.png";
    link.click();
  };

  return (
    <div style={{ position: "absolute", top: 10, left: 10, zIndex: 1000 }}>
      <button onClick={handleZoomIn}>Zoom In</button>
      <button onClick={handleZoomOut}>Zoom Out</button>
      <button onClick={handleFit}>Fit</button>
      <button onClick={handleExport}>Export</button>
    </div>
  );
};

export default Toolbar;
