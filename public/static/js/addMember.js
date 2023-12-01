document.getElementById("addButton").addEventListener("click", function () {
  let form = document.createElement("form");
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

  // add attributes
  form.action = "/addMember";
  form.method = "POST";

  // add input and button
  form.appendChild(input);
  form.appendChild(button);

  document.getElementById("formContainer").appendChild(form);
});
