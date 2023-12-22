(() => {  
const checkbox = document.getElementById('checkbox');
    const registrationBtn = document.getElementById('registrationBtn');

    checkbox.addEventListener('change', function () {
        registrationBtn.disabled = !this.checked;});

document.addEventListener("DOMContentLoaded", function () {
    var productNotes = document.querySelectorAll(".product-note");

    productNotes.forEach(function (note) {
        note.addEventListener("mouseover", function () {
            note.querySelector(".truncated-text").style.display = "none";
            note.querySelector(".full-text").style.display = "inline";
        });

        note.addEventListener("mouseout", function () {
            note.querySelector(".full-text").style.display = "none";
            note.querySelector(".truncated-text").style.display = "inline";
        });
    });
});
})();