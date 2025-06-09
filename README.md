# Python 3D Render Engine | Built from Scratch 🐍🎮

This is a **software-rendered 3D engine** built entirely from scratch using **Python** and **Pygame** — without any external 3D or graphics libraries. It features real-time rendering, camera controls, object loading, lighting, shading, and more.

Inspired by the fundamentals of graphics programming, this project includes a full implementation of a basic 3D pipeline including projection, backface culling, frustum clipping, and more.

---

## 🚀 Features

* 🧱 **OBJ Mesh Loading** (e.g., mountains.obj, Utah teapot, etc.)
* 🧯 **Real-Time Camera Navigation** (free-look movement with WASD + mouse)
* 💡 **Software Lighting** with dynamic shading based on surface normals 
* ✂️ **Triangle Clipping** against view and screen bounds
* 🧵 **Wireframe Rendering Mode** toggle
* 🎮 **Adjustable Line Thickness** for wireframe view
* 🔄 **Custom Matrix Transformations** (projection, rotation, scaling)
* 🖱️ **Mouse-Look Support** for FPS-style navigation
* 🎮 **Backface Culling** for performance optimization
* ⚙️ **Z-Sorting** for proper triangle render ordering

---

## 📸 Demo Preview


*A classic Utah Teapot — half flat shaded, half wireframe.*

---

## 🛠️ Requirements

* Python 3.8+
* pygame-ce (Pygame Community Edition)

### ✅ Install dependencies

```bash
pip install pygame-ce
```

---

## 🧑‍💻 How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/Dheer20/3D_Engine.git
   cd 3D_Engine
   ```

2. Make sure you have an `.obj` file to load (default: `objects/mountains.obj` or use a teapot model).

3. Run the engine:

   ```bash
   python D_Engine.py
   ```

---

## 🎮 Controls

| Key / Mouse           | Action                                  |
| --------------------- | --------------------------------------- |
| `W` / `S`             | Move forward / backward                 |
| `A` / `D`             | Strafe left / right                     |
| `Arrow Keys`          | Pan camera (left, right, up, down)      |
| `SPACE` / `SHIFT`     | Move camera up / down                   |
| `Mouse Movement`      | Look around (FPS-style camera rotation) |
| `TAB`                 | Toggle wireframe mode                   |
| `J` / `K` (Wireframe) | Decrease / Increase line thickness      |
| `HOME`                | Reset camera position                   |
| `ESC`                 | Exit the engine                         |

---

## 🧐 How It Works

* Custom-built `Vector`, `Triangle`, and `Matrix` math classes
* Object space → World space → View space → Projection → Screen space
* Dynamic lighting using dot product with surface normals
* Frustum and screen clipping using plane equations
* Backface culling and triangle Z-sorting for correct rendering

---

## 📂 Folder Structure

```
3D_Engine/
│
├── D_Engine.py           # Main render engine loop
├── Geometry.py           # All 3D math logic (Vectors, Matrices, etc.)
├── objects/
│   └── mountains.obj     # Sample 3D mesh (can replace with your own)
└── README.md             # You're reading it!
```

---

## ⭐ Star the Repo

If you find this project interesting or helpful, feel free to **star** the repository and share it!
[GitHub Repo → Dheer20/3D\_Engine](https://github.com/Dheer20/3D_Engine)

---

## 🔧 Upcoming Improvements

* Texture mapping support
* FPS counter & stats overlay
* GUI toggle for render modes
* Improved object loading performance
* Collisions & bounding boxes

---

## 📢 Contact

Feel free to reach out for collaboration, feedback, or ideas:

**LinkedIn**: [linkedin.com/in/dheerparekh](https://www.linkedin.com/in/dheerparekh)

**Email**: [dheerparekh.2004@gmail.com](mailto:dheerparekh.2004@gmail.com)

---
