"""
Setup script to initialize dialect samples
"""
import os
import sys

# Add the project root to Python path so we can import from config
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now we can import from config
try:
    from config.settings import SAMPLES_DIR
except ImportError:
    # Fallback if config import fails
    SAMPLES_DIR = os.path.join(project_root, 'data', 'dialects', 'samples')

def main():
    print("🎭 Setting up dialect samples...")
    
    if not os.path.exists(SAMPLES_DIR):
        os.makedirs(SAMPLES_DIR)
        print(f"Created {SAMPLES_DIR}")
    
    # Count existing dialect files
    dialect_files = [f for f in os.listdir(SAMPLES_DIR) if f.endswith('.txt')]
    print(f"Found {len(dialect_files)} dialect samples:")
    
    for file in dialect_files:
        print(f"  - {file.replace('.txt', '').replace('_', ' ').title()}")
    
    print("✅ Dialect setup complete!")

if __name__ == "__main__":
    main()
