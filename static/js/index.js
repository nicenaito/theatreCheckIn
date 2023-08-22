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
    }
    navigator.geolocation.getCurrentPosition(success, fail);

    const options = {
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: ''
        }
      };

    async function fetchData() {
        const data = await fetch('https://api.foursquare.com/v3/places/search?categories=10024', options);
        console.log(data);
        const res = await data.json();
        console.log(res.results.length);
        console.log(res.results);
        // selectタグのID取得
        var select = document.getElementById('id_theatre');
        while (select.firstChild) {
            select.removeChild(select.firstChild);
        }
        for (var item in res.results){
            console.log(res.results[item].name);
            if (res.results.length >= 1) {
                // option要素の宣言
                var option = document.createElement('option');
                // option要素のvalue属性に値をセット
                option.setAttribute('value', res.results[item].name);
                // option要素に値をセット
                option.innerHTML = res.results[item].name;
                // 作成したoption要素をselectタグに追加
                select.appendChild(option);
                console.log(select);
            }
        }
    }

    fetchData()
}
window.searchTheatre = searchTheatre;
