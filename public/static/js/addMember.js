// class formulate
const form = document.getElementById("formulate__user");

document.getElementById("addButton").addEventListener("click", function () {
  // the input and button exists?

  if (document.querySelector(".send__email")) {
    document.querySelector(".send__email").focus();
    return;
  }

  let input = document.createElement("input");
  let button = document.createElement("button");

  input.type = "email";

  // styles
  input.classList.add("send__email");
  input.placeholder = "Email";
  input.name = "email";
  input.autocomplete = "off";
  input.required = true;

  button.classList.add("btn");

  input.type = "email";
  button.textContent = "Agregar";

  // add input and button
  form.appendChild(input);
  form.appendChild(button);

  document.getElementById("formContainer").appendChild(form);
});
