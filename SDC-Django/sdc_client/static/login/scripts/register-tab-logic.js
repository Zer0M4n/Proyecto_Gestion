const tabPerson = document.getElementById("tab-person");
const tabInstitution = document.getElementById("tab-institution");
const formPerson = document.getElementById("form-person");
const formInstitution = document.getElementById("form-institution");

tabPerson.addEventListener("click", () => {
  tabPerson.classList.add("active");
  tabInstitution.classList.remove("active");
  formPerson.classList.add("active");
  formInstitution.classList.remove("active");
});

tabInstitution.addEventListener("click", () => {
  tabInstitution.classList.add("active");
  tabPerson.classList.remove("active");
  formInstitution.classList.add("active");
  formPerson.classList.remove("active");
});
