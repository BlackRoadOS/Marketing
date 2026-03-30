#!/usr/bin/env python3
"""
BlackRoad OS — Local Image Generator
Runs Stable Diffusion on Apple Silicon (Metal/MPS).

Usage:
    python3 generate.py "a glowing highway at night"
    python3 generate.py "a glowing highway at night" --output hero.png
    python3 generate.py "a glowing highway at night" --size 1080x1080
    python3 generate.py "a glowing highway at night" --size 1080x1920  # vertical/TikTok
    python3 generate.py "a glowing highway at night" --steps 8 --count 4
    python3 generate.py --batch prompts.txt  # One prompt per line, generates all

Models (auto-downloads on first use, cached at ~/.cache/huggingface/):
    --model turbo    SDXL Turbo — fast (~5s), good quality (default)
    --model lightning SDXL Lightning — fast (~5s), different style
    --model sdxl     SDXL 1.0 — slower (~30s), highest quality
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Default output directory
OUTPUT_DIR = Path.home() / "Marketing" / "assets" / "generated"


def load_pipeline(model_name="turbo"):
    """Load the appropriate Stable Diffusion pipeline."""
    import torch
    from diffusers import AutoPipelineForText2Image, StableDiffusionXLPipeline

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float16 if device == "mps" else torch.float32

    models = {
        "turbo": "stabilityai/sdxl-turbo",
        "lightning": "ByteDance/SDXL-Lightning",
        "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
    }

    model_id = models.get(model_name, models["turbo"])
    print(f"Loading {model_name} ({model_id})...")
    print(f"Device: {device} | Dtype: {dtype}")

    if model_name == "turbo":
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_id,
            torch_dtype=dtype,
            variant="fp16",
        )
        pipe = pipe.to(device)
        return pipe, {"guidance_scale": 0.0, "num_inference_steps": 4}

    elif model_name == "lightning":
        from diffusers import EulerDiscreteScheduler
        from huggingface_hub import hf_hub_download

        base = "stabilityai/stable-diffusion-xl-base-1.0"
        pipe = StableDiffusionXLPipeline.from_pretrained(
            base, torch_dtype=dtype, variant="fp16"
        ).to(device)
        pipe.scheduler = EulerDiscreteScheduler.from_config(
            pipe.scheduler.config, timestep_spacing="trailing"
        )
        repo = "ByteDance/SDXL-Lightning"
        ckpt = "sdxl_lightning_4step_unet.safetensors"
        pipe.unet.load_state_dict(
            __import__("safetensors.torch", fromlist=["load_file"]).load_file(
                hf_hub_download(repo, ckpt), device=str(device)
            )
        )
        return pipe, {"guidance_scale": 0.0, "num_inference_steps": 4}

    else:  # sdxl
        pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id, torch_dtype=dtype, variant="fp16",
        ).to(device)
        return pipe, {"guidance_scale": 7.5, "num_inference_steps": 30}


def generate(pipe, prompt, defaults, width=1024, height=1024, steps=None, seed=None):
    """Generate a single image."""
    import torch

    params = {**defaults}
    if steps:
        params["num_inference_steps"] = steps

    generator = None
    if seed is not None:
        generator = torch.Generator("mps" if torch.backends.mps.is_available() else "cpu")
        generator.manual_seed(seed)

    # BlackRoad brand negative prompt
    negative = "text, watermark, logo, blurry, low quality, distorted, ugly, deformed"

    result = pipe(
        prompt=prompt,
        negative_prompt=negative,
        width=width,
        height=height,
        generator=generator,
        **params,
    )
    return result.images[0]


def parse_size(size_str):
    """Parse WxH string."""
    parts = size_str.lower().split("x")
    w, h = int(parts[0]), int(parts[1])
    # Round to nearest 8 (required by SD)
    return (w // 8) * 8, (h // 8) * 8


def main():
    parser = argparse.ArgumentParser(description="BlackRoad Image Generator")
    parser.add_argument("prompt", nargs="?", help="Text prompt for image generation")
    parser.add_argument("--output", "-o", help="Output filename (default: auto-named)")
    parser.add_argument("--size", "-s", default="1024x1024", help="Image size WxH (default: 1024x1024)")
    parser.add_argument("--model", "-m", default="turbo", choices=["turbo", "lightning", "sdxl"])
    parser.add_argument("--steps", type=int, help="Number of inference steps (overrides model default)")
    parser.add_argument("--count", "-n", type=int, default=1, help="Number of images to generate")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--batch", help="File with one prompt per line")
    parser.add_argument("--dir", default=str(OUTPUT_DIR), help="Output directory")

    args = parser.parse_args()

    if not args.prompt and not args.batch:
        parser.print_help()
        sys.exit(1)

    # Create output dir
    out_dir = Path(args.dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    width, height = parse_size(args.size)
    print(f"Size: {width}x{height}")

    # Load model
    start = time.time()
    pipe, defaults = load_pipeline(args.model)
    print(f"Model loaded in {time.time() - start:.1f}s")

    # Collect prompts
    if args.batch:
        with open(args.batch) as f:
            prompts = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    else:
        prompts = [args.prompt]

    # Generate
    total = len(prompts) * args.count
    generated = []

    for i, prompt in enumerate(prompts):
        for j in range(args.count):
            idx = i * args.count + j + 1
            print(f"\n[{idx}/{total}] Generating: {prompt[:80]}...")

            seed = args.seed + j if args.seed is not None else None
            start = time.time()
            image = generate(pipe, prompt, defaults, width, height, args.steps, seed)
            elapsed = time.time() - start

            if args.output and len(prompts) == 1 and args.count == 1:
                filename = args.output
            else:
                # Auto-name from prompt
                safe = "".join(c if c.isalnum() or c in " -_" else "" for c in prompt[:40]).strip().replace(" ", "-").lower()
                filename = f"{safe}-{idx}.png"

            filepath = out_dir / filename
            image.save(filepath)
            print(f"Saved: {filepath} ({elapsed:.1f}s)")
            generated.append(str(filepath))

    print(f"\nDone. {len(generated)} image(s) generated in {args.dir}")
    for p in generated:
        print(f"  {p}")


if __name__ == "__main__":
    main()
