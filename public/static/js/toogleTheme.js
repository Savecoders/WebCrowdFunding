const theme = localStorage.getItem('theme');
const toggle = document.querySelector('.theme-toogle');

if (theme === 'dark') {
    document.body.classList.add('dark');
    document.body.classList.remove('light');
} else {
    document.body.classList.add('light');
    document.body.classList.remove('dark');
}

toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    document.body.classList.toggle('light');

    let theme = 'light';
    if (document.body.classList.contains('dark')) {
        theme = 'dark';
    }
    localStorage.setItem('theme', theme);
});