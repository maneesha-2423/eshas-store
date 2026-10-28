
"use strict";

/* =====================================================
   EESHA'S STORE — FRONTEND INTERACTIONS
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {
    setupImageFallbacks();
    setupQuantityInputs();
    setupFormProtection();
    setupSearchShortcut();
    setupProductCardEffects();
    setupFlashMessages();
});


/* ---------------- IMAGE FALLBACKS ---------------- */

// Replace a broken product or category image with a local placeholder.
function setupImageFallbacks() {
    document.querySelectorAll("img").forEach((image) => {
        image.addEventListener("error", () => {
            if (image.dataset.fallbackUsed === "true") {
                return;
            }

            image.dataset.fallbackUsed = "true";
            image.src = "https://placehold.co/600x750/faf7f2/74544b?text=Eesha%27s+Store";
        });
    });
}


/* ---------------- QUANTITY VALIDATION ---------------- */

// Prevent quantities outside the allowed range.
function setupQuantityInputs() {
    document.querySelectorAll('input[name="quantity"]').forEach((input) => {
        input.addEventListener("change", () => {
            const minimum = Number(input.min || 1);
            const maximum = Number(input.max || 10);
            let value = Number(input.value);

            if (!Number.isFinite(value)) {
                value = minimum;
            }

            value = Math.floor(value);
            value = Math.max(minimum, Math.min(value, maximum));

            input.value = String(value);
        });
    });
}


/* ---------------- FORM SUBMISSION ---------------- */

// Avoid accidental double-click submissions.
function setupFormProtection() {
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                form.reportValidity();
                return;
            }

            // Let the user click again if the form has validation errors.
            if (form.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

            form.dataset.submitting = "true";

            const submitButton = event.submitter;

            if (submitButton && submitButton.type !== "submit") {
                form.dataset.submitting = "false";
            }
        });
    });
}


/* ---------------- SEARCH SHORTCUT ---------------- */

// Press "/" to focus the product search input on pages that have one.
function setupSearchShortcut() {
    document.addEventListener("keydown", (event) => {
        const activeTag = document.activeElement?.tagName;
        const isTyping =
            activeTag === "INPUT" ||
            activeTag === "TEXTAREA" ||
            activeTag === "SELECT" ||
            document.activeElement?.isContentEditable;

        if (
            event.key === "/" &&
            !isTyping &&
            !event.ctrlKey &&
            !event.metaKey &&
            !event.altKey
        ) {
            const searchInput = document.querySelector(
                'input[name="q"], input[type="search"]'
            );

            if (searchInput) {
                event.preventDefault();
                searchInput.focus();
            }
        }

        if (
            event.key === "Escape" &&
            document.activeElement?.matches(
                'input[name="q"], input[type="search"]'
            )
        ) {
            document.activeElement.value = "";
            document.activeElement.blur();
        }
    });
}


/* ---------------- PRODUCT CARD EFFECTS ---------------- */

// Add a small visual cue when a user hovers over a product card.
function setupProductCardEffects() {
    const cards = document.querySelectorAll(".product-card");

    cards.forEach((card) => {
        card.addEventListener("mouseenter", () => {
            card.classList.add("is-hovered");
        });

        card.addEventListener("mouseleave", () => {
            card.classList.remove("is-hovered");
        });
    });
}


/* ---------------- FLASH MESSAGES ---------------- */

// Make flash messages accessible and dismissible.
// Bootstrap handles the actual dismissal interaction.
function setupFlashMessages() {
    document.querySelectorAll(".alert").forEach((alert) => {
        alert.setAttribute("role", "alert");
        alert.setAttribute("aria-live", "polite");
    });
}
