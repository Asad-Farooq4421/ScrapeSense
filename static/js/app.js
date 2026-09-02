// 1. THREE.JS 3D PARTICLE MATRIX
const init3DScene = () => {
  const canvas = document.getElementById("bg3d");
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 1000);
  camera.position.z = 400;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const particleCount = 500;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);

  for (let i = 0; i < particleCount * 3; i += 3) {
    positions[i] = (Math.random() - 0.5) * 1200;
    positions[i + 1] = (Math.random() - 0.5) * 1200;
    positions[i + 2] = (Math.random() - 0.5) * 800;
  }

  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const material = new THREE.PointsMaterial({
    color: 0x10B981,
    size: 2.5,
    transparent: true,
    opacity: 0.25
  });

  const particles = new THREE.Points(geometry, material);
  scene.add(particles);

  const animate = () => {
    requestAnimationFrame(animate);
    particles.rotation.y += 0.0004;
    particles.rotation.x += 0.0002;
    renderer.render(scene, camera);
  };
  animate();

  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
};

// 2. TOAST NOTIFICATIONS
const showToast = (message, type = "info") => {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;

  const iconMap = {
    success: '<i class="fa-solid fa-circle-check text-green"></i>',
    error: '<i class="fa-solid fa-circle-xmark text-red"></i>',
    info: '<i class="fa-solid fa-circle-info" style="color:#3B82F6;"></i>'
  };

  toast.innerHTML = `${iconMap[type] || ""} <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
};

// 3. CHARTS
let chartPriceInstance = null;
let chartShareInstance = null;

const renderCharts = (analytics) => {
  if (!analytics || !analytics.charts) return;

  const ctxPrice = document.getElementById("chartPrice").getContext("2d");
  const ctxShare = document.getElementById("chartShare").getContext("2d");

  if (chartPriceInstance) chartPriceInstance.destroy();
  if (chartShareInstance) chartShareInstance.destroy();

  // Price comparison
  chartPriceInstance = new Chart(ctxPrice, {
    type: "bar",
    data: {
      labels: analytics.charts.platform_comparison.labels,
      datasets: [{
        label: "Avg Price ($)",
        data: analytics.charts.platform_comparison.averages,
        backgroundColor: ["#F59E0B", "#3B82F6", "#F97316"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { grid: { color: "#E4E4E7" }, ticks: { color: "#52525B" } },
        x: { grid: { display: false }, ticks: { color: "#52525B" } }
      }
    }
  });

  // Store share
  chartShareInstance = new Chart(ctxShare, {
    type: "doughnut",
    data: {
      labels: analytics.charts.platform_share.labels,
      datasets: [{
        data: analytics.charts.platform_share.counts,
        backgroundColor: ["#F59E0B", "#3B82F6", "#F97316"],
        borderWidth: 2,
        borderColor: "#ffffff"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "right" } }
    }
  });
};

// 4. DATA FETCHING
const fetchAnalytics = async () => {
  try {
    const res = await fetch("/api/analytics");
    const data = await res.json();
    if (data.ready) {
      document.getElementById("statTotal").innerText = data.total_products;
      document.getElementById("statAvg").innerText = `$${data.avg_price}`;
      document.getElementById("statMin").innerText = `$${data.min_price}`;
      document.getElementById("statMax").innerText = `$${data.max_price}`;
      renderCharts(data);
    }
  } catch (err) {
    console.error("Analytics fetch error:", err);
  }
};

const fetchProducts = async () => {
  const source = document.getElementById("selectSourceFilter").value;
  try {
    let url = `/api/products?source=${encodeURIComponent(source)}`;
    const res = await fetch(url);
    const data = await res.json();
    const tbody = document.getElementById("tableBody");
    tbody.innerHTML = "";

    if (!data.products || data.products.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No products found.</td></tr>`;
      return;
    }

    data.products.forEach(p => {
      const storeClass = `store-${p.source.toLowerCase()}`;
      const img = p.image_url || "https://placehold.co/80x80/e2e8f0/1e293b?text=No+Image";
      const desc = p.description.length > 55 ? p.description.substring(0, 55) + "..." : p.description;

      const row = document.createElement("tr");
      row.innerHTML = `
        <td><img src="${img}" class="product-thumb" alt="Product" onerror="this.src='https://placehold.co/80x80?text=Item'" /></td>
        <td><span class="store-badge ${storeClass}">${p.source}</span></td>
        <td style="font-weight: 600; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${p.title}</td>
        <td style="font-family: var(--font-mono); font-weight: 700; color: #059669;">$${Number(p.price).toFixed(2)}</td>
        <td style="color: #F59E0B;">★ ${p.rating}</td>
        <td style="color: var(--text-muted); font-size: 0.8rem;">${desc}</td>
        <td>
          <a href="${p.product_url}" target="_blank" class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.75rem;">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Visit
          </a>
        </td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {
    showToast("Failed to populate product grid", "error");
  }
};

// 5. POLLING
let pollInterval = null;

const updateStatusUI = (statusData) => {
  const badge = document.getElementById("badgeStatus");
  const progressWrapper = document.getElementById("progressWrapper");
  const progressBar = document.getElementById("progressBar");
  const progressPct = document.getElementById("lblProgressPct");
  const progressMsg = document.getElementById("lblProgressMsg");
  const terminal = document.getElementById("terminalBody");

  badge.className = `badge badge-${statusData.status}`;
  badge.innerText = statusData.status.toUpperCase();

  terminal.innerHTML = "";
  statusData.logs.forEach(log => {
    const el = document.createElement("div");
    el.className = "log-entry";
    el.innerText = log;
    terminal.appendChild(el);
  });
  terminal.scrollTop = terminal.scrollHeight;

  if (statusData.status === "running") {
    progressWrapper.classList.remove("hidden");
    progressBar.style.width = `${statusData.progress}%`;
    progressPct.innerText = `${statusData.progress}%`;
  } else if (statusData.status === "completed") {
    progressBar.style.width = "100%";
    progressPct.innerText = "100%";
    clearInterval(pollInterval);
    pollInterval = null;
    showToast(`Scrape completed! ${statusData.total_records} items aggregated.`, "success");
    fetchAnalytics();
    fetchProducts();
    resetSearchButton();
  } else if (statusData.status === "failed") {
    clearInterval(pollInterval);
    pollInterval = null;
    showToast(`Failed: ${statusData.error_message}`, "error");
    resetSearchButton();
  }
};

const resetSearchButton = () => {
  const btn = document.getElementById("btnSearch");
  btn.disabled = false;
  btn.querySelector(".btn-text").innerHTML = '<i class="fa-solid fa-bolt"></i> Scrape All 3 Stores';
};

const startPolling = () => {
  if (pollInterval) clearInterval(pollInterval);
  pollInterval = setInterval(async () => {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      updateStatusUI(data);
    } catch (err) {
      console.error("Polling error:", err);
    }
  }, 1000);
};

// 6. INITIALIZATION
document.addEventListener("DOMContentLoaded", () => {
  init3DScene();
  fetchAnalytics();
  fetchProducts();

  document.getElementById("formSearch").addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = document.getElementById("inputQuery").value.trim();
    if (!query) return;

    const btn = document.getElementById("btnSearch");
    btn.disabled = true;
    btn.querySelector(".btn-text").innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Scraping...';
    document.getElementById("progressWrapper").classList.remove("hidden");

    try {
      const res = await fetch(`/api/search?query=${encodeURIComponent(query)}`, { method: "POST" });
      if (!res.ok) {
        const err = await res.json();
        showToast(err.detail || "Search request failed", "error");
        resetSearchButton();
        return;
      }
      showToast(`Searching Amazon, eBay & Alibaba for '${query}'...`, "info");
      startPolling();
    } catch (err) {
      showToast("Network error initiating search", "error");
      resetSearchButton();
    }
  });

  document.getElementById("selectSourceFilter").addEventListener("change", fetchProducts);

  document.getElementById("btnClearLogs").addEventListener("click", () => {
    document.getElementById("terminalBody").innerHTML = '<div class="log-entry">[CLEARED] Output stream cleared.</div>';
  });

  document.getElementById("btnExportCsv").addEventListener("click", () => {
    window.location.href = "/api/export/csv";
    showToast("Downloading CSV file...", "info");
  });

  document.getElementById("btnExportExcel").addEventListener("click", () => {
    window.location.href = "/api/export/excel";
    showToast("Downloading Excel spreadsheet...", "info");
  });
});