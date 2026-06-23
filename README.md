# Network Operations Center (NOC) Dashboard

A modern, responsive, and dynamic Network Operations Center (NOC) Dashboard built with Django and customized front-end styling. This project is designed to provide real-time monitoring and analytics for network sensors, devices, and server health.

## 🚀 Features

### 1. Unified Network Dashboard
A central hub providing a high-level overview of network health across multiple departments and sites.

- Department Health Gauges : 
Visual radial charts that instantly display the availability percentage of different departments, helping identify infrastructure bottlenecks at a glance.

- Live Sensor Analytics : 
Track the status (Online/Down) and latency (ms) of various network components including Gateways, Switches, Access Points, Firewalls, and Ping sensors.

*![Dashboard Overview](readmeImages/Dashboard1.png)*
*![Dashboard Overview](readmeImages/Dashboard2.png)*


Ye numbering thik kar do
### 2. Interactive Latency Graphs
Click on any active sensor to reveal a detailed, smooth area chart (powered by ApexCharts) tracking its latency history.

*![Latency Graph](readmeImages/Graphs.png)*

### 3. Advanced IP & Sensor Configuration
A dedicated "Add IP" interface allowing administrators to connect new PRTG servers, securely provide credentials, and selectively fetch and bind sensors to specific sites.

*![Add IP Configuration](readmeImages/Addip.png)*

### 4. Seamless Dark/Light Mode
A fully customized, premium UI that supports flawless switching between dark and light themes, ensuring high contrast and visual comfort in any environment.

## 🛠️ Technology Stack
- **Backend:** Python, Django
- **Frontend:** HTML5, Vanilla CSS, JavaScript
- **Styling/Components:** Bootstrap, Sneat Core, FontAwesome
- **Data Visualization:** ApexCharts
- **Date/Time Picking:** Flatpickr

## ⚙️ Setup & Installation

1. Clone the repository to your local machine.
2. Ensure you have Python installed.
3. Install dependencies using your package manager (e.g., `pip install -r requirements.txt`).
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`
6. Access the dashboard via `http://localhost:8000/`

