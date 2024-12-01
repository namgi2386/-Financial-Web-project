<template>
    <div class="map-container">
        <div id="map"></div>
    </div>
</template>
    
    <script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios'
    
    let geocoder = null;

    const lat = 35.20536
    const lon = 126.81056
    

    
    
    let map = null;
    let markers = [];
    
    const initMap = (lat = 35.20536, lon = 126.81056) => {
        const container = document.getElementById('map');
        const options = {
            center: new kakao.maps.LatLng(lat, lon),
            level: 5,
        };
    
        // 지도 객체를 등록합니다.
        // 지도 객체는 반응형 관리 대상이 아니므로 initMap에서 선언합니다.
        map = new kakao.maps.Map(container, options);
    };
    
    // Map.vue가 마운트 될 때, initMap() 함수 실행되도록
    onMounted(async () => {
        if (window.kakao && window.kakao.maps) {
            // Kakao Maps API가 이미 로드된 경우
            kakao.maps.load(() => {
                initMap();
                geocoder = new kakao.maps.services.Geocoder(); // geocoder 객체 생성
            });
        } else {
            // Kakao Maps API 스크립트 동적 로드
            const script = document.createElement('script');
            script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${import.meta.env.VITE_APP_mapKey}&libraries=services`;
            document.head.appendChild(script);
            script.onload = () => {
                kakao.maps.load(() => {
                    initMap();
                    geocoder = new kakao.maps.services.Geocoder(); // geocoder 객체 생성
                });
            };
        }
    });
    
    // var markers = []
    
    const markBank = async function (address ,bankName) {
        console.log(bankName, '을 찾으려고 하는 중')
        
        // const address = await getAddressFromCoords(lat, lon);
        console.log(address , '응여기');
        
        // map의 확대, 축소 레벨을 8로 고정
        map.setLevel(5)
    
        // 현재 지도에 표시된 마커가 있으면, 모두 제거함
        if (markers.length > 0) {
            markers.forEach((item) => {
                item.setMap(null)
            })
        }
    
        // 마커를 클릭하면 장소명을 표출할 인포윈도우 입니다
        var infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    
        // 장소 검색 객체를 생성합니다
        var ps = new kakao.maps.services.Places();

        // 위도, 경도를 기준으로 주변 ATM을 검색합니다
        const searchKeyword = `${lat}, ${lon} atm`;
    
        // 키워드로 장소를 검색합니다
        ps.keywordSearch(`${address} ${bankName}`, placesSearchCB);
    
        // 키워드 검색 완료 시 호출되는 콜백함수 입니다
        function placesSearchCB(data, status, pagination) {
            if (status === kakao.maps.services.Status.OK) {
    
                for (var i = 0; i < data.length; i++) {
                    displayMarker(data[i]);
                }
    
            }
            // console.log(markers)
        }

        // 지도에 마커를 표시하는 함수입니다
        function displayMarker(place) {
    
            // 마커를 생성하고 지도에 표시합니다
            var marker = new kakao.maps.Marker({
                map,
                position: new kakao.maps.LatLng(place.y, place.x)
            });
            markers.push(marker)
    
            // 마커에 클릭이벤트를 등록합니다
            kakao.maps.event.addListener(marker, 'mouseover', function () {
                // 마커에 마우스를 올리면 장소명 인포윈도우에 표출됩니다
                infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
                infowindow.open(map, marker);
            });
            kakao.maps.event.addListener(marker, 'mouseout', function () {
                // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
                infowindow.close(map, marker);
            });
            // 클릭하면 정보가 뜨도록 (추가해야함)
            kakao.maps.event.addListener(marker, 'click', function () {
                // 마커를 클릭하면 장소명이 해당 장소 확대
                const pos = marker.getPosition()
                map.setLevel(3)
                map.panTo(pos)
            });
    
        }
    
    }

//##########################################여기부터 atm ##################################################
// Geocoder 객체 생성


// 좌표를 주소로 변환하는 함수
const getAddressFromCoords = (lat, lon) => {
    return new Promise((resolve, reject) => {
        const coords = new kakao.maps.LatLng(lat, lon);
        geocoder.coord2Address(coords.getLng(), coords.getLat(), (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
            // 결과에서 법정동 주소 추출
            const address = result[0].address.address_name;
            resolve(address);
        } else {
            reject("주소를 가져올 수 없습니다.");
        }
        });
    });
    };

    // markATM 함수 수정
    const markATM = async (lat , lon) => {
    try {
        // 위경도를 기반으로 주소 가져오기
        const address = await getAddressFromCoords(lat, lon);
        console.log(`${address}의 주변 ATM을 찾습니다.`);
        
        // map의 확대, 축소 레벨을 5로 고정
        map.setLevel(6);

        // 기존 마커 제거
        if (markers.length > 0) {
        markers.forEach((item) => {
            item.setMap(null);
        });
        }

        // 마커를 클릭하면 장소명을 표출할 인포윈도우입니다
        const infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });

        // 장소 검색 객체 생성
        const ps = new kakao.maps.services.Places();

        // 키워드로 장소를 검색
        const extractTextBeforeNumber = (address) => {
            const match = address.match(/^[^\d]+/); // 숫자가 나오기 전까지의 문자열 매칭
            return match ? match[0].trim() : ""; // 매칭된 결과가 있으면 반환, 없으면 빈 문자열 반환
        };
        const refinedAddress = extractTextBeforeNumber(address);
        console.log(refinedAddress);
        
        ps.keywordSearch(`${refinedAddress} atm`, placesSearchCB);

        // 키워드 검색 완료 시 호출되는 콜백 함수
        function placesSearchCB(data, status) {
        if (status === kakao.maps.services.Status.OK) {
            for (let i = 0; i < data.length; i++) {
            displayMarker(data[i]);
            }
        }
        }

        // 지도에 마커를 표시하는 함수
        function displayMarker(place) {
        // 마커 생성 및 지도에 표시
        const marker = new kakao.maps.Marker({
            map,
            position: new kakao.maps.LatLng(place.y, place.x),
        });
        markers.push(marker);

        // 마커에 클릭 이벤트 등록
        kakao.maps.event.addListener(marker, "mouseover", function () {
            infowindow.setContent(`<div style="padding:5px;font-size:12px;">${place.place_name}</div>`);
            infowindow.open(map, marker);
        });
        kakao.maps.event.addListener(marker, "mouseout", function () {
            infowindow.close();
        });
        kakao.maps.event.addListener(marker, "click", function () {
            map.setLevel(3);
            map.panTo(marker.getPosition());
        });
        }
    } catch (error) {
        console.error(error);
    }
}
//############################################################################################



    // 현위치 버튼을 누르면, 지도 중심이 현위치로 이동하도록
    const setCenter = function (lat, lon) {
        const moveLatLon = new kakao.maps.LatLng(lat, lon);
        map.setLevel(6)
        // console.log('Map에서', moveLatLon)
        // console.log('Map에서', map)
        // 지도 중심을 이동 시킵니다
        map.setCenter(moveLatLon)
    
    }
    
    // address 넘겨주면, 위경도 검색하고 지도의 중심을 옮기는 함수
    const moveSelectedLocation = function (address) {
        // console.log(restAPIKey)
        axios({
            method: 'get',
            url: "https://dapi.kakao.com/v2/local/search/address.json",
            params: {
                'analyze_type': 'similar',
                'page': 1,
                'size': 3,
                'query': address
            },
            headers: { 'Authorization': `KakaoAK ${import.meta.env.VITE_APP_restAPIKey}` }
        })
            .then((res) => {
                console.log(res.data.documents[0].address)
                const lat = res.data.documents[0].address.y
                const lon = res.data.documents[0].address.x
                setCenter(lat, lon)
    
            })
            .catch((err) => {
                console.log(err)
            })
    
    }
    // ################################################################
    // kakao.maps.event.addListener(map, 'idle', function() {
    //     searchAddrFromCoords(map.getCenter(), displayCenterInfo);
    // });

    // function displayCenterInfo(result, status) {
    //     if (status === kakao.maps.services.Status.OK) {

    //         for(var i = 0; i < result.length; i++) {
    //             // 행정동의 region_type 값은 'H' 이므로
    //             if (result[i].region_type === 'H') {
    //                 return result[i].address_name
    //             }
    //         }
    //     }    
    // }
    // ################################################################

    defineExpose({
        setCenter, moveSelectedLocation, markBank , markATM
    })
    </script>
    
    
<style scoped>
/* 부모 컨테이너에 Flexbox 적용 */
.map-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh; /* 화면 전체 높이 사용 */
  margin-bottom: 40px;     /* 불필요한 여백 제거 */
}

/* 지도 스타일 */
#map {
  width: 60rem;
  height: 30rem;
  border-radius: 10px;
}
</style>
