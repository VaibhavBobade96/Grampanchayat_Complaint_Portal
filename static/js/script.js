document.addEventListener("DOMContentLoaded", function () {

    /* ================= AUTO DISMISS ALERTS ================= */
    setTimeout(() => {
        const alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => alert.remove());
    }, 5000);


    /* ================= DARK / LIGHT MODE TOGGLE ================= */
    const toggleBtn = document.getElementById("themeToggle");
    const body = document.body;

    console.log("script.js loaded"); // 🔍 DEBUG CHECK

    if (!toggleBtn) {
        console.error("themeToggle button not found");
        return;
    }

    // Load saved theme
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
        toggleBtn.innerText = "☀️ Light";
    } else {
        toggleBtn.innerText = "🌙 Dark";
    }

    // Toggle click
    toggleBtn.addEventListener("click", function () {
        body.classList.toggle("dark-mode");

        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            toggleBtn.innerText = "☀️ Light";
        } else {
            localStorage.setItem("theme", "light");
            toggleBtn.innerText = "🌙 Dark";
        }
    });

});
