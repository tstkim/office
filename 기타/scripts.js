const menu = document.getElementById('menu');
const items = menu.querySelectorAll('li');

items.forEach(item => {
    item.addEventListener('dragstart', dragStart);
    item.addEventListener('dragover', dragOver);
    item.addEventListener('drop', drop);
    item.addEventListener('dragend', dragEnd);
});

function dragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.innerText);
    e.target.classList.add('dragging');
}

function dragOver(e) {
    e.preventDefault();
    const draggingItem = document.querySelector('.dragging');
    const currentItem = e.target;
    if (currentItem !== draggingItem) {
        menu.insertBefore(draggingItem, currentItem);
    }
}

function drop(e) {
    e.preventDefault();
    const data = e.dataTransfer.getData('text');
    e.target.classList.remove('dragging');
}

function dragEnd(e) {
    e.target.classList.remove('dragging');
}
