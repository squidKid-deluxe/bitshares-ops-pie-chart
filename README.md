# BitShares Operations Pie Chart

This project generates a video visualization of BitShares operations over time, represented as pie charts. The video shows weekly and cumulative operation distributions, making it easy to visualize trends and changes.

<video controls>
  <source src="out.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.6 or higher
- pip (Python package installer)
- OpenCV
- NumPy

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/squidKid-deluxe/bitshares-ops-pie-chart.git
   cd bitshares-ops-pie-chart
   ```

2. Install the required Python packages:

   ```bash
   pip install numpy opencv-python
   ```

3. if you wish, update the CSV file `weekly bitshares ops count.csv` in the project directory. See `Screencast - Kibana Lens.webm` for help on how to make one.

## Usage

To generate the video visualization, run the `main.py` script:

```bash
python main.py
```

The script will read the CSV data, process it, and generate a video file named `out.mp4` showing the weekly and cumulative operation distributions.

## Project Structure

- `main.py`: The main script that processes the CSV data and generates the video.
- `ops.py`: Contains the list of BitShares operations.
- `pie_chart.py`: Contains functions to create pie charts and draw legends.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
