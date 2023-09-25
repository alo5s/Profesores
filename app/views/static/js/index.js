const navboggle = document.querySelector(".nav-toggle")
const navtoggle = document.querySelector(".content-nav-login ")

navboggle.addEventListener("click", () => {
  navtoggle.classList.toggle("nav-link-ul-visible")
})



function showFields() {
    var taskSelect = document.getElementById("task-form");
    var estudianteFields = document.getElementById("task-estudiante");
    var grupoFields = document.getElementById("task-grupo");

    estudianteFields.style.display = "none";
    grupoFields.style.display = "none";

    if (taskSelect.value === "estudiantes") {
        estudianteFields.style.display = "block";
    } else if (taskSelect.value === "grupo") {
        grupoFields.style.display = "block";
    }
}




