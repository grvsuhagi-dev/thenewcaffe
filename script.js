window.addEventListener("scroll",()=>{

const cards=document.querySelectorAll(".info-card")

cards.forEach(card=>{

let top=card.getBoundingClientRect().top

if(top<window.innerHeight-50){

card.style.opacity="1"

card.style.transform="translateY(0)"

}

})

})