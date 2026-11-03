(() => {
  "use strict";

  const SLIDE_DURATION_MS = 18_000;
  const app = document.querySelector("#app");
  const template = document.querySelector("#slide-template");
  const dotsContainer = document.querySelector("#slide-dots");
  const previousButton = document.querySelector("#previous");
  const nextButton = document.querySelector("#next");
  const toggleButton = document.querySelector("#toggle");
  const progressBar = document.querySelector("#progress-bar");

  let slides = [];
  let dots = [];
  let activeIndex = 0;
  let timer = null;
  let paused = false;

  const formatDigestDate = (value) => {
    const parts = String(value || "").split("-").map(Number);
    const date = parts.length === 3
      ? new Date(parts[0], parts[1] - 1, parts[2])
      : new Date();
    return new Intl.DateTimeFormat("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      weekday: "long",
    }).format(date);
  };

  const formatPublishedTime = (value) => {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "时间待核实";
    return new Intl.DateTimeFormat("zh-CN", {
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    }).format(date);
  };

  const getDomain = (url) => {
    try {
      return new URL(url).hostname.replace(/^www\./, "");
    } catch {
      return "原始信源";
    }
  };

  const resolveScreenshot = (path) => {
    if (!path) return "";
    return `./${String(path).replace(/^\/+/, "")}`;
  };

  const createSlide = (item, digest, index) => {
    const fragment = template.content.cloneNode(true);
    const slide = fragment.querySelector(".slide");
    slide.dataset.index = String(index);
    slide.querySelector(".display-date").textContent = formatDigestDate(digest.date);
    slide.querySelector(".edition-badge").textContent = digest.edition === "test"
      ? "测试版"
      : "自动更新";
    slide.querySelector(".story-index").textContent = `${String(index + 1).padStart(2, "0")} / ${String(digest.items.length).padStart(2, "0")}`;
    slide.querySelector(".story-title").textContent = item.title;
    slide.querySelector(".story-summary").textContent = item.summary;
    slide.querySelector(".story-why").textContent = item.why_it_matters;
    slide.querySelector(".source-name").textContent = item.source;
    slide.querySelector(".published-time").textContent = formatPublishedTime(item.published_at);

    const link = slide.querySelector(".source-link");
    link.href = item.url;
    const domain = getDomain(item.url);
    slide.querySelector(".browser-domain").textContent = domain;

    const image = slide.querySelector(".page-capture");
    const fallback = slide.querySelector(".capture-fallback");
    const screenshot = resolveScreenshot(item.screenshot);
    if (screenshot) {
      image.src = screenshot;
      image.addEventListener("error", () => {
        image.style.display = "none";
        fallback.style.display = "grid";
      });
    } else {
      image.style.display = "none";
      fallback.style.display = "grid";
    }
    return fragment;
  };

  const restartProgress = () => {
    progressBar.classList.remove("running");
    void progressBar.offsetWidth;
    if (!paused) progressBar.classList.add("running");
  };

  const scheduleNext = () => {
    window.clearTimeout(timer);
    if (!paused) {
      timer = window.setTimeout(() => showSlide(activeIndex + 1), SLIDE_DURATION_MS);
    }
  };

  const showSlide = (index) => {
    if (!slides.length) return;
    activeIndex = (index + slides.length) % slides.length;
    slides.forEach((slide, slideIndex) => {
      const isActive = slideIndex === activeIndex;
      slide.classList.toggle("active", isActive);
      slide.setAttribute("aria-hidden", String(!isActive));
    });
    dots.forEach((dot, dotIndex) => {
      dot.classList.toggle("active", dotIndex === activeIndex);
      dot.setAttribute("aria-current", dotIndex === activeIndex ? "true" : "false");
    });
    restartProgress();
    scheduleNext();
  };

  const setPaused = (value) => {
    paused = value;
    toggleButton.textContent = paused ? "▶" : "Ⅱ";
    toggleButton.setAttribute("aria-label", paused ? "继续轮播" : "暂停轮播");
    if (paused) {
      window.clearTimeout(timer);
      progressBar.classList.remove("running");
    } else {
      restartProgress();
      scheduleNext();
    }
  };

  const bindControls = () => {
    previousButton.addEventListener("click", () => showSlide(activeIndex - 1));
    nextButton.addEventListener("click", () => showSlide(activeIndex + 1));
    toggleButton.addEventListener("click", () => setPaused(!paused));
    document.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") showSlide(activeIndex - 1);
      if (event.key === "ArrowRight") showSlide(activeIndex + 1);
      if (event.key === " ") {
        event.preventDefault();
        setPaused(!paused);
      }
    });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        window.clearTimeout(timer);
      } else if (!paused) {
        restartProgress();
        scheduleNext();
      }
    });
  };

  const initialize = async () => {
    try {
      const response = await fetch("./data/latest.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const digest = await response.json();
      if (!Array.isArray(digest.items) || digest.items.length !== 5) {
        throw new Error("日报数据必须恰好包含五条新闻");
      }

      app.innerHTML = "";
      digest.items.forEach((item, index) => {
        app.appendChild(createSlide(item, digest, index));
        const dot = document.createElement("button");
        dot.className = "slide-dot";
        dot.type = "button";
        dot.setAttribute("aria-label", `查看第 ${index + 1} 条新闻`);
        dot.addEventListener("click", () => showSlide(index));
        dotsContainer.appendChild(dot);
      });
      slides = [...document.querySelectorAll(".slide")];
      dots = [...document.querySelectorAll(".slide-dot")];
      bindControls();
      showSlide(0);
    } catch (error) {
      app.innerHTML = `
        <section class="error-state">
          <h1>日报暂时无法载入</h1>
          <p>${String(error.message || error)}</p>
        </section>`;
      document.querySelector(".presentation-controls").style.display = "none";
      document.querySelector(".progress-track").style.display = "none";
    }
  };

  initialize();
})();

