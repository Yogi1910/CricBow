document.addEventListener("DOMContentLoaded", function () {
  const selectButtons = document.querySelectorAll('.select-button');
  selectButtons.forEach(button => {
    button.addEventListener('click', function(event) { // Add the event parameter
      event.preventDefault(); // Prevent the default behavior (page refresh)
      selectTeam(this);
    });
  });
});

function selectTeam(button) {
  const allButtons = document.querySelectorAll('.select-button');
  const selectedContainer = button.closest('.selected-team');

  if (selectedContainer.classList.contains('selected')) {
    selectedContainer.classList.remove('selected');
    button.textContent = 'Select';
  } else {
    allButtons.forEach(btn => {
      btn.textContent = 'Select';
      btn.disabled = false;
    });
    selectedContainer.classList.add('selected');
    button.textContent = 'Selected';

    const otherContainer = selectedContainer.nextElementSibling || selectedContainer.previousElementSibling;
    if (otherContainer) {
      const otherButton = otherContainer.querySelector('.select-button');
      otherButton.disabled = true;
    }
  }


}

