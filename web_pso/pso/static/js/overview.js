const link_advance = document.querySelector('.link_advance');
const advance = document.getElementById('advance');
const advanceMenu = document.querySelector('.advance_menu');
const closeBtn = document.getElementById('close');
const submitBtn = document.getElementById('submitBtn');



advance.addEventListener('click', () =>{
    link_advance.classList.add('switch_display');
    advanceMenu.classList.remove('switch_display');
    submitBtn.style.bottom = '-1rem';
});

closeBtn.addEventListener('click', () =>{
    link_advance.classList.remove('switch_display');
    advanceMenu.classList.add('switch_display');
    submitBtn.style.bottom = '-4rem';
});