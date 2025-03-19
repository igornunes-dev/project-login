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
const input_username = document.querySelector('#id_username');
const input_email = document.querySelector('#id_email');
const inputNewPassword1 = document.querySelector("#id_new_password1");
const inputNewPassword2 = document.querySelector("#id_new_password2");
const message_caracter = document.querySelector('.password_caracter');
const message_special = document.querySelector('.password_special');
const button_register = document.querySelector('.button_register');

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

function checkPasswordLength(str) {
  return str.length < 8;
}


if(inputPassword){
  inputPassword.addEventListener("input", checkPasswordLength);
}


function containsSpecialCharacter(str) {
  const specialChars = "!@#$%^&*(),.?\":{}|<>~`\\-_+=\\[\\];'/";
  
  for (let i = 0; i < str.length; i++) {
    if (specialChars.indexOf(str[i]) !== -1) {
      return true;
    }
  }
  
  return false;
}

inputPassword.addEventListener('input', () => {
  if (!containsSpecialCharacter(inputPassword.value)) {
    message_special.classList.add('active');
    button_register.classList.add('disabled');
    button_register.setAttribute('disabled', ''); 
  } 
  else {
    message_special.classList.remove('active');
  }
  if(checkPasswordLength(inputPassword.value)) {
    message_caracter.classList.add('active');
  } else {
    message_caracter.classList.remove('active');
  }

  if(!checkPasswordLength(inputPassword) && containsSpecialCharacter(inputPassword.value)) {
      button_register.removeAttribute('disabled');
      button_register.classList.remove('disabled');
  }
});

// if(input_username.value.trim() === '' || input_email.value.trim() === '' || inputPassword.value.trim() === '') {
//   button_register.setAttribute('disabled', '');
//   button_register.classList.add('disabled');
// } else {
//   button_register.removeAttribute('disabled', '');
//   button_register.classList.remove  ('disabled');
// }


