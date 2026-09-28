// Click-to-load YouTube players: the page shows a thumbnail and only loads
// YouTube's player when someone presses play, which keeps the page fast.
document.querySelectorAll(".yt").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var params = "autoplay=1&rel=0&playsinline=1";
    if (btn.dataset.start) params += "&start=" + btn.dataset.start;
    var frame = document.createElement("iframe");
    frame.src = "https://www.youtube-nocookie.com/embed/" + btn.dataset.id + "?" + params;
    frame.title = btn.getAttribute("aria-label") || "YouTube video";
    frame.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    frame.allowFullscreen = true;
    btn.replaceChildren(frame);
    btn.style.cursor = "default";
  }, { once: true });
});

document.getElementById("year").textContent = new Date().getFullYear();

// Show dates come from shows.json, so adding a show never means editing this page.
var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

function timeLabel(t) {
  if (!t) return "";
  var h = parseInt(t.slice(0, 2), 10), m = t.slice(3, 5);
  return ((h % 12) || 12) + (m === "00" ? "" : ":" + m) + (h < 12 ? " AM" : " PM");
}

function todayISO() {
  var d = new Date();
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}

fetch("shows.json", { cache: "no-cache" })
  .then(function (r) { return r.json(); })
  .then(function (data) {
    var list = document.getElementById("show-list");
    var shows = (data.shows || [])
      .filter(function (s) { return s.date >= todayISO(); })
      .sort(function (a, b) { return (a.date + (a.time || "")).localeCompare(b.date + (b.time || "")); });

    if (!shows.length) {
      list.innerHTML = '<p class="no-shows">New dates are on the way. Follow Chris below to hear first.</p>';
      return;
    }

    list.innerHTML = shows.map(function (s) {
      var d = new Date(s.date + "T12:00:00");
      var where = [s.venue, s.address].filter(Boolean).join(", ");
      return '<article class="show">' +
        '<div class="show-when"><span class="big">' + MONTHS[d.getMonth()] + " " + d.getDate() + '</span>' +
        '<span class="small">' + DAYS[d.getDay()] + (s.time ? " · " + timeLabel(s.time) : "") + "</span></div>" +
        '<div class="show-info"><h3>' + esc(s.title) + "</h3>" +
        "<p>" + esc(where) + (s.city ? " · " + esc(s.city) : "") + "</p>" +
        (s.doors || s.presenter ? "<p>" + [s.doors ? "Doors " + timeLabel(s.doors) : "", s.presenter ? "Presented by " + esc(s.presenter) : ""].filter(Boolean).join(" · ") + "</p>" : "") +
        '<p class="sponsor-tag">Sponsored by <a href="https://www.belleeah.com" target="_blank" rel="noopener">Belleeah\'s Apples &amp; Treats</a></p></div>' +
        '<div class="show-cta">' + (s.tickets ? '<a class="btn solid" href="' + esc(s.tickets) + '" target="_blank" rel="noopener">Get Tickets</a>' : "") + "</div>" +
        "</article>";
    }).join("");

    // Event markup so search engines can list the dates directly in results.
    var events = shows.map(function (s) {
      var ev = {
        "@context": "https://schema.org",
        "@type": "ComedyEvent",
        "name": s.title,
        "startDate": s.date + (s.time ? "T" + s.time + (s.utc_offset || "") : ""),
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": { "@type": "Place", "name": s.venue, "address": [s.address, s.city].filter(Boolean).join(", ") },
        "performer": { "@type": "Person", "name": "Chris Longoria" },
        "organizer": s.presenter ? { "@type": "Organization", "name": s.presenter } : undefined,
        "doorTime": s.doors ? s.date + "T" + s.doors + (s.utc_offset || "") : undefined,
        "sponsor": { "@type": "Organization", "name": "Belleeah's Apples & Treats", "url": "https://www.belleeah.com" }
      };
      if (s.tickets) ev.offers = { "@type": "Offer", "url": s.tickets, "availability": "https://schema.org/InStock" };
      return ev;
    });
    var tag = document.createElement("script");
    tag.type = "application/ld+json";
    tag.textContent = JSON.stringify(events);
    document.head.appendChild(tag);
  })
  .catch(function () {
    document.getElementById("show-list").innerHTML = '<p class="no-shows">Show dates are posted on Chris\'s Instagram.</p>';
  });
