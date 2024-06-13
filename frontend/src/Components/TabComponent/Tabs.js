import React, { useState } from "react";
import TabNavItem from "./TabNavItem.js";
import TabContent from "./TabContent.js";
import LeafletComponent from './LeafletComponent.js';

const Tabs = () => {
  const [activeTab, setActiveTab] = useState("leaflet");
 
  return (
    <div className="Tabs">
      <ul className="nav">
        <TabNavItem title="Leaflet" id="leaflet" activeTab={activeTab} setActiveTab={setActiveTab}/> 
        <TabNavItem title="Mapbox" id="mapbox" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="OpenLayers" id="openlayers" activeTab={activeTab} setActiveTab={setActiveTab}/>
      </ul>
 
      <div className="outlet">
        <TabContent id="leaflet" activeTab={activeTab}>
          <LeafletComponent></LeafletComponent>
        </TabContent>
        <TabContent id="mapbox" activeTab={activeTab}>
          <p>Mapbox works!</p>
        </TabContent>
        <TabContent id="openlayers" activeTab={activeTab}>
          <p>OpenLayers works!</p>
        </TabContent>
      </div>
    </div>
  );
};

export default Tabs;
