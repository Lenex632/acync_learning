function hide(item) {
    console.log('hide');
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
    item.onclick = function() {
        console.log(item);
        hide(item);
        post_function(item);
    };
});
color_btns.forEach(function (item, i, arr) {
    item.onclick = () => changeColor(item);
});


function post_function(item) {
    let post_item = {
        'id': item.parentElement.id,
        'color': item.parentElement.children[0].innerHTML,
        'value': item.parentElement.children[1].value
    }

    fetch('http://0.0.0.0:8080/post', {
        method: 'POST',
        headers: {
           "Content-type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify(post_item)
    })
        .then(response => response.json())
        .then(json => console.log(JSON.stringify(json)));
}
