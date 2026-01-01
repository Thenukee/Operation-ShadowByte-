
# 🕵️‍♂️ Operation ShadowByte

> **A Custom OSINT & Digital Investigation Platform aimed at modernizing Law Enforcement Intelligence.**

[![.NET Core](https://img.shields.io/badge/Backend-ASP.NET%20Core-512BD4?style=flat&logo=dotnet)](https://dotnet.microsoft.com/)
[![Python](https://img.shields.io/badge/Intelligence-Python-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?style=flat&logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Overview

**ShadowByte** is an Open Source Intelligence (OSINT) platform developed to assist law enforcement agencies—specifically aimed at the **Criminal Investigation Department (CID) of Sri Lanka**—in automating the digital intelligence cycle.

In an era where digital footprints are vast and dispersed, ShadowByte moves beyond simple data collection. It serves as a central hub for **gathering, processing, and visualizing** suspect data, reducing investigation time and highlighting connections that might otherwise remain hidden.

## ✨ Key Features

* **🔄 Automated Intelligence Cycle:** Streamlines the process of collection, processing, and analysis of digital evidence.
* **🕸️ Network Visualization:** Integrates **Cytoscape** to generate interactive link analysis graphs, mapping relationships between suspects, devices, and online entities.
* **🔍 Advanced Scraping Modules:** specialized Python modules containerized in **Docker** to scrape and validate data from open web sources.
* **🔒 Secure Data Handling:** Built on **ASP.NET Core** to ensure high-performance API handling and secure evidence management.
* **⚡ Real-time Validation:** Client-side strategies to ensure data integrity during live investigations.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Core** | ![ASP.NET](https://img.shields.io/badge/-ASP.NET%20Core-512BD4?logo=dotnet&logoColor=white) | RESTful APIs, Business Logic, and Security. |
| **Data Engine** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Web Scraping, Automation Scripts, and Data Parsing. |
| **Containerization** | ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white) | Modular deployment of scraping microservices. |
| **Visualization** | **Cytoscape.js** | Graph theory and network visualization for suspect mapping. |
| **Database** | *[Insert DB here, e.g., MSSQL/PostgreSQL]* | Persistent storage for case files and logs. |

---

## 🚀 Getting Started

### Prerequisites
* [.NET SDK](https://dotnet.microsoft.com/download) (6.0 or later recommended)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Python](https://www.python.org/downloads/) (3.9+)
* Node.js (for frontend dependencies)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Thenukee/Operation-ShadowByte-.git](https://github.com/Thenukee/Operation-ShadowByte-.git)
    cd Operation-ShadowByte-
    ```

2.  **Backend Setup**
    Navigate to the solution folder and restore dependencies:
    ```bash
    cd Backend
    dotnet restore
    dotnet run
    ```

3.  **Python Modules Setup**
    Navigate to the intelligence modules:
    ```bash
    cd DataModules
    pip install -r requirements.txt
    ```

4.  **Running with Docker (Optional)**
    ```bash
    docker-compose up --build
    ```

---

## 📸 Screenshots
*<img width="1280" height="688" alt="image" src="https://github.com/user-attachments/assets/c9993630-dbb2-4294-89be-da36837c9c06" />
<img width="1280" height="688" alt="image" src="https://github.com/user-attachments/assets/0a4e5a5e-3740-4dd1-b750-403e26b7e5ec" />



---

## ⚠️ Disclaimer

**Educational & Research Purpose Only**

This tool was developed as an undergraduate research project to demonstrate the application of software engineering in digital forensics.
* The developers are not responsible for any misuse of this tool.
* Ensure you have proper authorization before gathering data on individuals or entities.
* This tool is intended to aid authorized investigations, not to facilitate cyberstalking or unauthorized surveillance.

---

## 👥 The Team

This project was built by a team of Computer Science undergraduates dedicated to Public Safety and Digital Forensics.

* **Lean Beef Patty** -  [LinkedIn](https://www.linkedin.com/in/thsnukw120708323/)
* **Hasindu Nimesh**  - [LinkedIn](https://www.linkedin.com/in/hasindu-nimesh-6457521b6/)
* **Dinuka Wikramasinghe** - [LinkedIn](https://www.linkedin.com/in/dinuka-wickramasinghe-70b111248/)
* **Wageesha Rajapaksha** - [LinkedIn](https://www.linkedin.com/in/wageesha-rajapaksha-300035266/)
* **Tharusha Bandara** - [LinkedIn](https://www.linkedin.com/in/tharusha-bhanuka-bandara-7299a9265/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
