"""
Dialect sample loader for EchoLens
"""
import os
from typing import Dict

def load_dialect_samples() -> Dict[str, str]:
    """Load dialect samples from files"""
    samples = {}
    samples_dir = os.path.join('data', 'dialects', 'samples')
    
    if os.path.exists(samples_dir):
        for filename in os.listdir(samples_dir):
            if filename.endswith('.txt'):
                # Just use filename without extension as the dialect name
                dialect_name = filename.replace('.txt', '').replace('_', ' ').title()
                
                try:
                    with open(os.path.join(samples_dir, filename), 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:  # Only add non-empty files
                            samples[dialect_name] = content
                        else:
                            print(f"Warning: {filename} is empty")
                except Exception as e:
                    print(f"Warning: Could not load {filename}: {e}")
    
    # Fallback samples only if no files were loaded successfully
    if not samples:
        print("Warning: No dialect samples found in files, using fallback samples")
        samples = {
            "Academic Scholar": "The theoretical framework employs post-structuralist discourse analysis to examine the underlying assumptions embedded within these linguistic patterns.",
            "Startup Techie": "We're building something truly transformative here. This could fundamentally reshape how people think about this space.",
            "Crossfit Bro": "I'm absolutely crushing my goals right now. Hit a new PR yesterday and my nutrition is completely dialed in."
        }
    
    return samples
