// let safe = true
let safe = false;

document.querySelector(
  "#container"
).style.backgroundImage = `radial-gradient(circle at center, transparent 70%, var(${
  safe ? "--safe" : "--unsafe"
}))`;

var tripInfo = [
  "acceleration_x",
  "acceleration_y",
  "acceleration_z",
  "gyro_x",
  "gyro_y",
  "gyro_z",
  "second",
  "speed (km/h)",
  "yaw",
  "pitch",
  "roll",
  "turning_force",
  "acceleration",
];
var startString = `<table class="table-auto border-collapse border border-slate-500 w-full" id="tripTable">
<thead>
  <tr>
    <th class="border border-slate-600">&nbsp;</th>
    <th class="border border-slate-600">Min</th>
    <th class="border border-slate-600">25%</th>
    <th class="border border-slate-600">Medium</th>
    <th class="border border-slate-600">75%</th>
    <th class="border border-slate-600">Max</th>
    <th class="border border-slate-600">Mean</th>
    <th class="border border-slate-600">Std</th>
  </tr>
</thead>
<tbody>`;
for (i of tripInfo) {
  startString += `<tr>
    <th class="border border-slate-600">${i}</th>
    <td class="border border-slate-600">0</td>
    <td class="border border-slate-600">0</td>
    <td class="border border-slate-600">0</td>
    <td class="border border-slate-600">0</td>
    <td class="border border-slate-600">0</td>
    <td class="border border-slate-600">0</td>
    <td class="border border-slate-600">0</td>
  </tr>`;
}
startString += "</tbody></table>";

document.getElementById("tripInfo").innerHTML = startString;

mapboxgl.accessToken =
  "pk.eyJ1IjoidWx0cmFyYXB0b3IiLCJhIjoiY2t0cGo5aThxMGFxMzJybXBiNmZ3bWY4eSJ9.q24IUWxYYm6DhTDn5pY2Rg";
const map = new mapboxgl.Map({
  container: "map",
  // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
  style: "mapbox://styles/mapbox/streets-v12",
  zoom: 18,
});
map.on("load", () => {
  map["scrollZoom"].disable();
  map["dragPan"].disable();
  map["dragRotate"].disable();
  map["touchZoomRotate"].disable();
  map["doubleClickZoom"].disable();
  map["boxZoom"].disable();
});
navigator.geolocation.watchPosition(function (position) {
  var lat = position.coords.latitude;
  var lng = position.coords.longitude;
  var heading = position.coords.heading;
  console.log(position);
  // Update the map's view to center on the user's location
  map.setCenter([lng, lat]);

  // Display the user's location and direction on the map
  const player = document.createElement("div");
  player.style.backgroundImage = `url(https://cdn.discordapp.com/attachments/995303058131128371/995417061041901568/Yellow_Corn_2.png)`;
  player.id = `playerChar`;
  player.style.minWidth = `10px`;
  player.style.maxWidth = `50px`;
  player.style.width = `10vw`;
  player.style.aspectRatio = `3/4`;
  player.style.backgroundSize = `100%`;
  player.style.zIndex = `99`;
  var marker = new mapboxgl.Marker(player, { anchor: "bottom" })
    .setLngLat([lng, lat])
    .addTo(map);
  marker.setRotation(heading);
  alert(heading);
  map.setBearing(heading);
});

var measureArr = document.querySelectorAll(".measure");
var size = 0;
for (var ele of measureArr) {
  size +=
    ele.clientHeight +
    parseFloat(getComputedStyle(ele).marginTop) +
    parseFloat(getComputedStyle(ele).marginBottom);
  console.log(ele.clientHeight);
}
var elementHeight = document.getElementById("container").clientHeight;

var computedStyle = getComputedStyle(document.getElementById("container"));
elementHeight -=
  parseFloat(computedStyle.paddingTop) +
  parseFloat(computedStyle.paddingBottom);

document
  .querySelector("#map-container")
  .classList.add(`max-h-[${elementHeight - size}px]`);
