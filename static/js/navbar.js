// constains the code for the menu
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);
const hamburguerIcon = $('.nav__hamburguer');
const navOverlay = $('.nav__overlay');
const listCanOpen = $$('.can__open');


let currentDropdown = navOverlay;
// hamburguer listner
hamburguerIcon.addEventListener('click', ()=>{
    hamburguerIcon.classList.toggle('nav__hamburguer--open');

    navOverlay.classList.toggle('nav__overlay--show');
});

// overlay listner
listCanOpen.forEach((list) => {
    list.addEventListener('click', (e)=>{
        e.preventDefault();
        const currentElement = e.target;
        // console.log(e.target.classList.value);

        if( isActive(currentElement, 'nav__parent') ){

            const subMenu = currentElement.parentElement.children[1];

            if(window.innerWidth < 1200){

                let height = (subMenu.clientHeight == 0) 
                            ? subMenu.scrollHeight : 0;
                // console.log(subMenu.clientHeight);

                subMenu.style.height = `${height}px`;
            }else{

                if( !isActive(subMenu, 'nav__inner--show') ){
                    closeDropdown(currentDropdown);
                }
                subMenu.classList.toggle('nav__inner--show');

                currentDropdown = subMenu;

            }

        }
    });
});


function isActive(element, string){
    return element.classList.value.includes(string);
}

function closeDropdown(currentDropdown){
    if( isActive(currentDropdown, 'nav__inner--show')){
        currentDropdown.classList.remove('nav__inner--show');
    }
}

window.addEventListener('resize', ()=>{
    closeDropdown(currentDropdown);

    if(window.innerWidth > 1200){
        const navInners = document.querySelectorAll('.nav__inner');

        navInners.forEach(navInner =>{
            navInner.style.height = '';
        });
    }
});