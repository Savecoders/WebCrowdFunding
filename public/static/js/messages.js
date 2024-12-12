const messages = document.querySelectorAll(".message");

messages.forEach((message) => {
  message.addEventListener("click", () => {
    message.classList.add("fade-out");
    setTimeout(function () {
      message.remove();
    }, 300);
  });
});
