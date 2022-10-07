$(document).ready(function () {
    var lat = 46.227638;
    var lon = 2.213749;
    var myMap = null;

    function initMap() {
        myMap = L.map('map').setView([lat, lon], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
            attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
            minZoom: 1,
            maxZoom: 20,
            name: 'tiles',
        }).addTo(myMap);
        let i = 0;
        loadedCities.forEach(city => {
            if (i < 100) {
                var marker = L.marker([city.lat, city.lon]).addTo(myMap);
            }
            i++;
            // Nous ajoutons la popup. A noter que son contenu (ici la variable ville) peut être du HTML
            //marker.bindPopup(ville);
        });
    }

    window.onload = function () {
        initMap();
    };
});