// signup ajax function
let registerBtn = document.querySelector('.register-submit');
let signupForm = document.querySelector('.register-form');

signupForm.addEventListener('submit', submitInfor);

function submitInfor(e) {
e.preventDefault();
let userId = document.querySelector('.userid').value;
let userPwd = document.querySelector('.pwd').value;
let userPwdChk = document.querySelector('.pwd-chk').value;
let userEmail = document.querySelector('.email').value;

let param = {
  'user_id': userId,
  'password': userPwd,
  'password_chk':userPwdChk,
}
let csrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;

fetch("{% url 'user:signup' %}", {
  method: 'POST',
  headers: {
    "X-CSRFToken": csrfValue,
    "X-Requested-With": "XMLHttpRequest"
  },
  body: JSON.stringify(param),
}).then(function (response) {
  console.log('reass',response)
  return response.json()
}).then(function (data) {
  console.log('data',data)
  signupForm.reset()
  // console.log(data)
}).catch((error) => {
  console.log('error', error);
})

} // btn click function
