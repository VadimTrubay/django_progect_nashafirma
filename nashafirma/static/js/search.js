(() => {  
    document.getElementById("search-icon").addEventListener("click", function() {
        document.getElementById("search").submit();
    });
    document.addEventListener("DOMContentLoaded", function () {
        const forms = document.querySelectorAll("form[id^='search']");

        forms.forEach(form => {
            form.addEventListener("submit", function (event) {
                const input = form.querySelector("input[type='text']");
                if (!input.value.trim()) {
                    input.value = " "; // Устанавливаем пробел, если поле пустое
                }
            });
        });
    });
})();