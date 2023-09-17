function hide(item) {
    console.log('hide');
    console.log(item.value);
    item.classList.toggle('hidden');
}
function changeColor(item) {
    if (item.classList.contains('btn-primary')) {
        item.classList.remove('btn-primary');
        item.classList.add('btn-danger');
        item.innerHTML = 'Red'
    }
    else if (item.classList.contains('btn-danger')) {
        item.classList.remove('btn-danger');
        item.classList.add('btn-success');
        item.innerHTML = 'Green'
    }
    else if (item.classList.contains('btn-success')) {
        item.classList.remove('btn-success');
        item.classList.add('btn-primary');
        item.innerHTML = 'Blue'
    }
}

let plus_btns = document.querySelectorAll('#settings .pull .plus');
let reload_btns = document.querySelectorAll('#settings .pull .reload');
let close_btns = document.querySelectorAll('#settings .pull .close');
let color_btns = document.querySelectorAll('#settings .pull .color');

plus_btns.forEach(function (item, i, arr) {
    item.onclick = () => hide(item);
});
color_btns.forEach(function (item, i, arr) {
    item.onclick = () => changeColor(item);
});
