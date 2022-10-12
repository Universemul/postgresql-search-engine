$(document).ready(function () {
    var lat = 48.866667;
    var lon = 2.333333;
    var myMap = null;
    var defaultRadius = 10000; // 10km
    var circle = null;
    var citiesLayer = L.layerGroup();

    function initMap() {
        myMap = L.map('map').setView([lat, lon], 9);
        L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
            attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
            minZoom: 1,
            maxZoom: 20,
            name: 'tiles',
        }).addTo(myMap);
        circle = drawCircle(myMap, lat, lon, defaultRadius);
        citiesLayer.addTo(myMap);
    }

    window.onload = function () {
        initMap();
        $("#spatial_search_btn").click(function () {
            var radius = $("#radius_input").val() * 1000; // convert to meters
            var coordinate = circle.getLatLng();
            updateCircle(circle, radius, coordinate.lat, coordinate.lng);
            citiesLayer.clearLayers();
            getCities(myMap, citiesLayer, coordinate.lat, coordinate.lng, circle.getRadius());
        });
        myMap.on("moveend", function (e) {
            var center = myMap.getCenter();
            updateCircle(circle, circle.getRadius(), center.lat, center.lng);
            citiesLayer.clearLayers();
            getCities(myMap, citiesLayer, center.lat, center.lng, circle.getRadius());
        });
    };
});

function updateCircle(circle, radius, lat, lon) {
    circle.setRadius(radius);
    circle.setLatLng([lat, lon]);
}

function drawCircle(myMap, lat, lon, radius) {
    var circle = L.circle([lat, lon], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: radius,
    });
    circle.addTo(myMap);
    return circle;
}

function addCitiesToMap(map, citiesLayer, cities) {
    cities.forEach(city => {
        var marker = L.marker([city.lat, city.lon]).bindTooltip(city.name);
        citiesLayer.addLayer(marker);
    });
}

function getCities(myMap, citiesLayer, lat, lon, radius) {
    $.ajax({
        type: "GET",
        url: "getCities/" + lat + "/" + lon + "/" + radius,
        dataType: "json",
        encode: true,
    }).done(function (data) {
        addCitiesToMap(myMap, citiesLayer, data);
    });
}