let currentLevel = 1;
let currentName = ""; // Store customer name for restarting the trip
let updateInterval = null;
let lastMeta = null; // store latest meta to show it on finish screen only

/*
|--------------------------------------------------------------------------
| Fare level selection
|--------------------------------------------------------------------------
| Updates current fare level and highlights selected button
*/
function selectLevel(level) {
    currentLevel = level;
    document.querySelectorAll('.lvl-btn')
        .forEach(btn => btn.classList.remove('selected'));
    document.querySelectorAll('.lvl-btn')[level - 1]
        .classList.add('selected');
}

/*
|--------------------------------------------------------------------------
| Start trip
|--------------------------------------------------------------------------
| Validates input name and initiates a new trip
*/
async function startTrip() {
    const nameInput = document.getElementById('inputName').value;
    if (!nameInput) {
        alert("Please enter name");
        return;
    }

    currentName = nameInput;
    await _initiateTrip(currentName, currentLevel);
}

/*
|--------------------------------------------------------------------------
| Restart trip with the same user
|--------------------------------------------------------------------------
| Uses stored name and resets fare level
*/
async function restartSameUser() {
    currentLevel = 1;
    selectLevel(1);
    await _initiateTrip(currentName, currentLevel);
}

/*
|--------------------------------------------------------------------------
| Internal trip initializer
|--------------------------------------------------------------------------
| Sends start request to server and resets UI state
*/
async function _initiateTrip(name, level) {
    // API call to start trip
    await fetch('/api/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, level: level })
    });

    // Reset UI for trip screen
    switchScreen('screen-trip');
    document.getElementById('displayCustomer').innerText = name;
    document.getElementById('btnAction').innerText = "STOP";
    document.getElementById('displayFare').innerText = "0.00";
    document.querySelectorAll('.opt-btn')
        .forEach(b => b.classList.remove('active'));

    // Start periodic update loop
    startUpdateLoop(2000);
}

/*
|--------------------------------------------------------------------------
| Periodic update loop
|--------------------------------------------------------------------------
| Fetches trip status at a fixed interval
*/
function startUpdateLoop(intervalTime) {
    if (updateInterval) clearInterval(updateInterval);

    // Initial fetch to sync UI immediately
    fetchData();

    updateInterval = setInterval(fetchData, intervalTime);
}

/*
|--------------------------------------------------------------------------
| Fetch live trip data
|--------------------------------------------------------------------------
| Updates fare, logs, state button, and meta info
*/
async function fetchData() {
    try {
        const res = await fetch('/api/update');
        const data = await res.json();

        // Update fare display
        document.getElementById('displayFare')
            .innerText = data.fare.toFixed(2);

        // Update log list
        const logContainer = document.getElementById('logList');
        logContainer.innerHTML = '';
        data.logs.forEach(log => {
            const div = document.createElement('div');
            div.className = 'log-item';
            div.innerHTML = `<span>${log.time}</span><span>${log.msg}</span>`;
            logContainer.appendChild(div);
        });

        // Sync action button with current state
        const actionBtn = document.getElementById('btnAction');
        actionBtn.innerText = (data.state === '1') ? "STOP" : "MOVE";

        // Store meta for the finish screen (do NOT render on trip screen)
        if (data.meta) {
            lastMeta = data.meta;
        }

    } catch (e) {
        console.error("Update error:", e);
    }
}

/*
|--------------------------------------------------------------------------
| Toggle taxi state (MOVE / STOP)
|--------------------------------------------------------------------------
*/
async function toggleState() {
    await fetch('/api/toggle_state', { method: 'POST' });
    fetchData(); // Immediate refresh for responsiveness
}

/*
|--------------------------------------------------------------------------
| Toggle surcharge options (city / night)
|--------------------------------------------------------------------------
*/
async function toggleOption(type) {
    const btn = (type === 'city')
        ? document.getElementById('btnOptCity')
        : document.getElementById('btnOptNight');

    const willBeActive = !btn.classList.contains('active');
    btn.classList.toggle('active', willBeActive);

    await fetch('/api/toggle_option', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ option: type, active: willBeActive })
    });

    fetchData(); // Refresh after option change
}

/*
|--------------------------------------------------------------------------
| Finish trip
|--------------------------------------------------------------------------
| Stops update loop and shows final fare screen
*/
async function finishTrip() {
    clearInterval(updateInterval);

    const res = await fetch('/api/stop', { method: 'POST' });
    const data = await res.json();

    document.getElementById('finishCustomer').innerText = currentName;
    document.getElementById('finishFare').innerText = data.fare.toFixed(2);

    // show level/options ONLY here
    renderFinishMeta(lastMeta);

    switchScreen('screen-finish');
}

/*
|--------------------------------------------------------------------------
| Reset application
|--------------------------------------------------------------------------
*/
function resetApp() {
    location.reload();
}

/*
|--------------------------------------------------------------------------
| Trip history modal
|--------------------------------------------------------------------------
*/
async function showHistory() {
    document.getElementById('screen-history').style.display = 'block';

    const res = await fetch('/api/history');
    const list = await res.json();

    const tbody = document.querySelector('#historyTable tbody');
    tbody.innerHTML = '';

    list.forEach(item => {
        tbody.innerHTML += `
            <tr>
                <td>${item.date}</td>
                <td>${item.name}</td>
                <td>€ ${item.fare}</td>
            </tr>
        `;
    });
}

function closeHistory() {
    document.getElementById('screen-history').style.display = 'none';
}

/*
|--------------------------------------------------------------------------
| Screen navigation helper
|--------------------------------------------------------------------------
*/
function switchScreen(id) {
    document.querySelectorAll('.screen')
        .forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function renderFinishMeta(meta) {
  if (!meta) return;

  document.getElementById('finishInfoLevel').innerText = meta.level;
  document.getElementById('finishInfoMove').innerText = meta.move_rate.toFixed(3);
  document.getElementById('finishInfoStop').innerText = meta.stop_rate.toFixed(3);

  const optContainer = document.getElementById('finishInfoOptions');
  optContainer.innerHTML =
    (meta.active_options && meta.active_options.length > 0)
      ? meta.active_options.join('<br>')
      : "<small>-</small>";
}