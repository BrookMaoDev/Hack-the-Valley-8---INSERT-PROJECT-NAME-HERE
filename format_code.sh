#!/bin/bash

# Run black for Python files
echo "Formatting Python files with black..."
find . -name "*.py" -exec python -m black {} +

# Run prettier for other files
echo "Formatting other files with prettier..."
find . ! -name "*.py" ! -name "malaria_cell_classification_tensorflow.ipynb" -exec prettier --write {} +
