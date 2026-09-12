document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("stadium-form");
    const buttons = form.querySelectorAll(".stadium-button");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const stadiumName = button.getAttribute("data-stadium");
            const hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "stadium";
            hiddenInput.value = stadiumName;
            form.appendChild(hiddenInput);

            form.submit(); // Submit the form
        });
    });
});
