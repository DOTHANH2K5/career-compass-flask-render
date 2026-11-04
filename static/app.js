const skillsField = document.querySelector('textarea[name="skills"]');
const charCount = document.querySelector("#char-count");

if (skillsField && charCount) {
  const updateCount = () => { charCount.textContent = String(skillsField.value.length); };
  skillsField.addEventListener("input", updateCount);
  updateCount();
}

// Prevent accidental double submission while the form is being processed.
const form = document.querySelector(".diagnosis-form");
if (form) {
  form.addEventListener("submit", () => {
    const button = form.querySelector('button[type="submit"]');
    if (button) {
      button.disabled = true;
      button.innerHTML = '診断しています… <span>✓</span>';
    }
  });
}
