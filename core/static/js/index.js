const input_password = document.querySelector('#id_password')
      const fa_eye = document.querySelector(".fa-eye")

      fa_eye.addEventListener("click", () => {
        const type = input_password.type === 'password' ? 'text' : 'password'
        input_password.type = type

        if(type === 'password') {
          fa_eye.classList.remove("fa-eye-slash")
          fa_eye.classList.add("fa-eye")
        }else {
          fa_eye.classList.remove('fa-eye');
          fa_eye.classList.add('fa-eye-slash');
    }
      })