document.addEventListener("DOMContentLoaded", function () {
  const menuItems = document.querySelectorAll(".menu li");
  let currentPath = window.location.pathname; // Lấy URL hiện tại của trang

  // Loại bỏ dấu chéo cuối nếu có
  if (currentPath.endsWith("/")) {
    currentPath = currentPath.slice(0, -1);
  }

  // Duyệt qua tất cả các mục trong menu
  menuItems.forEach((item) => {
    const link = item.querySelector("a");
    let linkHref = link.getAttribute("href");

    // Loại bỏ dấu chéo cuối nếu có trong href của link
    if (linkHref.endsWith("/")) {
      linkHref = linkHref.slice(0, -1);
    }

    // So sánh đường dẫn hiện tại với href của link
    if (linkHref === currentPath) {
      // Nếu href của link trùng với URL hiện tại, thêm class 'active'
      item.classList.add("active");
    } else {
      // Nếu không trùng, loại bỏ class 'active'
      item.classList.remove("active");
    }
  });

  // Thêm sự kiện click để thay đổi active class khi người dùng click vào menu
  menuItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Loại bỏ 'active' class từ tất cả các mục
      menuItems.forEach((i) => i.classList.remove("active"));

      // Thêm 'active' class vào mục được chọn
      item.classList.add("active");
    });
  });
});
