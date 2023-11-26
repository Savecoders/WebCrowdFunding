// selectors
const $ = document.querySelector.bind(document);
const inputFile = $(".file-upload-input");

const checkSubmitFile = () => {
  // label upload image
  const label = $(".file-upload-label");

  // check if file/image is selected
  if (inputFile && inputFile.files.length) {
    label.innerHTML = "Foto de Perfil seleccionada";
    console.log(inputFile.files.length);
    label.classList.add("file-upload-selected");
  } else {
    label.innerHTML = "Seleccionar Foto de Perfil";
    label.classList.remove("file-upload-selected");
  }
};

const plusIcon = $(".image-plus__icon");
plusIcon.addEventListener("click", () => {
  inputFile.click();
});
