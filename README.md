# IE598 - Perspective Projection & 3D Graphics

This repository contains assignments for IE598 (Computer Graphics) at UIUC, focusing on perspective projection, view frustums, and 3D visualization using PyGame and OpenGL.

## Project Overview

This project demonstrates fundamental computer graphics concepts:

- **Perspective Projection Matrix**: Implementation of the projection matrix that transforms 3D camera space coordinates to normalized device coordinates (NDC)
- **View Frustum Visualization**: Interactive visualization of the view frustum (truncated pyramid) and its transformation to the canonical view volume
- **Perspective Division**: Demonstration of how objects at different depths undergo perspective foreshortening
- **Field of View Analysis**: Study of how FOV affects perspective projection, with specific focus on Meta Quest 3's 110° FOV

## Contents

- **`ind_ass_2.py`**: Interactive PyGame + OpenGL application with three visualization modes:
  - Mode 0: First-person view through the custom projection matrix
  - Mode 1: External view showing the view frustum and virtual objects
  - Mode 2: NDC space visualization showing perspective-transformed objects

- **`do_not_commit/quest3_perspective_projection.ipynb`**: Jupyter notebook with detailed mathematical analysis and visualizations:
  - Frustum bounds calculation
  - Projection matrix construction
  - Step-by-step visualization of the transformation pipeline
  - Perspective division demonstrations
  - FOV analysis and discussion

## Features

### Interactive Controls (ind_ass_2.py)

- **SPACE**: Cycle through visualization modes
- **Mouse Drag**: Rotate camera (in modes 1 and 2)
- **Mouse Wheel**: Zoom in/out
- **ESC**: Exit application

### Key Implementations

1. **Custom Projection Matrix**: Hand-built 4×4 perspective projection matrix based on frustum parameters
2. **Multiple View Modes**: Toggle between first-person, external, and NDC space views
3. **Real-time Rendering**: Hardware-accelerated OpenGL rendering
4. **Visual Debugging**: Color-coded cubes at different depths (z = -2, -5, -10)

## Setup

### Prerequisites

- Anaconda or Miniconda
- Python 3.11+

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ie598
   ```

2. Create the conda environment:
   ```bash
   conda env create -f environment.yml
   ```

3. Activate the environment:
   ```bash
   conda activate IE598
   ```

## Usage

### Running the Interactive Application

```bash
python ind_ass_2.py
```

Press SPACE to cycle through visualization modes:
- **Mode 0**: View scene through custom projection (first-person perspective)
- **Mode 1**: External view showing frustum and objects in camera space
- **Mode 2**: View objects transformed to NDC space (inside canonical cube)

### Running the Jupyter Notebook

```bash
jupyter notebook do_not_commit/quest3_perspective_projection.ipynb
```

The notebook provides:
- Mathematical derivations
- Step-by-step visualizations
- Verification tests
- Detailed analysis of FOV effects

## Technical Details

### Projection Matrix

The projection matrix `P` is constructed from frustum parameters:

```
P = [ X   0   A   0  ]
    [ 0   Y   B   0  ]
    [ 0   0   C   D  ]
    [ 0   0  -1   0  ]

where:
  X = 2n/(r-l)
  Y = 2n/(t-b)
  A = (r+l)/(r-l)
  B = (t+b)/(t-b)
  C = -(f+n)/(f-n)
  D = -2fn/(f-n)
```

### Parameters

- **FOV**: 110° (Meta Quest 3 specification)
- **Near Plane**: 0.1 units
- **Far Plane**: 20.0 units
- **Aspect Ratio**: 1.0 (square viewport)
- **Window Size**: 800×800 pixels

### Virtual Objects

Three cubes placed at different depths:
- **Red Cube**: z = -2.0 (near)
- **Green Cube**: z = -5.0 (middle)
- **Blue Cube**: z = -10.0 (far)

## Key Concepts Demonstrated

1. **Frustum Calculation**: Computing frustum bounds from FOV and aspect ratio
2. **Projection Matrix Construction**: Building the transformation matrix manually
3. **Clip Space**: Understanding homogeneous coordinates before perspective division
4. **Perspective Division**: The w-divide step that creates foreshortening (w' = -z)
5. **NDC Space**: The canonical [-1, 1]³ cube after projection
6. **FOV Trade-offs**: Analysis of how field of view affects immersion, distortion, and performance

## Dependencies

Core dependencies (see `environment.yml` for complete list):
- **pygame**: Window management and event handling
- **PyOpenGL**: OpenGL bindings for Python
- **numpy**: Numerical computations and matrix operations
- **matplotlib**: Plotting and visualization
- **PyGLM**: GLM math library for Python
- **Pillow**: Image processing

## Project Structure

```
ie598/
├── ind_ass_2.py                    # Main interactive application
├── environment.yml                  # Conda environment specification
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
└── do_not_commit/
    └── quest3_perspective_projection.ipynb  # Analysis notebook
```

## Assignment Requirements

This project fulfills the following requirements:

1. ✅ Calculate frustum bounds from FOV parameters
2. ✅ Implement perspective projection matrix manually
3. ✅ Visualize view frustum and canonical volume
4. ✅ Demonstrate perspective division on virtual objects
5. ✅ Analyze FOV effects on AR/VR headsets

## Notes

- The `do_not_commit/` folder contains work-in-progress and experimental code
- The PyOpenGL GLUT visualization in the notebook may not work in all Jupyter environments
- For best results with the notebook, run cells sequentially
- The interactive application requires a display (won't work over SSH without X11 forwarding)

## References

- Computer Graphics: Principles and Practice (3rd Edition)
- OpenGL Programming Guide (Red Book)
- Meta Quest 3 Technical Specifications
- Real-Time Rendering (4th Edition)

## Author

**Het Patel**
NetID: hcp4
Course: IE598 - Computer Graphics
Institution: University of Illinois Urbana-Champaign

## License

This project is for educational purposes as part of coursework at UIUC.
