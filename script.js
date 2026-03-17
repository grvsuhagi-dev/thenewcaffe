// simple scroll animation

window.addEventListener("scroll", function(){

let elements = document.querySelectorAll(".menu-card");

elements.forEach(function(el){

let position = el.getBoundingClientRect().top;

let screen = window.innerHeight;

if(position < screen){

el.style.opacity = "1";
el.style.transform = "translateY(0px)";

}

})

})