
// category-list nav menu 삭제가능
document.querySelector('.menu-all').classList.remove('checked');
document.querySelector('.menu-category').classList.add('checked');

document.querySelector('.select-sub-form').onchange = (e) => {
$selectForm = document.querySelector('.select-sub-form');
$selectForm.submit();
}