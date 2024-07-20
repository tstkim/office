// 드롭앤드롭 방식의 메뉴
document.addEventListener('DOMContentLoaded', () => {
    const menu = document.getElementById('menu');
    
    menu.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', e.target.innerText);
    });

    menu.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    menu.addEventListener('drop', (e) => {
        e.preventDefault();
        const data = e.dataTransfer.getData('text/plain');
        const target = e.target;
        
        if (target.tagName === 'LI') {
            target.innerText = data;
        }
    });
});
