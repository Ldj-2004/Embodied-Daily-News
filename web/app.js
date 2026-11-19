(() => {
  "use strict";

  const SLIDE_DURATION_MS = 25_000;
  const COMPANY_LABELS = [
    ["Google DeepMind", ["google deepmind", "deepmind", "gemini robotics", "谷歌deepmind"]],
    ["Microsoft", ["microsoft", "微软"]],
    ["Boston Dynamics", ["boston dynamics", "波士顿动力"]],
    ["Unitree", ["unitree", "宇树"]],
    ["Figure AI", ["figure ai"]],
    ["Agility Robotics", ["agility robotics"]],
    ["NVIDIA", ["nvidia", "英伟达"]],
    ["Amazon Robotics", ["amazon robotics", "亚马逊机器人"]],
    ["Tesla", ["tesla", "optimus", "特斯拉"]],
    ["Hyundai", ["hyundai motor", "hyundai", "现代汽车"]],
    ["DJI", ["dji", "大疆"]],
    ["UBTECH", ["ubtech", "优必选"]],
    ["AgiBot", ["agibot", "智元机器人"]],
    ["ABB", ["abb robotics", "abb机器人"]],
    ["KUKA", ["kuka", "库卡"]],
    ["FANUC", ["fanuc", "发那科"]],
  ];
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
  let dateTimer = null;

  const formatBeijingDate = (date = new Date()) => (
    new Intl.DateTimeFormat("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      weekday: "long",
      timeZone: "Asia/Shanghai",
    }).format(date)
  );

  const updateDisplayDates = () => {
    const currentDate = formatBeijingDate();
    document.querySelectorAll(".display-date").forEach((element) => {
      element.textContent = currentDate;
    });
  };

  const scheduleBeijingMidnightUpdate = () => {
    window.clearTimeout(dateTimer);
    updateDisplayDates();
    const parts = Object.fromEntries(
      new Intl.DateTimeFormat("en-CA", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        timeZone: "Asia/Shanghai",
      }).formatToParts().map((part) => [part.type, part.value]),
    );
    const nextMidnightUtc = Date.UTC(
      Number(parts.year),
      Number(parts.month) - 1,
      Number(parts.day) + 1,
    ) - (8 * 60 * 60 * 1000);
    dateTimer = window.setTimeout(
      scheduleBeijingMidnightUpdate,
      Math.max(1_000, nextMidnightUtc - Date.now() + 150),
    );
  };

  const companyShortName = (item) => {
    if (item.company_short_name) return item.company_short_name;
    const text = [item.title, item.summary, item.source].join(" ").toLowerCase();
    let best = null;
    COMPANY_LABELS.forEach(([label, aliases]) => {
      aliases.forEach((alias) => {
        const position = text.indexOf(alias);
        if (position >= 0 && (!best || position < best.position)) {
          best = { label, position };
        }
      });
    });
    if (best) return best.label;
    return /^[\x00-\x7F]+$/.test(item.source || "")
      ? item.source
      : "Global Robotics";
  };

  const resolveScreenshot = (path) => {
    if (!path) return "";
    return `./${String(path).replace(/^\/+/, "")}`;
  };

  const createSlide = (item, digest, index) => {
    const fragment = template.content.cloneNode(true);
    const slide = fragment.querySelector(".slide");
    const isResearch = item.source_kind === "research";
    const isSpecial = item.source_kind === "special";
    slide.classList.toggle("research-slide", isResearch);
    slide.classList.toggle("special-slide", isSpecial);
    slide.dataset.index = String(index);
    slide.querySelector(".display-date").textContent = formatBeijingDate();
    slide.querySelector(".edition-badge").textContent = digest.edition === "test"
      ? "测试版"
      : "自动更新";
    slide.querySelector(".story-index").textContent = `${String(index + 1).padStart(2, "0")} / ${String(digest.items.length).padStart(2, "0")}`;
    slide.querySelector(".story-title").textContent = item.title;
    slide.querySelector(".story-summary").textContent = item.summary;
    slide.querySelector(".story-why").textContent = item.why_it_matters;

    const link = slide.querySelector(".source-link");
    link.href = item.url;
    slide.querySelector(".browser-domain").textContent = isResearch
      ? "arXiv"
      : companyShortName(item);
    slide.querySelector(".capture-label").textContent = isResearch
      ? "论文图表"
      : isSpecial
        ? "特别关注"
        : "精选现场图";

    const image = slide.querySelector(".page-capture");
    image.alt = isResearch
      ? "论文中的代表性图表"
      : isSpecial
        ? "特别关注新闻配图"
        : "新闻中的机器人操作或部署画面";
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
        updateDisplayDates();
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
      if (
        !Array.isArray(digest.items)
        || digest.items.length < 15
        || digest.items.length > 16
      ) {
        throw new Error("日报数据必须包含十五条常规内容，最多再加一条特别关注");
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
      scheduleBeijingMidnightUpdate();
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


