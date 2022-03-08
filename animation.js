import WbWorld from 'https://cyberbotics.com/wwi/R2022b/nodes/WbWorld.js';

function sceneIsReady() {
  console.log("Scene is ready");
}

function displayViewpoint() {
  let webotsView = document.getElementsByTagName('webots-view')[0];
  if (typeof WbWorld.instance === 'undefined') {
    console.log("No world instance.");
    return;
  }
  let object = WbWorld.instance.nodes.get('n266');
  if (object) {
    console.log("Found Transform");
    console.log(object.rotation.toString())
  } else
    console.log("No Transform found");
  object = WbWorld.instance.viewpoint;
  if (object) {
    console.log("Viewpoint orientation = " + object.orientation.toString())
    console.log("Viewpoint position = " + object.position.toString())
  } else
    console.log("No Viewpoint found");
}

window.addEventListener('DOMContentLoaded', (event) => {
  let webotsView = document.getElementsByTagName('webots-view')[0];
  webotsView.onready = sceneIsReady;
});
