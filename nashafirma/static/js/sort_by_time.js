(() => {
  document.addEventListener('DOMContentLoaded', function () {
    const radios = document.querySelectorAll('input[name="time"]');
    radios.forEach(function (radio) {
      radio.addEventListener('change', function () {
        this.form.submit();  // Автоматическая отправка формы при выборе
      });
    });
  });
})();