// var safe = true
var safe = false;

var data = {
  accuracy: [],
  bearing: [],
  acceleration_x: [],
  acceleration_y: [],
  acceleration_z: [],
  gyro_x: [],
  gyro_y: [],
  gyro_z: [],
  second: [0],
  "speed (km/h)": [],
  yaw: [],
  pitch: [],
  roll: [],
  turning_force: [],
  acceleration: [],
};

var startTime = new Date();

var agg = ["mean", "max", "min", "std", "25", "75"];

var tripInfo = [
  "accuracy",
  "bearing",
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
    <th class="border border-slate-600 whitespace-nowrap">&nbsp;</th>
    <th class="border border-slate-600 whitespace-nowrap">Mean</th>
    <th class="border border-slate-600 whitespace-nowrap">Max</th>
    <th class="border border-slate-600 whitespace-nowrap">Min</th>
    <th class="border border-slate-600 whitespace-nowrap">Std</th>
    <th class="border border-slate-600 whitespace-nowrap">25%</th>
    <th class="border border-slate-600 whitespace-nowrap">75%</th>
  </tr>
</thead>
<tbody>`;
for (i of tripInfo) {
  startString += `<tr id="${i}">
    <th class="border border-slate-600 whitespace-nowrap">${i}</th>
    <td class="border border-slate-600 whitespace-nowrap" data-value="mean">0</td>
    <td class="border border-slate-600 whitespace-nowrap" data-value="max">0</td>
    <td class="border border-slate-600 whitespace-nowrap" data-value="min">0</td>
    <td class="border border-slate-600 whitespace-nowrap" data-value="std">0</td>
    <td class="border border-slate-600 whitespace-nowrap" data-value="25">0</td>
    <td class="border border-slate-600 whitespace-nowrap" data-value="75">0</td>
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

navigator.geolocation.watchPosition(
  function (position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    var heading = position.coords.heading;
    // console.log(position);
    var speed = position.coords.speed; // Metre per Second
    data["speed (km/h)"].push(speed * 3.6);
    var accuracy = position.coords.accuracy;
    data["accuracy"].push(accuracy);
    data["bearing"].push(heading);
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
  },
  (err) => {
    console.error(`ERROR(${err.code}): ${err.message}`);
  },
  {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0,
  }
);

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
  document.querySelector("#container").classList.add(safe ? "safe" : "unsafe");
  document
    .querySelector("#container")
    .classList.remove(safe ? "unsafe" : "safe");
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
    Math.atan(
      event.accelerationIncludingGravity.y /
        Math.sqrt(
          Math.pow(event.accelerationIncludingGravity.x, 2) +
            Math.pow(event.accelerationIncludingGravity.z, 2)
        )
    );

  data.yaw.push(yaw);
  data.pitch.push(pitch);
  data.roll.push(roll);
  data.turning_force.push(yaw * pitch * roll);
}

let gyroscope = new Gyroscope({ frequency: 60 });

gyroscope.addEventListener("reading", (e) => {
  data.gyro_x.push(gyroscope.x);
  data.gyro_y.push(gyroscope.y);
  data.gyro_z.push(gyroscope.z);
});
gyroscope.start();

const asc = (arr) => arr.sort((a, b) => a - b);

const sum = (arr) => arr.reduce((a, b) => a + b, 0);

const mean = (arr) => sum(arr) / arr.length;

const std = (arr) => {
  const mu = mean(arr);
  const diffArr = arr.map((a) => (a - mu) ** 2);
  return Math.sqrt(sum(diffArr) / (arr.length - 1));
};

const quantile = (arr, q) => {
  const sorted = asc(arr);
  const pos = (sorted.length - 1) * q;
  const base = Math.floor(pos);
  const rest = pos - base;
  if (sorted[base + 1] !== undefined) {
    return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
  } else {
    return sorted[base];
  }
};

setInterval(() => {
  data.second.push(parseInt([...data.second].splice(-1)) + 1);
  for (i of tripInfo) {
    var Q1 = quantile(data[i], 0.25);
    var Q3 = quantile(data[i], 0.75);
    document.getElementById(i).querySelector("[data-value='min']").textContent =
      Math.min.apply(Math, data[i]) == null ||
      isNaN(Math.min.apply(Math, data[i]))
        ? 0
        : Math.min.apply(Math, data[i]).toFixed(3);
    document.getElementById(i).querySelector("[data-value='25']").textContent =
      Q1 == null || isNaN(Q1) ? 0 : Q1.toFixed(3);
    document.getElementById(i).querySelector("[data-value='75']").textContent =
      Q3 == null || isNaN(Q3) ? 0 : Q3.toFixed(3);
    document.getElementById(i).querySelector("[data-value='max']").textContent =
      Math.max.apply(Math, data[i]) == null ||
      isNaN(Math.max.apply(Math, data[i]))
        ? 0
        : Math.max.apply(Math, data[i]).toFixed(3);
    document
      .getElementById(i)
      .querySelector("[data-value='mean']").textContent =
      mean(data[i]) == null || isNaN(mean(data[i]))
        ? 0
        : mean(data[i]).toFixed(3);
    document.getElementById(i).querySelector("[data-value='std']").textContent =
      std(data[i]) == null || isNaN(std(data[i])) ? 0 : std(data[i]).toFixed(3);
  }
}, 1000);

document.getElementById("saveData").addEventListener("click", () => {
  csvData = tableToCSV();
  downloadCSVFile(csvData);
});

var pointer = document.getElementById("pointer");
var mapContainer = document.getElementById("map-container");

const bookingIDLength = 10;
const letters = "0123456789";
function uniqueId() {
  var text = "";
  for (var i = 0; i < bookingIDLength; i++) {
    text += letters.charAt(Math.floor(Math.random() * letters.length));
  }
  return text;
}
var bookingID = uniqueId();
function tableToCSV() {
  // Variable to store the final csv data
  var csv_data = [];
  var columnName = ["bookingID"];
  var dataRow = [bookingID];
  for (i of tripInfo) {
    for (var value of agg) {
      columnName.push(`${i}_${value}`);
      dataRow.push(
        document
          .getElementById(i)
          .querySelector(`[data-value='${value}']`)
          .textContent.includes("Infinity")
          ? 0
          : parseFloat(
              document
                .getElementById(i)
                .querySelector(`[data-value='${value}']`).textContent
            )
      );
    }
  }
  csv_data.push(columnName.join(","));
  csv_data.push(dataRow.join(","));

  csv_data = csv_data.join("\n");
  // console.log(csv_data);
  return csv_data;
}

function downloadCSVFile(csv_data) {
  // Create CSV file object and feed our
  // csv_data into it
  CSVFile = new Blob([csv_data], { type: "text/csv" });

  // Create to temporary link to initiate
  // download process
  var temp_link = document.createElement("a");

  // Download csv file
  temp_link.download = "driving.csv";
  var url = window.URL.createObjectURL(CSVFile);
  temp_link.href = url;

  // This link should not be displayed
  temp_link.style.display = "none";
  document.body.appendChild(temp_link);

  // Automatically click the link to trigger download
  temp_link.click();
  document.body.removeChild(temp_link);
}

mapContainer.addEventListener("click", () => {
  if (mapContainer.dataset.good == "None") {
    console.log("Ho");
  } else {
    setTimeout(() => {
      pointer.classList.add(
        mapContainer.dataset.good == "True" ? "safe" : "unsafe"
      );
      document
        .querySelector("#container")
        .classList.add(mapContainer.dataset.good == "True" ? "safe" : "unsafe");
      document
        .querySelector("#container")
        .classList.remove(
          mapContainer.dataset.good == "True" ? "unsafe" : "safe"
        );
      document.getElementById("container");
      document.getElementById("state").textContent =
        mapContainer.dataset.good == "True" ? "Safe" : "Unsafe";
      setTimeout(() => {
        pointer.classList.add("osc");
      }, 3500);
    }, 2000);
  }
});

setInterval(() => {
  axios
    .post("https://justtaxi.onrender.com/predict", { csvData: tableToCSV() })
    .then((result) => {
      var prob = result.data.replace("[[", "").replace("]]", "");
      prob = prob.split(" ");
      var safeProb = prob[0];
      var unsafeProb = prob[1];
      var finalProb = Math.max(safeProb, unsafeProb);
      if (finalProb == safeProb) {
        document.getElementById("proba").textContent = (
          finalProb * 100
        ).toFixed(2);
        document.querySelector("#container").classList.add("safe");
        document.querySelector("#container").classList.remove("unsafe");
        document.getElementById("pointer").style.rotate =
          finalProb * 100 + "deg";
      } else {
        document.getElementById("proba").textContent = (
          -finalProb * 100
        ).toFixed(2);
        document.querySelector("#container").classList.remove("safe");
        document.querySelector("#container").classList.add("unsafe");
        document.getElementById("pointer").style.rotate =
          -(finalProb * 100) + "deg";
      }
    })
    .catch(() => {});
}, 500);
