const tabPersona = document.getElementById("tab-persona");
const tabInstitucion = document.getElementById("tab-institucion");
const formPersona = document.getElementById("form-persona");
const formInstitucion = document.getElementById("form-institucion");

tabPersona.addEventListener("click", () => {
  tabPersona.classList.add("active");
  tabInstitucion.classList.remove("active");
  formPersona.classList.add("active");
  formInstitucion.classList.remove("active");
});

tabInstitucion.addEventListener("click", () => {
  tabInstitucion.classList.add("active");
  tabPersona.classList.remove("active");
  formInstitucion.classList.add("active");
  formPersona.classList.remove("active");
});
