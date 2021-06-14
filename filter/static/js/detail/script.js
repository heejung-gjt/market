
  document.querySelector('.menu-all').classList.remove('checked');

  // 좋아요 토글

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
      console.log('reass',response)
      return response.json()
    }).then(function (data) {
      console.log(data)
      let likedIcon = document.querySelector(`.detail-like`);
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

//   // 댓글 ajax
// function commentBtn(article_pk) {
// event.preventDefault();
// let commentCsrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;
// let comment = document.querySelector('.input-comment').value;
// let param = {
//   'article_pk': article_pk,
//   'user_pk':'{{request.user.pk}}',
//   'owner_pk':'{{article.writer.pk}}',
//   'comment': comment,
// }
// fetch("{% url 'social:comment' %}", {
//   method: 'POST',
//   headers: {
//     "X-CSRFToken": commentCsrfValue,
//     "X-Requested-With": "XMLHttpRequest"
//   },
//   body: JSON.stringify(param),
// }).then(function (response) {
//   console.log('reass', response)
//   return response.json()
// }).then(function (data) {
//   console.log(data)
//   document.querySelector('.comment-ul').innerHTML += `
//   <li class="comment-li${data.comment_pk}">
//   <span>${data.user} - </span><span class="comment">${data.comment}</span>
//         <div class="re-comment-form-div${data.comment_pk}}">
//           <form action=""method="POST">
//             {% csrf_token %}
//             <input type="text" class="input-re-comment${data.comment_pk}" name="re-comment" placeholder="댓글입력">
//         <input class="re-comment-btn${data.comment_pk}" type="submit"value="입력하기" onclick="reCommentBtn(${data.comment_pk})">
//           </form>
//       </div>
//       </li>
// `

// }).catch((error) => {
//   console.log('error', error);
// })
// }

// // // 재댓글
// function reCommentBtn(comment_pk){
//   event.preventDefault(); 
//   console.log(comment_pk)
//   console.log('hh');
  
//   if(document.querySelector(`.input-re-comment${comment_pk}`).value == ''){
//     return
//   }

// let commentCsrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;
// let recomment = document.querySelector(`.input-re-comment${comment_pk}`).value;
// let param = {
//   // 'article_pk': article_pk,
//   'user_pk':'{{request.user.pk}}',
//   'writer_pk':'{{article.writer.pk}}',
//   'comment_pk':comment_pk,
//   're_comment': recomment,
//   // 're_comment_pk':
// }
// fetch("{% url 'social:re_comment' %}", {
//   method: 'POST',
//   headers: {
//     "X-CSRFToken": commentCsrfValue,
//     "X-Requested-With": "XMLHttpRequest"
//   },
//   body: JSON.stringify(param),
// }).then(function (response) {
//   console.log('reass', response)
//   return response.json()
// }).then(function (data) {
//   document.querySelector(`.recomment-ul${comment_pk}`).innerHTML+=`
//           <li class="recommet-li"><span>${data.comment_data.writer}님에게 답장<span> ${data.re_comment}</li>
//   `
//   console.log('daaaaya',data)

// }).catch((error) => {
//   console.log('error', error);
// })
// }
// function reCommentCancelBtn(comment_pk){
//   event.preventDefault();
//   console.log('hhh')
//   document.querySelector(`.re-comment-form-div${comment_pk}`).style.display='none';
// }



function commentReply(comment_pk){
  document.querySelector(`.recomment-form${comment_pk}`).classList.remove('non-display');
}

function reCommentCancelBtn(comment_pk){
  event.preventDefault();
  document.querySelector(`.recomment-form${comment_pk}`).classList.add('non-display');
}

function reCommentBtn(comment_pk){
  // event.preventDefault();
  document.querySelector(`.re-comment-form-div${comment_pk}`).classList.add('non-display');
  document.querySelector(`recomment-form${comment_pk}`).submit();
}

function commentDelete(comment_pk){
  document.querySelector(`.comment-li${comment_pk}`).classList.add('non-display');
  document.querySelector(`recomment-form${comment_pk}`).submit();

}

function reCommentDelete(recomment_pk){

}

// comment ajax
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
    'user_pk':'{{request.user.pk}}',
    'owner_pk': '{{article.writer.pk}}'
  }
  // console.log(param)
  let csrfValue = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  // ajax통신
  fetch("{% url 'social:comment' %}", {
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
    $commentForm.reset()

    
  }).catch((error) => {
    console.log('error', error);
  })

} 
