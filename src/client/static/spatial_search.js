$(document).ready(function () {
    var lat = 46.227638;
    var lon = 2.213749;
    var myMap = null;

    function initMap() {
        myMap = L.map('map').setView([lat, lon], 8);
        L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
            attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
            minZoom: 1,
            maxZoom: 20,
            name: 'tiles',
        }).addTo(myMap);
    }

    window.onload = function () {
        initMap();
    };
});