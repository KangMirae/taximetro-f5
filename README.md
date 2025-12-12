# Digital Taximeter

> A modernized digital taximeter system built with Python and Flask.
> Designed with a mobile-first approach to simulate real-world usage by taxi drivers.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3)

## 📖 About The Project

This project is a **Digital Taximeter** prototype developed as part of a Python Bootcamp project. The goal was to evolve a simple CLI program into a robust, Object-Oriented application with a web-based graphical user interface (GUI).

It simulates the fare calculation logic used in real taxis, considering:
- **State-based Pricing**: Different rates for "Moving" vs "Stopped".
- **Rate Levels**: Adjustable pricing levels (1-4) based on demand.
- **Surcharges**: Options for Night shifts or Out-of-City trips.
- **Real-time Updates**: Live fare calculation displayed on a mobile-friendly interface.

---

## ✨ Key Features

*   **📱 Mobile-First UI**: A responsive web interface that looks and feels like a native mobile app.
*   **⚙️ Dynamic Configuration**: Rates, multipliers, and levels are configurable via `data/rates.json`.
*   **🔄 Real-time Calculation**: Fares update automatically every 5 seconds (simulated) or instantly upon interaction.
*   **💾 Persistent History**: Automatically saves completed trips to `data/trip_history.json`.
*   **🛠 OOP Architecture**: Clean separation of concerns using `Taximeter` class (Logic), `HistoryManager` (Storage), and Flask (Presentation).
*   **🌓 Smart Surcharges**: Toggleable options for "Night" and "City" rates with visual feedback.
*   **🔁 Quick Restart**: Ability to start a new trip immediately with the same passenger details.

---

## 🏗 Project Structure

```text
├── data/
│   ├── rates.json        # Configuration for pricing & rates
│   ├── trip_history.json # Database of past trips
│   └── taximetro.log     # Application logs
├── src/
│   ├── taximeter.py      # Core business logic (OOP)
│   ├── storage.py        # JSON file handling
│   └── config.py         # Configuration loader
├── static/
│   ├── style.css         # Modern, mobile-optimized styling
│   └── script.js         # Frontend logic & API communication
├── templates/
│   └── index.html        # Single Page Application (SPA) structure
├── app.py                # Flask entry point
├── main.py               # (Legacy) CLI version
└── requirements.txt      # Python dependencies
```

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites
*   Python 3.x installed
*   Git installed

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Bootcamp-IA-P6/Proyecto1_Mirae_Kang.git
    cd Proyecto1_Mirae_Kang
    ```

2.  **Create a virtual environment (Optional but recommended)**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install flask
    ```

4.  **Run the application**
    ```bash
    python app.py
    ```

5.  **Access the App**
    *   Open your browser and go to: `http://127.0.0.1:5000`
    *   (Tip: Open DevTools `F12` and toggle "Device Toolbar" to see the mobile view!)

---

## ⚙️ Configuration (`rates.json`)

You can modify the pricing logic without changing the code by editing `data/rates.json`:

```json
{
    "base_rates": {
        "1": 0.05,  // Rate per second when moving
        "2": 0.02   // Rate per second when stopped
    },
    "levels": {
        "1": 1.0,   // Multiplier for Level 1
        "2": 1.2    // Multiplier for Level 2
        ...
    },
    "options": {
        "night": { "name": "Night", "multiplier": 1.2 }
    }
}
```

---

## 👩‍💻 Author

*   **Mirae Kang** - *Development & Refactoring*

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
