
// profile page switch conext - html에서 control
profileInfor = (e) => {
  e.preventDefault();
  $profileInfor = document.querySelector('.infor');
  location.reload();
  $profileInfor.innerHTML = `{% include 'profile-infor.html' %}`
  document.querySelector('.profile-btn').classList.add('clicked');
  document.querySelector('.write-btn').classList.remove('clicked');
  document.querySelector('.like-btn').classList.remove('clicked');
}
writeInfor = (e) => {
  e.preventDefault();
  $profileInfor = document.querySelector('.infor');
  $profileInfor.innerHTML = `{% include 'write-infor.html' %}`
  document.querySelector('.profile-btn').classList.remove('clicked');
  document.querySelector('.write-btn').classList.add('clicked');
  document.querySelector('.like-btn').classList.remove('clicked');
  
}
likeInfor = (e) => {
  e.preventDefault();
  $profileInfor = document.querySelector('.infor');
  $profileInfor.innerHTML = `{% include 'like-infor.html' %}`
  document.querySelector('.profile-btn').classList.remove('clicked');
  document.querySelector('.write-btn').classList.remove('clicked');
  document.querySelector('.like-btn').classList.add('clicked');
  
}

// profile user 이미지 업로드 기능
const $uploadImgInput = document.querySelector('.profile-upload-img-input');
const $uploadPreviewImg = document.querySelector('.profile-upload-preview-img');

$uploadImgInput.onchange = (e) => {
// document.querySelector('.upload-img-div').innerHTML='';
let image = event.target.files[0]
  let reader = new FileReader();
  reader.onload = function (event) {
    $uploadPreviewImg.setAttribute('src', event.target.result);
  }

  reader.readAsDataURL(image);
}



function UploadImg(event){
$uploadImgInput.click();
}


// 찜한 제품 프로필 - html에서 control
function likeBtn(article_pk) {

let likeCsrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;
let param = {
  'article_pk': article_pk,
}
fetch("{% url 'social:like' %}", {
  method: 'POST',
  headers: {
    "X-CSRFToken": likeCsrfValue,
    "X-Requested-With": "XMLHttpRequest"
  },
  body: JSON.stringify(param),
}).then(function (response) {
  console.log('readdss',response)
  return response.json()
}).then(function (data) {
  let likedIcon = document.querySelector(`.detail-like${data.article_pk}`);
  if (data.is_liked){
      likedIcon.classList.add('liked');
  }
  else{
    likedIcon.classList.remove('liked');
  }

}).catch((error) => {
  console.log('error', error);
})
}