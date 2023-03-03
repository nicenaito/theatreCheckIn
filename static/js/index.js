var map;
var service;
var infowindow;
var lat = 35.689611;
var lng = 139.6983826;

function initMap() {
    function success(pos) {
        lat = pos.coords.latitude;
        lng = pos.coords.longitude;
    }
    function fail(error) {
        alert('位置情報の取得に失敗しました。エラーコード：' + error.code);
        lat = 35.689611;
        lng = 139.6983826;
        var latlng = new google.maps.LatLng(35.6812405, 139.7649361); //東京駅
    }
    navigator.geolocation.getCurrentPosition(success, fail);
}
window.initMap = initMap;

function searchTheatre() {
    function success(pos) {
        lat = pos.coords.latitude;
        lng = pos.coords.longitude;
    }
    function fail(error) {
        alert('位置情報の取得に失敗しました。エラーコード：' + error.code);
        lat = 35.689611;
        lng = 139.6983826;
        var latlng = new google.maps.LatLng(35.6812405, 139.7649361); //東京駅
    }
    navigator.geolocation.getCurrentPosition(success, fail);

    var sydney = new google.maps.LatLng(lat, lng);

    infowindow = new google.maps.InfoWindow();

    map = new google.maps.Map(
        document.getElementById('map'), { radius: 5000 });

    var search_text = document.getElementById('id_search');

    var request = {
        query: search_text.value,
        location: sydney,
        radius: '5000',
        type: 'movie_theater'
    };

    service = new google.maps.places.PlacesService(map);
    service.textSearch(request, callback);

    function callback(results, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            // selectタグのID取得
            var select = document.getElementById('id_theatre');
            while (select.firstChild) {
                select.removeChild(select.firstChild);
            }
            // removeChild(select);
            for (var i = 0; i < results.length; i++) {
                var place = results[i];
                // option要素の宣言
                var option = document.createElement('option');
                // option要素のvalue属性に値をセット
                option.setAttribute('value', results[i].name);
                // option要素に値をセット
                option.innerHTML = results[i].name;
                // 作成したoption要素をselectタグに追加
                select.appendChild(option);
                console.log(select);
            }
        }
    }
}
window.searchTheatre = searchTheatre;
