API_KEY = '904f2fe1a5a35a647ceda442a230b413'; // 발급 받은 API KEY 삽입 

const iconClasses = {
   '01d': 'fas fa-sun',       // 맑은 날씨 (주간)
   '01n': 'fas fa-moon',      // 맑은 날씨 (야간)
   '02d': 'fas fa-cloud-sun', // 구름 조금 (주간)
   '02n': 'fas fa-cloud-moon',// 구름 조금 (야간)
   '03d': 'fas fa-cloud',     // 구름 낌 (주간)
   '03n': 'fas fa-cloud',     // 구름 낌 (야간)
   '04d': 'fas fa-cloud',     // 구름 많음 (주간)
   '04n': 'fas fa-cloud',     // 구름 많음 (야간)
   '09d': 'fas fa-cloud-rain',// 비 (주간)
   '09n': 'fas fa-cloud-rain',// 비 (야간)
   '10d': 'fas fa-cloud-sun-rain', // 비 (주간)
   '10n': 'fas fa-cloud-moon-rain',// 비 (야간)
   '11d': 'fas fa-bolt',      // 번개 (주간)
   '11n': 'fas fa-bolt',      // 번개 (야간)
   '13d': 'fas fa-snowflake', // 눈 (주간)
   '13n': 'fas fa-snowflake', // 눈 (야간)
   '50d': 'fas fa-smog',      // 안개 (주간)
   '50n': 'fas fa-smog'       // 안개 (야간)
};
  

function onGeoOk(position){
   const lat=position.coords.latitude;
   const lon=position.coords.longitude;
   const url=`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=kr`;
   fetch(url)
       .then(res=>res
       .json().then(data=>{
           const weather=document.querySelector("#weather span:first-child");
           const city=document.querySelector("#weather span:nth-child(3)");

           const iconClass = iconClasses[data.weather[0].icon];
           const weatherIcon = document.getElementById('weather-icon');
           weather.className = iconClass;

           weather.innerText=`${data.weather[0].main} ${data. main.temp}°`;
           city.innerText="@"+data.name;


   }))
}
function onGeoError(){
   alert("Can't find you. No Weather for you.");
}




navigator.geolocation.getCurrentPosition(onGeoOk,onGeoError);
