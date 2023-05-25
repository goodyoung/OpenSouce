var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(my_location[1],my_location[2]), // 지도의 중심좌표
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
	  const address = my_location[0];
	  const coords = await getAddressCoordinates(address);
    console.log(`100`,address,coords);
    
	  // 결과값으로 받은 위치를 마커로 표시합니다
	  var marker = new kakao.maps.Marker({
		map: map,
		position: coords
	  });
  
	  // 인포윈도우로 장소에 대한 설명을 표시합니다
	  var infowindow = new kakao.maps.InfoWindow({
		content: '<div style="width:150px;text-align:center;padding:6px 0;">내 위치</div>'
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
	minLevel: 4 // 클러스터 할 최소 지도 레벨 
});
console.log(`4`);

// 모달 열기 버튼
var modalButton = document.getElementById("modal-button");

// 모달 엘리먼트
var modal = document.getElementById("modal");

// 닫기 버튼
var closeBtn = document.getElementsByClassName("close")[0];

// 모달 열기 버튼 클릭
modalButton.onclick = function() {
  modal.style.display = "block";
}

// 닫기 버튼 클릭
closeBtn.onclick = function() {
  modal.style.display = "none";
}

// 모달 외부 클릭
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var circle = new kakao.maps.Circle({
  center : new kakao.maps.LatLng(my_location[1], my_location[2]),  // 원의 중심좌표 입니다 
  radius: result_around[0][4].distance, // 미터 단위의 원의 반지름입니다 
  strokeWeight: 5, // 선의 두께입니다 
  strokeColor: '#75B8FA', // 선의 색깔입니다
  strokeOpacity: 1, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
  strokeStyle: 'dashed', // 선의 스타일 입니다
  fillColor: '#CFE7FF', // 채우기 색깔입니다
  fillOpacity: 0.7  // 채우기 불투명도 입니다   
}); 

// 지도에 원을 표시합니다 
circle.setMap(map); 




