const closeBtn = document.getElementById('close');
const manual = document.getElementById('manual');
const base = document.getElementById('base');
const modal = document.getElementById('modal');

manual.addEventListener('click', () =>{
    base.classList.add('switch_display');
    modal.classList.remove('switch_display');
});

closeBtn.addEventListener('click', ()=>{
    base.classList.remove('switch_display');
    modal.classList.add('switch_display');
});

var newURL = window.location.protocol + "//" + window.location.host + "/" + window.location.pathname + window.location.search

console.log(newURL)
