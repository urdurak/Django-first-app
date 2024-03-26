const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');

function openpanel() {
    container.classList.add("right-panel-active")
};

function closepanel() {
    container.classList.remove("right-panel-active")
};

signInButton.addEventListener("click", openpanel);
signInButton.addEventListener("click", closepanel);
