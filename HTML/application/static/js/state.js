// var safe = true
var safe = false;

var data = {
  acceleration_x: [],
  acceleration_y: [],
  acceleration_z: [],
  gyro_x: [],
  gyro_y: [],
  gyro_z: [],
  second: [],
  "speed (km/h)": [],
  yaw: [],
  pitch: [],
  roll: [],
  turning_force: [],
  acceleration: [],
};

var startTime = new Date();

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
  var speed = position.coords.speed; // Metre per Second
  data["speed (km/h)"].push(speed * 3.6);
  // Update the map's view to center on the user's location
  map.setCenter([lng, lat]);

  // Display the user's location and direction on the map
  const player = document.createElement("div");
  player.style.backgroundImage = `url(https://media.discordapp.net/attachments/910885868733087747/1068527441720647840/image-removebg-preview.png)`;
  player.id = `playerChar`;
  player.style.minWidth = `10px`;
  player.style.maxWidth = `50px`;
  player.style.width = `10vw`;
  player.style.aspectRatio = `1`;
  player.style.backgroundSize = `100%`;
  player.style.zIndex = `99`;
  if (document.querySelectorAll("#playerChar").length >= 1) {
    document.querySelectorAll("#playerChar")[0].remove();
  }
  var marker = new mapboxgl.Marker(player, { anchor: "bottom" })
    .setLngLat([lng, lat])
    .addTo(map);
  marker.setRotation(heading);
  map.setBearing(heading);
});

var measureArr = document.querySelectorAll(".measure");
var size = 0;
for (var ele of measureArr) {
  size +=
    ele.clientHeight +
    parseFloat(getComputedStyle(ele).marginTop) +
    parseFloat(getComputedStyle(ele).marginBottom);
}
var elementHeight = document.getElementById("container").clientHeight;

var computedStyle = getComputedStyle(document.getElementById("container"));
elementHeight -=
  parseFloat(computedStyle.paddingTop) +
  parseFloat(computedStyle.paddingBottom);

document
  .querySelector("#map-container")
  .classList.add(`max-h-[${elementHeight - size}px]`);

document.getElementById("tripInfo").addEventListener("click", () => {
  safe = !safe;
  document.querySelector(
    "#container"
  ).style.backgroundImage = `radial-gradient(circle at center, transparent 70%, var(${
    safe ? "--safe" : "--unsafe"
  }))`;
});

if (window.DeviceMotionEvent) {
  window.addEventListener("devicemotion", motion, false);
} else {
  console.log("DeviceMotionEvent is not supported");
}
function motion(event) {
  data.acceleration_x.push(event.accelerationIncludingGravity.x);
  data.acceleration_y.push(event.accelerationIncludingGravity.y);
  data.acceleration_z.push(event.accelerationIncludingGravity.z);
  yaw =
    180 *
    Math.atan(
      event.accelerationIncludingGravity.z /
        Math.sqrt(
          Math.pow(event.accelerationIncludingGravity.x, 2) +
            Math.pow(event.accelerationIncludingGravity.z, 2)
        )
    );
  pitch =
    180 *
    Math.atan(
      event.accelerationIncludingGravity.z /
        Math.sqrt(
          Math.pow(event.accelerationIncludingGravity.x, 2) +
            Math.pow(event.accelerationIncludingGravity.z, 2)
        )
    );
  roll =
    180 *
    np.arctan(
      event.accelerationIncludingGravity.y /
        (event.accelerationIncludingGravity.x ** 2 +
          event.accelerationIncludingGravity.z ** 2) **
          (1 / 2)
    );

  data.yaw.push(yaw);
  data.pitch.push(pitch);
  data.roll.push(roll);
  data.turning_force.push(yaw * pitch * roll)
}

let gyroscope = new Gyroscope({ frequency: 60 });

gyroscope.addEventListener("reading", (e) => {
  data.gyro_x.push(gyroscope.x);
  data.gyro_y.push(gyroscope.y);
  data.gyro_z.push(gyroscope.z);
  console.log(data);
});
gyroscope.start();

setInterval(() => {
  data.second.push(Date.now() - startTime);
  console.log(data);
}, 1000);
