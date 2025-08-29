gsap.registerPlugin(ScrollTrigger);

const video = document.getElementById("bg-video");

// ✅ Mobile / Desktop video set karna
// if (window.innerWidth <= 768) {
//   video.src = "video-mobile.mp4";  // mobile ke liye video
// } else {
//   video.src = "video.mp4"; // desktop ke liye video
// }

const videoDuration = 60;

gsap.to(video, {
  currentTime: videoDuration,
  ease: "none",
  scrollTrigger: {
    trigger: ".scroll-spacer",
    start: "top top",
    end: "bottom bottom",
    scrub: 1,
  }
});
