let map;
let pins;
let pos;
let marker;

function GetMap()
{
    map = new Microsoft.Maps.Map('#myMap');

    navigator.geolocation.getCurrentPosition((position)=> {
        map = new Microsoft.Maps.Map('#myMap', {center: new Microsoft.Maps.Location(position.coords.latitude, position.coords.longitude), zoom:18, disableStreetside: true})
    });
    marker = new Microsoft.Maps.Pushpin(map.getCenter(), {
        icon: window.static + "/marker.png"
    });
    map.entities.push(marker);
    navigator.geolocation.watchPosition((position) => {
        marker.setLocation(new Microsoft.Maps.Location(
                    position.coords.latitude,
                    position.coords.longitude));
        pos = [position.coords.latitude, position.coords.longitude]
    })
    GeneratePins();
    setInterval(function() {
        GeneratePins();
    }, 300000);
    WaterFountainCheck(document.getElementById("type"));
}

function AddPin() {
    document.getElementById("button").style.display = "none";

    navigator.geolocation.getCurrentPosition((position) => {
        pos = [position.coords.latitude, position.coords.longitude]
        fetch('http://127.0.0.1:5000/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"latitude": pos[0], "longitude": pos[1], "type": GetType()})
        }).then(data => data.json().then(async (value) => {
            if (value["result"] === "spam") {
                alert("There is already an object here");
            } else {
                GeneratePins();
            }
            document.getElementById("button").style.display = "block";
        }))
    }, (error) => console.log(error))
}

function GetType() {
    console.log(document.getElementById("type").checked)
    if (!document.getElementById("type").checked) {
        return "1" + (document.getElementById("1").checked ? "0" : "1") + (document.getElementById("2").checked ? "0" : "1") + "0";
    }
    return "0" + (document.getElementById("1").checked ? "0" : "1") + (document.getElementById("2").checked ? "0" : "1") + (document.getElementById("3").checked ? "0" : "1");
}

async function MoveMap(seconds, location)
{
    center = map.getCenter();
    for (let index = 0; index < seconds * 40; index++) {
        await new Promise(r => setTimeout(r, 25));
        map.setView({center: new Microsoft.Maps.Location(Lerp(center.latitude, location[0], (index+1)/(seconds*40)), Lerp(center.longitude, location[1], (index+1)/(seconds*40)))})
    }
}

function Lerp(oldValue, newValue, t) {
    return oldValue + t*(newValue-oldValue)
}

async function GeneratePins() {
    navigator.geolocation.getCurrentPosition((position) => {
        pos = [position.coords.latitude, position.coords.longitude]
        fetch('http://127.0.0.1:5000/near?' + new URLSearchParams( {
        "latitude": pos[0],
        "longitude": pos[1]
    }), {method: 'GET'}).then(data=>data.json().then(value => {
        pins = value["data"];
        map.entities.clear();
        map.entities.push(marker);
        document.getElementById("abcd").replaceChildren();
        pins.forEach(element => {
            var type = element[2][0] === "0" ? "Trashcan" : "Water Fountain";
            var a = document.getElementById("a").cloneNode();
            var b = document.getElementById("b").cloneNode();
            document.getElementById("abcd").appendChild(a);
            a.appendChild(b);
            var c = document.getElementById("c").cloneNode();
            b.appendChild(c);
            var d = document.getElementById("d").cloneNode();
            d.src = window.static + "/" + element[2] + ".png";
            b.appendChild(d);
            c.textContent = type + " #" + element[3].toString();
            b.style.display = 'block';
            b.addEventListener("click", function(e) {
                MoveMap(0.3, [element[0], element[1]])
            })
            var pin = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(element[0], element[1]), {
                title: type,
                icon: window.static + "/" + element[2] + ".png"
            });
            map.entities.push(pin);
        });
    }))
    }, (error) => console.log(error))
}

function WaterFountainCheck(element) {
    if (!element.checked) {
        const a = document.getElementById("typeimg");
        a.src = window.static + "/1000.png";
        a.title = "Switch to adding a trashcan"
        const b = document.getElementById("1img");
        b.src = window.static + "/1100.png";
        b.title = "Can you fill water bottles here?"
        const c = document.getElementById("2img");
        c.src = window.static + "/1010.png";
        c.title = "Can pets drink water here?"
        document.getElementById("3").parentElement.style.display = "none";
    }
    else {
        const a = document.getElementById("typeimg");
        a.src = window.static + "/0100.png";
        a.title = "Switch to adding a water fountain"
        const b = document.getElementById("1img");
        b.src = window.static + "/0100.png";
        b.title = "Can you put things in landfill here?"
        const c = document.getElementById("2img");
        c.src = window.static + "/0010.png";
        c.title = "Can you recycle things here?"
        document.getElementById("3").parentElement.style.display = "block";
    }
}