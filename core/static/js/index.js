// Função para alternar o tipo do campo de senha
function togglePasswordVisibility(inputField, eyeIcon) {
  if (inputField && eyeIcon) {
    const type = inputField.type === 'password' ? 'text' : 'password';
    inputField.type = type;

    if (type === 'password') {
      eyeIcon.classList.remove("fa-eye-slash");
      eyeIcon.classList.add("fa-eye");
    } else {
      eyeIcon.classList.remove('fa-eye');
      eyeIcon.classList.add('fa-eye-slash');
    }
  }
}

const inputPassword = document.querySelector('#id_password');
const inputNewPassword1 = document.querySelector("#id_new_password1");
const inputNewPassword2 = document.querySelector("#id_new_password2");

const eyeIcon1 = document.querySelector(".fa-eye");
const eyeIcon2 = document.querySelector(".fa-eye.input-2"); 
const eyeIcon3 = document.querySelector(".fa-eye.input-3"); 

if (eyeIcon1 && inputPassword) {
  eyeIcon1.addEventListener("click", () => {
    togglePasswordVisibility(inputPassword, eyeIcon1);
  });
}

if (eyeIcon2 && inputNewPassword1) {
  eyeIcon2.addEventListener("click", () => {
    togglePasswordVisibility(inputNewPassword1, eyeIcon2);
  });
}

if (eyeIcon3 && inputNewPassword2) {
  eyeIcon3.addEventListener("click", () => {
    togglePasswordVisibility(inputNewPassword2, eyeIcon3);
  });
}


window.onload = () => {
  setTimeout(() => {
    document.querySelector("main").style.opacity = "1"; 
  }, 500); 
};





