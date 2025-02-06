document.addEventListener("DOMContentLoaded", function () {
  const menuItems = document.querySelectorAll(".menu li");
  let currentPath = window.location.pathname; // Lấy URL hiện tại của trang

  // Loại bỏ dấu chéo cuối nếu có
  if (currentPath.endsWith("/")) {
    currentPath = currentPath.slice(0, -1);
  }

  menuItems.forEach((item) => {
    const link = item.querySelector("a");
    let linkHref = link.getAttribute("href");

    if (linkHref.endsWith("/")) {
      linkHref = linkHref.slice(0, -1);
    }

    if (currentPath.startsWith(linkHref)) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });

  menuItems.forEach((item) => {
    item.addEventListener("click", function () {
      menuItems.forEach((i) => i.classList.remove("active"));
      item.classList.add("active");
    });
  });
});
