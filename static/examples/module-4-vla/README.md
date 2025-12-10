# Module 4: VLA Examples

This directory contains downloadable code examples for Module 4: Vision-Language-Action Models.

## Contents

- `whisper_commands.py` - Voice command processing with Whisper
- `vla_inference.py` - VLA model inference example
- `embodied_agent.py` - End-to-end embodied agent pipeline

## Prerequisites

- Python 3.10+
- PyTorch 2.0+
- transformers library
- OpenAI Whisper
- CUDA-capable GPU (recommended)

## Usage

```bash
# Install dependencies
pip install torch transformers openai-whisper

# Run voice command processing
python whisper_commands.py --audio recording.wav

# Run VLA inference
python vla_inference.py --image scene.jpg --instruction "pick up the red cube"
```

## Notes

VLA models require significant GPU memory. Recommended: NVIDIA GPU with 16GB+ VRAM.
