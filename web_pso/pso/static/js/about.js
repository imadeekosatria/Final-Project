const f1 = document.getElementById('1');
const f2 = document.getElementById('2');
const f3 = document.getElementById('3');
const f4 = document.getElementById('4');
const f5 = document.getElementById('5');
const content = document.querySelector('.context');
const feature = document.getElementById('feature');

content.addEventListener('animationend', ()=>{
    content.classList.remove('animate__fadeInUp');
});

f1.addEventListener('click', ()=>{
    feature.innerHTML ='Checking each sentence similarity with <b>Title</b>. Calculate how many times <b>word in Title</b> shown in <b>each sentence</b>.';
    content.classList.add('animate__fadeInUp');
    if (f1.classList.contains('clicked_feature') == false) {
        const clicked_feature = document.querySelector('.clicked_feature');
        f1.classList.add('clicked_feature');
        clicked_feature.classList.remove('clicked_feature');
    }
});


f2.addEventListener('click', ()=>{
    feature.innerHTML = '<b>Short sentences</b> generally do not contain information related to the main topic. So this feature is used to filter sentence that\'s not related';
    content.classList.add('animate__fadeInUp');
    if (f2.classList.contains('clicked_feature') == false) {
        const clicked_feature = document.querySelector('.clicked_feature');
        f2.classList.add('clicked_feature');
        clicked_feature.classList.remove('clicked_feature');
    }
});

f3.addEventListener('click', ()=>{
    feature.innerHTML = '<b>Sentence position</b> usually affects where important information is located. Generally the first sentence contains the most important information.';
    content.classList.add('animate__fadeInUp');
    if (f3.classList.contains('clicked_feature') == false) {
        const clicked_feature = document.querySelector('.clicked_feature');
        f3.classList.add('clicked_feature');
        clicked_feature.classList.remove('clicked_feature');
    }
});

f4.addEventListener('click', ()=>{
    feature.innerHTML = '<b>TF-IDF</b> is a method for calculating the weight of each word that is most commonly used in information retrieval.';
    content.classList.add('animate__fadeInUp');
    if (f4.classList.contains('clicked_feature') == false) {
        const clicked_feature = document.querySelector('.clicked_feature');
        f4.classList.add('clicked_feature');
        clicked_feature.classList.remove('clicked_feature');
    }
});


f5.addEventListener('click', ()=>{
    feature.innerHTML = 'The <b>Cosine Similarity</b> method is a method used to calculate the similarity (level of similarity) between two sentences.';
    content.classList.add('animate__fadeInUp');
    if (f5.classList.contains('clicked_feature') == false) {
        const clicked_feature = document.querySelector('.clicked_feature');
        f5.classList.add('clicked_feature');
        clicked_feature.classList.remove('clicked_feature');
    }
});

const sr = ScrollReveal({
    origin: 'top',
    distance: '80px',
    duration: 2000,
    reset: true
});
sr.reveal('#image_about', {});
sr.reveal('#first', {delay:400});
sr.reveal('#second', {delay:400});
sr.reveal('#third', {delay:400});
sr.reveal('#title_about', {delay: 600});
sr.reveal('#about_desc', {delay: 600});
sr.reveal('#easy_use', {delay:400})
sr.reveal('.easy_list', {delay:800});
sr.reveal('.feature > img', {delay:400});
sr.reveal('.feature_btn', {delay:400});