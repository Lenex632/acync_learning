function switch_visual(items) {
    items.forEach(function (item, i, arr) {
        item.classList.toggle('d-none');
    })
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
function addLight(item) {
    let post_item = {
        'id': item.parentElement.id.split('-')[1],
        'color': item.parentElement.children[0].innerHTML,
        'value': item.parentElement.children[1].value
    }

    fetch('http://0.0.0.0:8080/add_light', {
        method: 'POST',
        body: JSON.stringify(post_item)
    })
        .then(response => response.json())
        .then(json => console.log(JSON.stringify(json)));
}
function addSetting() {
    fetch('http://0.0.0.0:8080/add_setting', {
        method: 'POST',
    })
        .then(response => response.json())
        .then(json => console.log(JSON.stringify(json)));
}
function flash(item) {
    item.classList.toggle('active')
    setTimeout(() => item.classList.toggle('active'), 200);
}


let plus_btns = document.querySelectorAll('#settings .pull .plus');
let reload_btns = document.querySelectorAll('#settings .pull .reload');
let close_btns = document.querySelectorAll('#settings .pull .close');
let color_btns = document.querySelectorAll('#settings .pull .color');

let lights = document.querySelectorAll('#lights .light')

plus_btns.forEach(function (item, i, arr) {
    item.onclick = function() {
        console.log(item);
        switch_visual(item.parentElement.querySelectorAll('.plus, .reload, .close'));
        addLight(item);
        addSetting();
    };
});
color_btns.forEach(function (item, i, arr) {
    item.onclick = () => changeColor(item);
});

lights.forEach(function (item, i, arr) {
    item.onclick = () => flash(item);
});
