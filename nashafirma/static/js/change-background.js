(() => {
// JavaScript код для изменения фона сайта
function changeBackground() {
    const container = document.querySelector('.container');
    const backgrounds = ['background_3.jpg']
    const randomBackground = backgrounds[Math.floor(Math.random() * backgrounds.length)];
    container.style.backgroundImage = `url('/static/images/${randomBackground}')`;
}

// Вызов функции при смене страницы или событии, которое вы хотите использовать для изменения фона сайта
// Например, вызов функции при загрузке страницы
window.addEventListener('load', changeBackground);
  })();