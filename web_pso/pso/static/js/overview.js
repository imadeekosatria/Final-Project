const link_advance = document.querySelector('.link_advance');
const advance = document.getElementById('advance');
const advanceMenu = document.querySelector('.advance_menu');
const closeBtn = document.getElementById('close');
const submitBtn = document.getElementById('submitBtn');
const researchBtn = document.getElementById('mode_research');
const researchMenu = document.querySelector('.research_menu');
const linkTesting = document.querySelector('.testing');
const close_research = document.getElementById('close_research');






advance.addEventListener('click', () =>{
    link_advance.classList.add('switch_display');
    advanceMenu.classList.remove('switch_display');
    linkTesting.classList.add('switch_display');
    submitBtn.style.bottom = '-1rem';
});

closeBtn.addEventListener('click', () =>{
    link_advance.classList.remove('switch_display');
    advanceMenu.classList.add('switch_display');
    linkTesting.classList.remove('switch_display');
    submitBtn.style.bottom = '-4rem';
});

researchBtn.addEventListener('click', ()=>{
    link_advance.classList.add('switch_display');
    linkTesting.classList.add('switch_display');
    researchMenu.classList.remove('switch_display');
    submitBtn.style.bottom = '-1rem';
});

close_research.addEventListener('click', ()=>{
    linkTesting.classList.remove('switch_display');
    link_advance.classList.remove('switch_display');
    researchMenu.classList.add('switch_display');
    submitBtn.style.bottom = '-1rem';
});