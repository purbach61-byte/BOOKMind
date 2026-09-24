// ── Rating Slider Live Update ──────────────────────────────────────────────
const slider  = document.getElementById("rating-slider");
const display = document.getElementById("rating-display");

if (slider && display) {
    slider.addEventListener("input", () => {
        display.textContent = parseFloat(slider.value).toFixed(1) + " ⭐";
    });
}

// ── Animate score bars on results page ────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    const fills = document.querySelectorAll(".score-fill");
    fills.forEach(el => {
        const target = el.style.width;
        el.style.width = "0%";
        setTimeout(() => { el.style.width = target; }, 200);
    });
});
