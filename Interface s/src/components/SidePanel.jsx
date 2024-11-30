import React, { useState } from "react";

const SidePanel = ({ selectedNode }) => {
  if (!selectedNode) {
    return null;
  }

  return (
    <div style={{ position: "absolute", top: 0, right: 0, width: "300px", height: "100%", background: "#333", color: "#fff", padding: "10px" }}>
      <h3>Node Details</h3>
      <p><strong>ID:</strong> {selectedNode.data("id")}</p>
      <p><strong>Label:</strong> {selectedNode.data("label")}</p>
      {/* Add more details as needed */}
    </div>
  );
};

export default SidePanel;
