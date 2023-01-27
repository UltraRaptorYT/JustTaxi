// let safe = true
let safe = false;

document.querySelector(
  "#container"
).style.backgroundImage = `radial-gradient(circle at center, transparent 70%, var(${
  safe ? "--safe" : "--unsafe"
}))`;

var tripInfo = [
  "acceleration_x_mean",
  "acceleration_x_max",
  "acceleration_x_min",
  "acceleration_x_std",
  "acceleration_x_25%",
  "acceleration_x_75%",
  "acceleration_y_mean",
  "acceleration_y_max",
  "acceleration_y_min",
  "acceleration_y_std",
  "acceleration_y_25%",
  "acceleration_y_75%",
  "acceleration_z_mean",
  "acceleration_z_max",
  "acceleration_z_min",
  "acceleration_z_std",
  "acceleration_z_25%",
  "acceleration_z_75%",
  "gyro_x_mean",
  "gyro_x_max",
  "gyro_x_min",
  "gyro_x_std",
  "gyro_x_25%",
  "gyro_x_75%",
  "gyro_y_mean",
  "gyro_y_max",
  "gyro_y_min",
  "gyro_y_std",
  "gyro_y_25%",
  "gyro_y_75%",
  "gyro_z_mean",
  "gyro_z_max",
  "gyro_z_min",
  "gyro_z_std",
  "gyro_z_25%",
  "gyro_z_75%",
  "second_mean",
  "second_max",
  "second_min",
  "second_std",
  "second_25%",
  "second_75%",
  "speed (km/h)_mean",
  "speed (km/h)_max",
  "speed (km/h)_min",
  "speed (km/h)_std",
  "speed (km/h)_25%",
  "speed (km/h)_75%",
  "yaw_mean",
  "yaw_max",
  "yaw_min",
  "yaw_std",
  "yaw_25%",
  "yaw_75%",
  "pitch_mean",
  "pitch_max",
  "pitch_min",
  "pitch_std",
  "pitch_25%",
  "pitch_75%",
  "roll_mean",
  "roll_max",
  "roll_min",
  "roll_std",
  "roll_25%",
  "roll_75%",
  "turning_force_mean",
  "turning_force_max",
  "turning_force_min",
  "turning_force_std",
  "turning_force_25%",
  "turning_force_75%",
  "acceleration_mean",
  "acceleration_max",
  "acceleration_min",
  "acceleration_std",
  "acceleration_25%",
  "acceleration_75%",
];

for (i of tripInfo) {
  document.querySelector("#tripInfo").innerHTML += `<p>${i}:<br/>0</p>`;
}

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
  map["doubleClickZoom"].disable();
  map["boxZoom"].disable();
});
navigator.geolocation.watchPosition(function (position) {
  var lat = position.coords.latitude;
  var lng = position.coords.longitude;
  var heading = position.coords.heading;

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
