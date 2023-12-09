// ================================
// Input Page Dynamic UI Manipulation Functions
// ================================

async function SendCoordinates(latitude, longitude){

    const data = {
        latitude: latitude,
        longitude: longitude
    };

    const response = await fetch(`https://backend-q6r6.onrender.com/send-coordinates`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    let newform = document.querySelector(".modal-content");
    if (response.status === 400) {
        alert("Please Add a latitude and a longitude");
    }

    else if(!response.ok){
        newform.innerHTML = `
            <h1> Coordinates failed to send </h1>
            <button type="button" onclick="back()">Back</button>
        `
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
    }

    else {
        const data =  await response.json();
        
        // create satellite item
        let satellitesContent = data.map(sat => {
            return `<div class="satellite-item">
                        <h4>${sat.satname}</h4>
                        <p>ID: ${sat.satid}</p>
                        <p>Latitude: ${sat.satlatitude}</p>
                        <p>Longitude: ${sat.satlongitude}</p>
                        <p>Altitude: ${sat.sataltitude}</p>
                    </div>`;
        }).join(''); 
        document.getElementById('modal').style.display = "block";
        newform.innerHTML = `
            <div id="analyzing-options">
                <div id="satellites-list">
                    ${satellitesContent}
                </div>
                <button id="map-button" onclick="makeMapOptions()">Add satellites onto a map</button>
                <button id="plot-info-button" onclick="plotInfo()">Plot satellite information on a graph or chart</button>
            </div>
        `
        
    }
}


async function plotInfo(){
    let newform = document.querySelector(".modal-content");

    newform.innerHTML = `
        <div id="plot-options">
            <div class="plot-buttons-container">
                <label for="satorbits">Categorize satellite orbits</label>
                <button type="button" onclick="calculateOrbits()">Categorize orbits</button>
            </div>
        </div>
    `
}


async function calculateOrbits(){
    
    const data = {
        type: "orbits"
    }

    const response = await fetch(`https://backend-q6r6.onrender.com/send-to-analyzer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    let newform = document.querySelector(".modal-content");
    if (!response.ok) {
        newform.innerHTML = `
            <h1> Could not fetch data, try again </h1>
            <button type="button" onclick="back()">Back</button>
        `

        throw new Error(`Server error: ${response.status_code} ${response.statusText}`);
    }
    else {
        const dataRes = await response.json();

        newform.innerHTML = `
            <h1> Satellite Orbit Results </h1>
            <canvas id="orbitChart"></canvas>
            <button type="button" onclick="back()">Back</button>
        `

        const canvas = document.getElementById('orbitChart').getContext('2d');
        const OrbitChart = new Chart(canvas, {
            type: 'bar', 
            data: dataRes
        });
    }
}


function makeMapOptions(){

    let newform = document.querySelector(".modal-content");

    newform.innerHTML = `
        <div id="map-options">
            <div id="satellite-options">
                <h1> Satellite Plotting Options</h1>
                <h2> Leave fields empty to get all satellites </h2>
                <div class="input-group">
                    <label for="satname">Search by Satellite name:</label>
                    <input type="text" id="satname" name="Satellite name" placeholder="Enter a satellite name">
                </div>
                <div class="input-group">
                    <label for="satlatitude">Search for satellites with a latitude of:</label>
                    <input type="text" id="satlatitude" name="Satellite Latitude" placeholder="Enter a satellite latitude">
                </div>
                <div class="input-group">
                    <label for="satlongitude">Search for satellites with a longitude of:</label>
                    <input type="text" id="satlongitude" name="Satellite longitude" placeholder="Enter a satellite longitude">
                </div>
                <div class="input-group">
                    <label for="sataltitude">Search for satellites with an altitude of:</label>
                    <input type="text" id="sataltitude" name="Satellite Altitude" placeholder="Enter a satellite altitude">
                </div>
            </div>
            <div id="miscellaneous-additions">
                <h3> Future stellar objects(meteorShowers, astronomical stuff, UFOS) To be added in the future</h3>
            </div>
            <div class="buttons-container">
                <button type="button" onclick="makeMap()">Add Custom Objects To Map</button>
            </div>
        </div>
    `
}


async function makeMap(){
    let satellite_data = await sendSatelliteReqs();
    
    let newform = document.querySelector(".modal-content");
    newform.innerHTML = `
            <div id="map" style="height: 400px;"></div>
            <button type="button" onclick="back()">Back</button>
        `
    
    // learned how to do this using leaflet docs, this sets up the map and adds markers for each satellite.
    let map = L.map('map').setView([0, 0], 1);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 17,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    satellite_data.forEach(satellite => {
        L.marker([satellite.satlatitude, satellite.satlongitude]).addTo(map)
            .bindPopup(`<b>${satellite.satname}</b><br>Altitude: ${satellite.sataltitude} km`);
    });
}


async function sendSatelliteReqs(){
    const latitude = document.getElementById('satlatitude').value;
    const longitude = document.getElementById('satlongitude').value;
    const name = document.getElementById('satname').value;
    const altitude = document.getElementById('sataltitude').value;

    let data;

    if (latitude === "" && longitude === "" && name === "" && altitude === ""){
        data = {
            satname: name,
            satlatitude: latitude,
            satlongitude: longitude,
            sataltitude: altitude,
            includes: "all",
            type: "map"
        }
    }
    else {
        data = {
            satname: name,
            satlatitude: latitude,
            satlongitude: longitude,
            sataltitude: altitude,
            includes: "filtered",
            type: "map"
        }
    }

    const response_data = await fetch(`https://backend-q6r6.onrender.com/send-to-analyzer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    let newform = document.querySelector(".modal-content");
    if (!response_data.ok) {
        newform.innerHTML = `
            <h1> Could not fetch data </h1>
            <button type="button" onclick="back()">Back</button>
        `
        throw new Error(`Server error: ${response_data.status} ${response_data.statusText}`);
    }

    return response_data.json();
}


function submitCoordinates(){
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    SendCoordinates(latitude,longitude);
}


function getUserLocation() {
    // geolocation API Documentation helped here
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(success, showError);
    } 
    else {
        alert("Geolocation is not supported by this browser.");
    }
  }


function success(position) {
    // geolocation API Documentation helped here
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    SendCoordinates(latitude,longitude);

}


function showError(error){
    // geolocation API Documentation helped here
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User Denied Permissions");
            break;
        case error.TIMEOUT:
            alert("Request Timed Out");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location Info Not Found");
            break;
    }
    console.warn(`ERROR(${err.code}): ${err.message}`);
}


function back(){
    window.location.href = '/';
}


function closeModal() {
    document.getElementById('modal').style.display = "none";
}