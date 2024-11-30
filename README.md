<a id="readme-top"></a>
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="adopt-a-pet/static/images/logo.png" alt="Logo" width="350" height="80">
  </a>
  <p align="center"><i>This project, adopt-a-pet, is a Django-based web application that simplifies the process of adopting pets from shelters. It is developed as     part of our Information Management 2 capstone.</i></p>
  <a href="https://github.com/eynabdllh/pet-adoption-system/stargazers"><img src="https://img.shields.io/github/stars/eynabdllh/pet-adoption-system" alt="Stars Badge"/></a>
<a href="https://github.com/eynabdllh/pet-adoption-system/network/members"><img src="https://img.shields.io/github/forks/eynabdllh/pet-adoption-system" alt="Forks Badge"/></a>
<a href="https://github.com/eynabdllh/pet-adoption-system/pulls"><img src="https://img.shields.io/github/issues-pr/eynabdllh/pet-adoption-system" alt="Pull Requests Badge"/></a>
<a href="https://github.com/eynabdllh/pet-adoption-system/issues"><img src="https://img.shields.io/github/issues/eynabdllh/pet-adoption-system" alt="Issues Badge"/></a>
<a href=https://github.com/eynabdllh/pet-adoption-system/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/eynabdllh/pet-adoption-system?color=2b9348"></a>
<a href="https://github.com/eynabdllh/pet-adoption-system/blob/master/LICENSE"><img src="https://img.shields.io/github/license/eynabdllh/pet-adoption-system?color=2b9348" alt="License Badge"/></a>
</div>
<br>

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [ERD](#erd-entity-relationship-diagram)
- [UI/UX](#uiux-design)
- [Gantt Chart](#gantt-chart)
- [Developers](#developers)
- [Top Contributors](#top-contributors)
- [License](#license)

---

## Introduction

[![Landing-Page](https://github.com/eynabdllh/pet-adoption-system/raw/main/adopt-a-pet/static/images/adopt-a-pet.png)](https://github.com/eynabdllh/pet-adoption-system)

adopt-a-pet is a web application designed to make the pet adoption process easier for both animal shelters and adopters. It helps users browse pets, submit adoption requests, schedule pick-ups, and receive notifications, while shelter admins can manage pet listings and oversee the adoption process. This project aims to develop a streamlined and efficient pet adoption system to improve the adoption experience for both shelters and potential adopters.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Features
1. **User Registration and Authentication:** Users can create accounts and log in securely.
2. **Profile Management:** Users can update personal details and view their adoption history.
3. **Pet Listing:** A detailed listing of all available pets, with information about breed, age, and status.
4. **Adoption Request:** Users can submit requests to adopt pets of their choice.
5. **Pick-Up Scheduling:** Users can schedule a pick-up date for adopted pets.
6. **Notifications:** Receive updates on adoption status, new pet listings, and scheduled visits.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Built With
<section id="technologies">
  <a href="https://www.djangoproject.com/" target="_blank">
    <img src="https://img.shields.io/badge/Django-blue?style=for-the-badge&logo=django" alt="Django" />
  </a>
  <a href="https://getbootstrap.com" target="_blank">
    <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
  </a>
  <a href="https://www.w3.org/Style/CSS/" target="_blank">
    <img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS" />
  </a>
  <a href="https://html.spec.whatwg.org/multipage/" target="_blank">
      <img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML" />
  </a>
  <a href="https://www.javascript.com/" target="_blank">
      <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="Javascript" />
  </a>
</section>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

Follow these steps to set up the project locally and start using it efficiently.

### Prerequisites

Below are the required tools and steps to install them for running the software.
#### 1. Install Python
Install ```python-3.12.5```. Follow the steps from the below reference document based on your Operating System.
Reference: [https://docs.python-guide.org/starting/installation/](https://docs.python-guide.org/starting/installation/) 

#### 2. Clone the repo
   ```sh
   git clone https://github.com/eynabdllh/pet-adoption-system.git
   ```

#### 3. Navigate to the project directory
 ```sh
   cd adopt-a-pet
   ```

#### 4. Setup virtual environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv/scripts/Activate #For macOS/Linux 'source venv/bin/activate'

```

#### 5. Installation

1. Install dependencies
   ```sh
   pip install openpyxl
   pip install pillow
   ```
2. Install Requirements
   ```sh
   pip install -r requirements.txt
   ```
3. Migrate database
    ```sh
   py manage.py makemigrations
   py manage.py migrate
   ```
4. Run the server
   ```sh
    py manage.py runserver
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Gantt Chart

The timeline for the development of this project is available in the Gantt Chart below:

[Gantt Chart](https://docs.google.com/spreadsheets/d/1xkvWZaWizDLPvSHAJ-dwQYHgKrJD6Z7OzchyzyKRr8s/edit?usp=sharing)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
## ERD (Entity Relationship Diagram)

The following ERD outlines the relationships between entities in the system, such as users, pets, and adoption requests:

[ERD Diagram](https://drive.google.com/file/d/1hNGwf2DInYBS6GWfPdmwFCWZkkdSKpuF/view?usp=sharing)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## UI/UX Design

The design and layout of the user interface can be explored via the Figma link below:

[UI/UX Design](https://www.figma.com/design/QkxAZ7so69q8vqw4oeFkwE/Adopt-a-Pet?node-id=0-1&t=AOHbSggJNBGv0g9K-1)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
## Developers
<div>
  <table>
    <tr>
      <th>Developers</th>
      <th>Assigned Apps</th>
    </tr>
    <tr>
      <td align="center">
        <strong>Anamerah M. Abdullah</strong><br>
        <a href="https://github.com/eynabdllh"><img src="https://img.shields.io/badge/GitHub-Profile-blueviolet?style=for-the-badge&logo=github&logoColor=white" alt="Anamerah's GitHub"></a>
      </td>
      <td>
        <p>Dashboard, Pet Listing/Management, Profile Management</p>
      </td>
    </tr>
    <tr>
      <td align="center">
        <strong>Chrizza Arnie T. Gales</strong><br>
        <a href="https://github.com/Chrizmas20"><img src="https://img.shields.io/badge/GitHub-Profile-blueviolet?style=for-the-badge&logo=github&logoColor=white" alt="Chrizza's GitHub"></a>
      </td>
      <td>
        <p>Adoption Request/Management, Schedule List/Management</p>
      </td>
    </tr>
    <tr>
      <td align="center">
        <strong>Jan Raye Edbert L. Dutosme</strong><br>
        <a href="https://github.com/MrCareerBully"><img src="https://img.shields.io/badge/GitHub-Profile-blueviolet?style=for-the-badge&logo=github&logoColor=white" alt="Jan Raye's GitHub"></a>
      </td>
      <td>
        <p>Login/Register, Notification</p>
      </td>
    </tr>
  </table>
</div>

---
## Top Contributors
<a href="https://github.com/eynabdllh/pet-adoption-system/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=eynabdllh/pet-adoption-system" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## License
This project is open-source and licensed under the MIT License.  See `LICENSE.txt` for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>
