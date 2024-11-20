# **Ball Bouncer Game**

A simple and interactive arcade game where a ball bounces within a circular boundary, with realistic gravity and collision physics. The player can observe the ball's interaction with a rotating boundary arc, offering a fun way to experience physics-based gameplay.

![Game Screenshot](docs/images/game_screenshot.png)

---

## **Table of Contents**
- [**Ball Bouncer Game**](#ball-bouncer-game)
  - [**Table of Contents**](#table-of-contents)
  - [**Features**](#features)
  - [**Installation**](#installation)
    - [**1. Clone the Repository**](#1-clone-the-repository)
    - [**2. Set Up a Virtual Environment**](#2-set-up-a-virtual-environment)
    - [**3. Install Dependencies**](#3-install-dependencies)
  - [**Usage**](#usage)
  - [**Project Structure**](#project-structure)

---

## **Features**
- **Physics-based gameplay**: The ball bounces with gravity, elasticity, and collision detection.
- **Rotating boundary**: A circular arc boundary rotates, creating dynamic gameplay.
- **Customizable settings**: Adjust ball speed, gravity, and boundary rotation speed.

---

## **Installation**
Follow these steps to set up and run the project:

### **1. Clone the Repository**
```bash
git clone https://github.com/thisisaqib/ball_bouncer.git
cd ball_bouncer
```

### **2. Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

## **Usage**
To run the game:

```bash
python src/main.py
```

When running, you will see:

- A ball bouncing within a rotating boundary.
- Collision sounds when the ball interacts with certain regions.

## **Project Structure**
```bash
ball_bouncer/
├── src/
│   ├── ball_bouncer/      # Main application package
│   │   ├── __init__.py    # Package-level initialization
│   │   ├── config.py      # Configuration constants
│   │   ├── ball.py        # Ball logic
│   │   ├── boundary.py    # Boundary logic
│   │   └── game.py        # Game entry point
│   └── __init__.py        # Ensures `src` is treated as a package
├── docs/
│   ├── images/            # Images for documentation (e.g., screenshots)
├── assets/                # Game assets (sounds, images, etc.)
├── requirements.txt       # List of dependencies
├── pyproject.toml         # Project metadata and build configuration
├── .gitignore             # Files to ignore in source control
├── README.md              # Project overview and documentation
└── LICENSE                # License file for open-source projects
```

