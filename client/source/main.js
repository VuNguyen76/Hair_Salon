(() => {
  handleBanner(5);
  handleUserMenu();
  handleComment();
})();
function handleBanner(bannerLength) {
  const listBanner = document.querySelector(".list_banner");
  const nextBtn = document.querySelector(".next_banner");
  const prevBtn = document.querySelector(".prev_banner");
  let currentBanner = 1;
  let intervalID;
  const updateBanner = () => {
    listBanner.style.transform = `translateX(${(currentBanner - 1) * -1200}px)`;
  };
  const autoSlideBanner = () => {
    clearInterval(intervalID);
    intervalID = setInterval(() => {
      currentBanner++;
      if (currentBanner > bannerLength) currentBanner = 1;
      updateBanner();
    }, 3000);
  };
  autoSlideBanner();
  nextBtn.onclick = () => {
    currentBanner++;
    if (currentBanner > bannerLength) currentBanner = 1;
    updateBanner();
    autoSlideBanner();
  };
  prevBtn.onclick = () => {
    currentBanner--;
    if (currentBanner < 1) currentBanner = 5;
    updateBanner();
    autoSlideBanner();
  };
}
function handleUserMenu() {
  const user = document.querySelector(".user");
  const userDashboard = document.querySelector(".user-dashboard");
  user.onclick = () => {
    userDashboard.classList.toggle("hidden");
  };
  window.onclick = (e) => {
    if (!e.target.closest(".user-dashboard") && !e.target.closest(".user")) {
      userDashboard.classList.add("hidden");
    }
  };
}
function handleComment() {
  const comment = document.querySelector(".comment");
  const commentDashboard = document.querySelector(".comment-dashboard");
  const rowDashboard = document.querySelector(".row-comment");
  const userDashboard = document.querySelector(".user-dashboard");
  comment.onclick = () => {
    commentDashboard.classList.toggle("hidden");
    userDashboard.classList.toggle("hidden");
    console.log(4);
  };
  window.onclick = (e) => {
    e.target.closest(".comment-dashboard");
    if (!e.target.closest(".row-comment") && !e.target.closest(".comment")) {
      commentDashboard.classList.add("hidden");
    }
  };
}
