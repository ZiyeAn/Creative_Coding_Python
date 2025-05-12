let birthdays, festivals, crops;

Promise.all([
  fetch("../data/birthdays.json").then(res => res.json()),
  fetch("../data/festivals.json").then(res => res.json()),
  fetch("../data/crops.json").then(res => res.json())
]).then(([b, f, c]) => {
  birthdays = b;
  festivals = f;
  crops = c;
});

function getInfo() {
  const season = document.getElementById("season").value;
  let day = document.getElementById("day").value;
  day = String(day).padStart(2, '0');

  const output = document.getElementById("output");
  output.innerHTML = "";

  //  Festival
  const fest = festivals[season]?.find(e => e.date === day);
  if (fest) {
    output.innerHTML += `Festival Today: ${fest.name}\n\n`;
  } else {
    output.innerHTML += `No festival today. Take it easy.\n\n`;
  }

  //  Birthday
  const bday = birthdays[season]?.find(e => e.date === day);
  if (bday) {
    output.innerHTML += ` It's ${bday.name}'s birthday today!\n`;
    if (bday.loved_gifts?.length) {
      output.innerHTML += `Loved gifts: ${bday.loved_gifts.join(", ")}\n\n`;
    }
  } else {
    output.innerHTML += `Relax, it's nobody's birthday today. No presents needed!\n\n`;
  }

  // Plantable Crops
  const remaining = 28 - parseInt(day);
  const plantables = crops[season]?.filter(c => c.grow_days !== null && c.grow_days <= remaining);
  if (plantables?.length) {
    output.innerHTML += `You still have time to grow:\n`;
    plantables.forEach(crop => {
      output.innerHTML += `• ${crop.name} (${crop.grow_days} days)\n`;
    });
  }
}
// animation
const win = document.getElementById("window");
const header = document.getElementById("window-header");
let offsetX = 0, offsetY = 0, isDown = false;

header.addEventListener("mousedown", (e) => {
  isDown = true;
  offsetX = e.clientX - win.offsetLeft;
  offsetY = e.clientY - win.offsetTop;
});

document.addEventListener("mouseup", () => isDown = false);

document.addEventListener("mousemove", (e) => {
  if (!isDown) return;
  win.style.left = `${e.clientX - offsetX}px`;
  win.style.top = `${e.clientY - offsetY}px`;
});


// 可拖动图标
document.querySelectorAll(".app-icon").forEach(icon => {
  let iconOffsetX, iconOffsetY, dragging = false;

  icon.addEventListener("mousedown", (e) => {
    dragging = true;
    iconOffsetX = e.clientX - icon.offsetLeft;
    iconOffsetY = e.clientY - icon.offsetTop;
    icon.style.zIndex = 1000;
  });

  document.addEventListener("mouseup", () => dragging = false);

  document.addEventListener("mousemove", (e) => {
    if (!dragging) return;
    icon.style.left = `${e.clientX - iconOffsetX}px`;
    icon.style.top = `${e.clientY - iconOffsetY}px`;
  });
});