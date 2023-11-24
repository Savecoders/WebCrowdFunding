
const $ = document.querySelector.bind(document);

const checkSubmitFile = () => {
    // label upload image 
    const label = $('.file-upload-label');
    // input image
    const inputFile = $('#profile_image');

    // check if file/image is selected
    if (inputFile && inputFile.files.length) {
        label.innerHTML = "Foto de Perfil seleccionada";
        label.classList.add('file-upload-selected');
    } else {
        label.innerHTML = "Seleccionar Foto de Perfil";
        label.classList.remove('file-upload-selected'); 
    }
}