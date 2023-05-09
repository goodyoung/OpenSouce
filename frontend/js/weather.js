const API_KEY="";

function onGeoOk(position){
   const lat=position.coords.latitude;
   const lon=position.coords.longitude;
   const url=`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=kr`;
   fetch(url)
       .then(res=>res
       .json().then(data=>{
           const weather=document.querySelector("#weather span:first-child");
           const city=document.querySelector("#weather span:last-child");
           const weatherIconImg = document.querySelector('.weatherIcon');
           const weatherIcon = data.weather[0].icon;
           const weatherIconAdrs = `http://openweathermap.org/img/wn/${weatherIcon}@2x.png`;
    
           weather.innerText=`${data.weather[0].main} ${data. main.temp}°`;
           city.innerText="@"+data.name;
           console.log(weatherIconAdrs);
           weatherIconImg.setAttribute('src', weatherIconAdrs);
   }))
}
function onGeoError(){
   alert("Can't find you. No Weather for you.");
}




navigator.geolocation.getCurrentPosition(onGeoOk,onGeoError);
