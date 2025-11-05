#!/bin/bash
echo "Setting up Visas Pro..."
pip install -r requirements.txt

# Create icon placeholder
touch static/icon.png  # Add your 16x16 PNG icon

# Initialize DB
python -c "
from core.memory_manager import MemoryManager
mm = MemoryManager()
print('Database initialized')
"

echo "Setup complete! Run: python app.py"