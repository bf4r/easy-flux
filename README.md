# easy-flux
Make FLUX.1 images quickly using this simple python script

# Requirements
- Python 3.12 (https://www.python.org/downloads/)
- Replicate API token (https://replicate.com/account/api-tokens)

# Quick install
```
git clone https://github.com/bf4r/easy-flux
cd easy-flux
pip install -r requirements.txt
python flux.py a house, illustration
```

# Step-by-step Install
1. Clone the repo
```
git clone https://github.com/bf4r/easy-flux
```
2. cd
```
cd easy-flux
```
3. Install requirements
```
pip install -r requirements.txt
```
4. Run
```
python flux.py a house, illustration
```
Note: The first time you run flux.py, you will be asked to enter your [Replicate API token](https://replicate.com/account/api-tokens).
Alternatively, you can add a .env file to the repository folder:
```
REPLICATE_API_TOKEN=your_token_here
```

# Image Generation with Flux Models

## Usage

All parameters (but prompt) have default values, but you can specify them like this:

```bash
python flux.py A beautiful painting --model dev --aspect 1:1 --steps 30 --guidance 3.5 --seed 42 --format png --quality 90 --bypass True --path "./output.png"
```

## Arguments

- **prompt** (required): The prompt for image generation, text (e.g. `A beautiful painting`).
- No special codes, just put it right after `flux.py`

- **--model**: The model to use for generation (default: `schnell`)
Examples:
  - `schnell`
  - `dev`
  - `pro`
  - Full model name (`black-forest-labs/flux-dev`)
  - Only model name (`flux-dev`)

- **--aspect**: The aspect ratio of the output image (default: `1:1`).
Available choices:
  - `1:1`
  - `16:9`
  - `21:9`
  - `2:3`
  - `3:2`
  - `4:5`
  - `5:4`
  - `9:16`
  - `9:21`

- **--steps**: The number of denoising steps to use (default: `30`). This parameter is ignored for `flux-schnell`.

- **--guidance**: Guidance scale, determining how much the model follows your prompt (default: `3.5`). This parameter is ignored for `flux-schnell`.

- **--seed**: The seed to use for randomness (default: random). If you use the same seed and prompt twice, the image will be the same.

- **--format**: The output format of the image (default: `png`).
Options:
- `webp`
- `png`
- `jpg`

- **--quality**: The output quality of the image (1-100, default: `90`).

- **--bypass**: Bypass the safety checker (default: `True`).

- **--path**: The path to download the output file to (just prints the image link by default).

## Example
Desktop wallpaper
```
python flux.py an artistic landscape, high quality --model dev --aspect 16:9
```
