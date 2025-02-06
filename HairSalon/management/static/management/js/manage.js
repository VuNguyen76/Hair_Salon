document.addEventListener("DOMContentLoaded", function () {
  const menuItems = document.querySelectorAll(".menu li");
  const currentPath = window.location.pathname.replace(/\/$/, ""); // Xóa dấu '/' cuối cùng nếu có

  menuItems.forEach((item) => {
    const link = item.querySelector("a");
    if (!link) return; // Nếu không có thẻ <a>, bỏ qua

    const linkHref = link.getAttribute("href").replace(/\/$/, ""); // Xóa dấu '/' cuối cùng nếu có

    // Kiểm tra đường dẫn phải khớp chính xác với đường dẫn hiện tại
    if (currentPath === linkHref) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });
});
