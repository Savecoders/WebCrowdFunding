
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);
const regexSign = /[-$%^&*()+|~=`{}\[\]:";'<>?,\/]/;


// const btn = document.querySelector('.btn1');
const btn = $('.btn1');

btn.addEventListener('click', checkStuff);



const checkStuff  = () => {

    const name = $('#name').value.trim();

    if(name === '') {
        alert('Please enter your name');
        return;
    }

    const email = $('#email').value.trim();

    if(email === '') {
        alert('Please enter your email');
        return;
    } if(email.includes(regexSign)) {
        alert('Please enter a valid email');
        return;
    }

}