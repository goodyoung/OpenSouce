var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(37.576022, 126.9769), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption); 
console.log(`1`);


// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();
console.log(`2`);

var mapTypeControl = new kakao.maps.MapTypeControl();

// 지도에 컨트롤을 추가해야 지도위에 표시됩니다
// kakao.maps.ControlPosition은 컨트롤이 표시될 위치를 정의하는데 TOPRIGHT는 오른쪽 위를 의미합니다
map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);

// 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

var mapTypes = {
    terrain : kakao.maps.MapTypeId.TERRAIN,    
    traffic :  kakao.maps.MapTypeId.TRAFFIC,
    bicycle : kakao.maps.MapTypeId.BICYCLE,
    useDistrict : kakao.maps.MapTypeId.USE_DISTRICT
};

// 체크 박스를 선택하면 호출되는 함수입니다
function setOverlayMapTypeId() {
    var chkTerrain = document.getElementById('chkTerrain'),  
        chkTraffic = document.getElementById('chkTraffic'),
        chkBicycle = document.getElementById('chkBicycle'),
        chkUseDistrict = document.getElementById('chkUseDistrict');
    
    // 지도 타입을 제거합니다
    for (var type in mapTypes) {
        map.removeOverlayMapTypeId(mapTypes[type]);    
    }

    // 지적편집도정보 체크박스가 체크되어있으면 지도에 지적편집도정보 지도타입을 추가합니다
    if (chkUseDistrict.checked) {
        map.addOverlayMapTypeId(mapTypes.useDistrict);    
    }
    
    // 지형정보 체크박스가 체크되어있으면 지도에 지형정보 지도타입을 추가합니다
    if (chkTerrain.checked) {
        map.addOverlayMapTypeId(mapTypes.terrain);    
    }
    
    // 교통정보 체크박스가 체크되어있으면 지도에 교통정보 지도타입을 추가합니다
    if (chkTraffic.checked) {
        map.addOverlayMapTypeId(mapTypes.traffic);    
    }
    
    // 자전거도로정보 체크박스가 체크되어있으면 지도에 자전거도로정보 지도타입을 추가합니다
    if (chkBicycle.checked) {
        map.addOverlayMapTypeId(mapTypes.bicycle);    
    }
    
} 

function getAddressCoordinates(address) {
	return new Promise((resolve, reject) => {
	  geocoder.addressSearch(address, function(result, status) {
		if (status === kakao.maps.services.Status.OK) {
		  var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
		  resolve(coords);
		} else {
		  reject(new Error("주소 검색에 실패했습니다."));
		}
	  });
	});
  }
  
  async function searchAddress() {
	try {
	  console.log(`3`);
	  const address = '서울 종로구 사직로 161';
	  const coords = await getAddressCoordinates(address);
  
	  // 결과값으로 받은 위치를 마커로 표시합니다
	  var marker = new kakao.maps.Marker({
		map: map,
		position: coords
	  });
  
	  // 인포윈도우로 장소에 대한 설명을 표시합니다
	  var infowindow = new kakao.maps.InfoWindow({
		content: '<div style="width:150px;text-align:center;padding:6px 0;">현재위치</div>'
	  });
	  infowindow.open(map, marker);
  
	  // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
	  map.setCenter(coords);
	} catch (error) {
	  console.error(error);
	}
  }
  
  searchAddress();
  

var clusterer = new kakao.maps.MarkerClusterer({
	map: map, // 마커들을 클러스터로 관리하고 표시할 지도 객체 
	averageCenter: true, // 클러스터에 포함된 마커들의 평균 위치를 클러스터 마커 위치로 설정 
	minLevel: 6 // 클러스터 할 최소 지도 레벨 
});
console.log(`4`);


$.get("./json_data.json", function(data) {
    var stationLatitude = data.stationLatitude;
    var stationLongitude = data.stationLongitude;
	var imageSrc = './image/bicycle_station.png', // 마커이미지의 주소입니다    
    imageSize = new kakao.maps.Size(64, 69), // 마커이미지의 크기입니다
    imageOption = {offset: new kakao.maps.Point(27, 69)}; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.

	var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption)
    // 데이터에서 좌표 값을 가지고 마커를 표시합니다
    // 마커 클러스터러로 관리할 마커 객체는 생성할 때 지도 객체를 설정하지 않습니다
    var markers = $.map(stationLatitude, function(latitude, index) {
        var longitude = stationLongitude[index];
        var position = new kakao.maps.LatLng(latitude, longitude);
        return new kakao.maps.Marker({ position: position, image: markerImage });
    });

    // 클러스터러에 마커들을 추가합니다
    clusterer.addMarkers(markers);
});


