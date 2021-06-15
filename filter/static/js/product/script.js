// article main page select form submit
document.querySelector('.select-filter-form').onchange = (e) => {
  $selectForm = document.querySelector('.select-filter-form');
  $selectForm.submit();
  }


// detail js에서는 동작 x 왜??
  function commentReply(comment_pk) {
    document.querySelector(`.recomment-form${comment_pk}`).classList.remove('non-display');
  }
// article detail page like ajax function
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
      console.log('readdss', response)
      return response.json()
    }).then(function (data) {
      let likedIcon = document.querySelector(`.detail-like${data.article_pk}`);
      if (data.is_liked) {
        likedIcon.classList.add('liked');
      }
      else {
        likedIcon.classList.remove('liked');
      }

    }).catch((error) => {
      console.log('error', error);
    })
  }

  // detail page comment ajax function
  let $commentForm = document.querySelector('.comment-form');

  $commentForm.addEventListener('submit', submitComment);

  function submitComment(e) {
    e.preventDefault();
    let content = document.querySelector('.input-comment').value;
    if (content == '') {
      return
    }
    let param = {
      'article_pk': '{{article.pk}}',
      'content': content,
      'user_pk': '{{request.user.pk}}',
      'owner_pk': '{{article.writer.pk}}'
    }
    let csrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    fetch("{% url 'social:comment' %}", {
      method: 'POST',
      headers: {
        "X-CSRFToken": csrfValue,
        "X-Requested-With": "XMLHttpRequest"
      },
      body: JSON.stringify(param),
    }).then(function (response) {
      console.log('reass', response)
      return response.json()
    }).then(function (data) {
      let data_id = data.comment_obj.id
      console.log(data.profile_nickname)
      $commentForm.reset()


      if ('{{article.writer.pk}}' == data.writer_pk || '{{article.writer.pk}}' == '{{request.user.pk}}') {
        document.querySelector('.comment-ul').innerHTML += `
      <li class="comment-li comment-li${data_id}">
        <span class="comment-profile-span"><img class="user-img user_img${data_id} comment-profile-img"
          src="{{article.writer.profile.image.url}}" alt="" onerror="this.src='{% static 'img/감자.png' %}'"><strong
          class="owner">판매자</strong><span>${data.comment_obj.created_at}</span></span>
          <span class="comment-content comment-content${data_id}">${data.comment_obj.content}</span>
          <form class="delete-comment-form delete-comment-form${data_id}" action="" method="POST">
        <input type="submit" class="comment-delete comment-delete${data_id}" onclick="commentDelete('${data_id}')"value="삭제">
        <button type="submit" class="comment-content-edit comment-content-edit${data_id}"
            onclick="commentContentEditBtn('${data_id}')">수정</button>
        </form>
      <form action="" method="POST" class="edit-comment-form edit-comment-form${data_id} non-display">
          {% csrf_token %}
          <input type="text" class="edit_comment${data_id}" name="edit_text" value="${data.comment_obj.content}">
          <input type="submit" class="edit-comment-btn" value="수정하기" onclick="commentEditBtn('${data_id}')"></input>
          <button type="submit" class="comment-edit-cancel comment-edit-cancel${data_id}"
            onclick="commentEditCancelBtn('${data_id}')">취소하기</button>
        </form>
          <form action="" method="POST"
          class="recomment-form${data_id} non-display" onsubmit="recommentForm('${data_id}')>
          {% csrf_token %}
          <textarea type="text" class="input-re-comment input-re-comment${data_id}" name="re_comment"
          placeholder="댓글입력"></textarea>
          <div class="input-re-comment-input">
            <input class="re-comment-btn re-comment-btn${data_id}" type="submit" value="입력하기"
            ">
            <input class="re-comment-btn re-comment-cancel-btn${data_id}" type="submit" value="취소하기"
            onclick="reCommentCancelBtn('${data_id}')">
            </div>
            </form>
            </li>
            `
      }
      else if ('{{article.writer.pk}}' !== data.writer_pk && data.writer_pk != '{{request.user.pk}}') {
        document.querySelector('.comment-ul').innerHTML += `
            <li class="comment-li comment-li${data_id}">
              <span class="comment-profile-span"><img class="user-img user_img${data_id} comment-profile-img"
                src="${data.user_img}" alt=""
                onerror="this.src='{% static 'img/감자.png' %}'">${data.profile_nickname}<span>${data.comment_obj.created_at}</span></span>
                <span class="comment-content ">${data.comment_obj.content}</span>
                <form class="delete-comment-form" action="" method="POST">
        <input type="submit" class="comment-delete comment-delete${data_id}" onclick="commentDelete(${data_id})"value="삭제">
      </form>
                <form action="" method="POST"
                class="recomment-form${data_id} non-display">
                {% csrf_token %}
                <textarea type="text" class="input-re-comment input-re-comment${data_id}" name="re_comment"
                placeholder="댓글입력"></textarea>
                <div class="input-re-comment-input">
                  <input class="re-comment-btn re-comment-btn${data_id}" type="submit" value="입력하기"
                  ">
                  <input class="re-comment-btn re-comment-cancel-btn${data_id}" type="submit" value="취소하기"
                  onclick="reCommentCancelBtn('${data_id}')">
                  </div>
                  </form>
                  </li>
                  `
      }
      else if(data.writer_pk == '{{request.user.pk}}' && '{{article.writer.pk}}' !== data.writer_pk){
        document.querySelector('.comment-ul').innerHTML += `
        <li class="comment-li comment-li${data_id}">
              <span class="comment-profile-span"><img class="user-img user_img${data_id} comment-profile-img"
                src="${data.user_img}" alt=""
                onerror="this.src='{% static 'img/감자.png' %}'">${data.profile_nickname}<span>${data.comment_obj.created_at}</span></span>
                <span class="comment-content comment-content${data_id}">${data.comment_obj.content}</span>
                <form class="delete-comment-form delete-comment-form${data_id}" action="" method="POST">
        <input type="submit" class="comment-delete comment-delete${data_id}" onclick="commentDelete(${data_id})"value="삭제">
        <button type="submit" class="comment-content-edit comment-content-edit${data_id}"
            onclick="commentContentEditBtn('${data_id}')">수정</button>
      </form>
      <form action="" method="POST" class="edit-comment-form edit-comment-form${data_id} non-display">
          {% csrf_token %}
          <input type="text" class="edit_comment${data_id}" name="edit_text" value="${data.comment_obj.content}">
          <input type="submit" class="edit-comment-btn" value="수정하기" onclick="commentEditBtn('${data_id}')"></input>
          <button type="submit" class="comment-edit-cancel comment-edit-cancel${data_id}"
            onclick="commentEditCancelBtn('${data_id}')">취소하기</button>
        </form>
          <form action="" method="POST"
          class="recomment-form${data_id} non-display" onsubmit="recommentForm('${data_id}')>
          {% csrf_token %}
          <textarea type="text" class="input-re-comment input-re-comment${data_id}" name="re_comment"
          placeholder="댓글입력"></textarea>
          <div class="input-re-comment-input">
            <input class="re-comment-btn re-comment-btn${data_id}" type="submit" value="입력하기"
            ">
            <input class="re-comment-btn re-comment-cancel-btn${data_id}" type="submit" value="취소하기"
            onclick="reCommentCancelBtn('${data_id}')">
            </div>
            </form>
            </li>
            `
      }
    }).catch((error) => {
      console.log('error', error);
    })
  }

// recomment cancel button
function reCommentCancelBtn(comment_pk) {
event.preventDefault();
document.querySelector(`.recomment-form${comment_pk}`).classList.add('non-display');
}

//  detail page recomment ajax function
function recommentForm(comment_pk) {
event.preventDefault();

if (document.querySelector(`.input-re-comment${comment_pk}`).value == '') {
  return
}
let recommentCsrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;
let recomment = document.querySelector(`.input-re-comment${comment_pk}`).value;
document.querySelector(`.recomment-form${comment_pk}`).classList.add('non-display');
let param = {
  // 'article_pk': article_pk,
  'user_pk': '{{request.user.pk}}',
  'writer_pk': '{{article.writer.pk}}',
  'comment_pk': comment_pk,
  're_comment': recomment,
}
fetch("{% url 'social:re_comment' %}", {
  method: 'POST',
  headers: {
    "X-CSRFToken": recommentCsrfValue,
    "X-Requested-With": "XMLHttpRequest"
  },
  body: JSON.stringify(param),
}).then(function (response) {
  // console.log('reass', response)
  return response.json()
}).then(function (data) {
  document.querySelector(`.recomment-form${comment_pk}`).reset();
  console.log(data.recomment_obj)
  let recommentLi = ''
  for (let key in data.recomment_obj) {

    if ('{{article.writer.pk}}' == data.recomment_obj[key]['writer_pk']) {
      recommentLi += `<li class="recomment-li recomment-li${key}">
      <span class="comment-profile-span">
      <img class="user-img comment-profile-img img${data.recomment_obj[key]['id']}" src="${data.recomment_obj[key]['user_img']}"  onerror="this.src='{% static 'img/감자.png' %}'"><strong
            class="owner">판매자</strong> <span>${data.recomment_obj[key]['created_at']}</span></span><br>
            `
    }
    else {
      recommentLi += `<li class="recomment-li recomment-li${key}">
      <span class="comment-profile-span">
      <img class="user-img comment-profile-img img${data.recomment_obj[key]['id']} "  src="${data.recomment_obj[key]['user_img']}" onerror="this.src='{% static 'img/감자.png' %}'">
      ${data.recomment_obj[key]['profile_nickname']} <span>${data.recomment_obj[key]['created_at']}</span></span>
            <br>
            `
    }
    if ('{{request.user.pk}}' == data.recomment_obj[key]['writer_pk']) {
      recommentLi += `
    <span class="comment-content">${data.recomment_obj[key]['content']}</span>
    <form class="delete-recomment-form delete-recomment-form${data.recomment_obj[key]['id']}" action="" method="POST">
      {% csrf_token %}
      <span class="comment-delete comment-delete${data.comment_data.id}"
            onclick="reCommentDelete('${data.recomment_obj[key]['id']}')">삭제</span></li>
          </form>
          `
    }
    else {
      recommentLi += `
    <span class="comment-content">${data.recomment_obj[key]['content']}</span>
          <span class="comment-reply comment-reply${data.comment_data.pk}" onclick="commentReply('${data.comment_data.id}')">답글</span></li>`
    }
  }
  document.querySelector(`.recomment-ul${comment_pk}`).innerHTML = recommentLi

}).catch((error) => {
  console.log('error', error);
})
}

// detail comment buttons clicked non-clicked control 

function commentEditCancelBtn(comment_pk){
  event.preventDefault();
  document.querySelector(`.edit-comment-form${comment_pk}`).classList.add('non-display');
  document.querySelector(`.comment-content${comment_pk}`).classList.remove('non-display');
  document.querySelector(`.delete-comment-form${comment_pk}`).classList.remove('non-display');
  console.log('d')
}
function commentContentEditBtn(comment_pk){
  event.preventDefault();
  document.querySelector(`.edit-comment-form${comment_pk}`).classList.remove('non-display');
  document.querySelector(`.comment-content${comment_pk}`).classList.add('non-display');
  document.querySelector(`.delete-comment-form${comment_pk}`).classList.add('non-display');

}


//detail comment edit function
function commentEditBtn(comment_pk){
  event.preventDefault();
  document.querySelector(`.edit-comment-form${comment_pk}`).addEventListener('submit',EditCommentForm(comment_pk));
}

function EditCommentForm(comment_pk){
event.preventDefault();
edit_comment = document.querySelector(`.edit_comment${comment_pk}`).value;
if (edit_comment == '') {
      return
}
document.querySelector(`.edit-comment-form${comment_pk}`).classList.add('non-display');
  document.querySelector(`.comment-content${comment_pk}`).classList.remove('non-display');
  document.querySelector(`.delete-comment-form${comment_pk}`).classList.remove('non-display');
let param = {
      'edit_comment': edit_comment,
      'comment_pk': comment_pk
    }
    let csrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    
    // ajax통신
    fetch("{% url 'social:edit' %}", {
      method: 'POST',
      headers: {
        "X-CSRFToken": csrfValue,
        "X-Requested-With": "XMLHttpRequest"
      },
      body: JSON.stringify(param),
    }).then(function (response) {
      console.log('reass', response)
      return response.json()
    }).then(function (data) {
      console.log(data)
      console.log(edit_comment = document.querySelector(`.edit_comment${comment_pk}`).value)
      document.querySelector(`.comment-content${comment_pk}`).innerText = edit_comment
     
    }).catch((error) => {
      console.log('error', error);
    })
  }
  

  // detail comment delete ajax function
  function commentDelete(comment_pk) {
    document.querySelector('.delete-comment-form').addEventListener('submit', deleteComment(comment_pk));
  }
  
  function deleteComment(comment_pk) {
    event.preventDefault();
    document.querySelector(`.comment-li${comment_pk}`).classList.add('non-display');

    let param = {
      'article_pk': '{{article.pk}}',
      'user_pk': '{{request.user.pk}}',
      'owner_pk': '{{article.writer.pk}}',
      'comment_pk': comment_pk
    }
    let csrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    
    // ajax통신
    fetch("{% url 'social:delete' %}", {
      method: 'POST',
      headers: {
        "X-CSRFToken": csrfValue,
        "X-Requested-With": "XMLHttpRequest"
      },
      body: JSON.stringify(param),
    }).then(function (response) {
      console.log('reass', response)
      return response.json()
    }).then(function (data) {
      console.log(data)
      console.log('{{comment_pk}}')
     
    }).catch((error) => {
      console.log('error', error);
    })
  }


// detail recomment delete ajax function
function reCommentDelete(recomment_pk){
  document.querySelector(`.delete-recomment-form${recomment_pk}`).addEventListener('submit', deleteReComment(recomment_pk));
}
function deleteReComment(recomment_pk) {
    event.preventDefault();
    document.querySelector(`.recomment-li${recomment_pk}`).classList.add('non-display');

    let param = {
      'recomment_pk': recomment_pk,
      'msg':'recomment_delete',
    }
    let csrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    
    // ajax통신
    fetch("{% url 'social:delete' %}", {
      method: 'POST',
      headers: {
        "X-CSRFToken": csrfValue,
        "X-Requested-With": "XMLHttpRequest"
      },
      body: JSON.stringify(param),
    }).then(function (response) {
      console.log('reass', response)
      return response.json()
    }).then(function (data) {
      console.log(data)
     
    }).catch((error) => {
      console.log('error', error);
    })
  }

  
 // article edit page 이미지 업로드 기능
 const $uploadImgInput = document.querySelector('.upload-img-input');
 const $uploadPreviewImg = document.querySelector('.upload-preview-img');
 const $editImg = document.querySelector('.edit-user-img');
 const $multipleContainer = document.querySelector('.multiple-container');

 $uploadPreviewImg.onclick = () => {
   $uploadImgInput.click();
 }


// article edit page 이미지 여러개 업로드 기능
 $uploadImgInput.onchange = (e) => {
   document.querySelector('.edit-img-div').innerHTML='';
   for (let image of event.target.files) {
     let reader = new FileReader();
     reader.onload = function (event) {
       let img = document.createElement('img');
       img.classList.add('edit-user-img');
       img.setAttribute('src', event.target.result);

       document.querySelector('.edit-img-div').appendChild(img);
     }

     console.log(image);
     reader.readAsDataURL(image);
   }
 }