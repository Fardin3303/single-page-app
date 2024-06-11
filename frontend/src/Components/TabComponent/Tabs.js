import React, { useState } from "react";
import TabNavItem from "./TabNavItem.js";
import TabContent from "./TabContent.js";
import LeafletComponent from './LeafletComponent.js';
import Login from '../Auth/Login';
import PointsList from '../Points/PointsList';
import PointForm from '../Points/PointForm';
 
const Tabs = () => {
  const [activeTab, setActiveTab] = useState("mapbox");
 
  return (
    <div className="Tabs">
      <ul className="nav">
        <TabNavItem title="Mapbox" id="mapbox" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="Leaflet" id="leaflet" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="OpenLayers" id="openlayers" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="ArcGIS" id="arcgis" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="Carto" id="carto" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="Login" id="login" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="Points" id="points" activeTab={activeTab} setActiveTab={setActiveTab}/>
        <TabNavItem title="Create Point" id="create-point" activeTab={activeTab} setActiveTab={setActiveTab}/>
      </ul>
 
      <div className="outlet">
        <TabContent id="mapbox" activeTab={activeTab}>
          <p>Mapbox works!</p>
        </TabContent>
        <TabContent id="leaflet" activeTab={activeTab}>
          <LeafletComponent></LeafletComponent>
        </TabContent>
        <TabContent id="openlayers" activeTab={activeTab}>
          <p>OpenLayers works!</p>
        </TabContent>
        <TabContent id="arcgis" activeTab={activeTab}>
          <p>ArcGIS works!</p>
        </TabContent>
        <TabContent id="carto" activeTab={activeTab}>
          <p>Carto works!</p>
        </TabContent>
        <TabContent id="login" activeTab={activeTab}>
          <Login />
        </TabContent>
        <TabContent id="points" activeTab={activeTab}>
          <PointsList />
        </TabContent>
        <TabContent id="create-point" activeTab={activeTab}>
          <PointForm />
        </TabContent>
      </div>
    </div>
  );
};

export default Tabs;
