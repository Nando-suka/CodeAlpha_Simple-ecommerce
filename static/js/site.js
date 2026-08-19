document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll(".quantity-control").forEach((control) => {
    const input = control.querySelector("input");
    control.querySelector("[data-quantity-minus]")?.addEventListener("click", () => {
      input.value = Math.max(Number(input.min || 1), Number(input.value || 1) - 1);
    });
    control.querySelector("[data-quantity-plus]")?.addEventListener("click", () => {
      input.value = Math.min(Number(input.max || 99), Number(input.value || 1) + 1);
    });
  });

  document.querySelectorAll(".toast").forEach((toast) => {
    window.setTimeout(() => toast.classList.add("toast-hide"), 4200);
  });
});
