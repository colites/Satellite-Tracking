// ================================
// Input Page Dynamic UI Manipulation Functions
// ================================

async function SendCoordinates(latitude, longitude){

    const data = {
        latitude: latitude,
        longitude: longitude
  };

    const response = await fetch(`http://127.0.0.1:5001/send-coordinates`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const newform = document.querySelector("#input_container");
    newform.innerHTML = `
          <h1>  Coordinates failed to send because I dont want to use up my precious API transactions till the final project so this will just echo</h1>
          <p>Latitude: ${latitude}</p>
          <p>Longitude: ${longitude}</p>
          <button type="button" onclick="back()">Back</button>
    `
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
