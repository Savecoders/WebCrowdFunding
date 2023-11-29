const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

const messages = $$(".message");

messages.forEach((message) => {
  message.addEventListener("click", () => {
    message.classList.add("fade-out");
    setTimeout(function () {
      message.remove();
    }, 300);
  });
});
