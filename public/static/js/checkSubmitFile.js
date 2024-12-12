// selectors
const $QS = document.querySelector.bind(document);
const inputFile = $QS(".file-upload-input");

const checkSubmitFile = () => {
  // label upload image
  const label = $QS(".file-upload-label");

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

const plusIcon = $QS(".image-plus__icon");
plusIcon.addEventListener("click", () => {
  inputFile.click();
});
