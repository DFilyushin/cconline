ymaps.ready(init);

function init () {
    var myMap = new ymaps.Map('map', {
            center: [52.18, 76.57],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        }),
        objectManager = new ymaps.ObjectManager({
            clusterize: true,
            gridSize: 64,
            hasBalloon: false,  
            hasHint: false,
            clusterDisableClickZoom: true
        });
    objectManager.objects.options.set('preset', 'islands#blueCircleDotIcon');
    objectManager.clusters.options.set('preset', 'islands#lightBlueClusterIcons');
    myMap.geoObjects.add(objectManager);
    var url = new URL(window.location.href);
    var c = url.searchParams.get("year");
    if (!c){
        c = (new Date()).getFullYear();
    }
    $.ajax({
        url: "/get_map?year=" + c
    }).done(function(data) {
        objectManager.add(data);
    });

}