import replicate
import argparse
import requests
import random
import os
import dotenv
import sys

dotenv.load_dotenv()
if os.getenv("REPLICATE_API_TOKEN") is not None:
    os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")
else:
    #print("REPLICATE_API_TOKEN not found. Please set REPLICATE_API_TOKEN=... in the .env file, where ... is your Replicate API key. You can get a Replicate API token here: https://replicate.com/account/api-tokens.")
    key = input("REPLICATE_API_TOKEN not found. Please enter your Replicate API token, you won't have to enter it again. (Get it here: https://replicate.com/account/api-tokens): ")
    os.environ["REPLICATE_API_TOKEN"] = key
    # save the key to .env
    with open('.env', 'w') as f:
        f.write(f'REPLICATE_API_TOKEN={key}\n')

def run_model(prompt, model, aspect, steps, guidance, seed, format, quality, bypass):
    model_versions = {
        "schnell": "black-forest-labs/flux-schnell",
        "dev": "black-forest-labs/flux-dev",
        "pro": "black-forest-labs/flux-pro",
        "flux-schnell": "black-forest-labs/flux-schnell",
        "flux-dev": "black-forest-labs/flux-dev",
        "flux-pro": "black-forest-labs/flux-pro"
    }
    model = model_versions.get(model, model)
    if model == "black-forest-labs/flux-schnell":
        input_data = {
        "prompt": prompt,
        "aspect_ratio": aspect,
        "output_format": format,
        "output_quality": quality,
        "disable_safety_checker": bypass,
        "seed": seed
        }
    else:
        input_data = {
        "prompt": prompt,
        "aspect_ratio": aspect,
        "output_format": format,
        "output_quality": quality,
        "disable_safety_checker": bypass,
        "seed": seed,
        "num_inference_steps": steps,
        "guidance": guidance
        }
    
    try:
        output = replicate.run(
        model,
        input=input_data
        )
        return output[0]
    except replicate.exceptions.ReplicateError as e:
        if e.status == 401:
            print("An invalid Replicate API token was provided, please modify the .env file and enter a valid one. (Get it here: https://replicate.com/account/api-tokens)")
            sys.exit(0)
        else:
            print(e)

def download_image(url, save_path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {save_path}")
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Easily generate images using Flux models on Replicate.")
    parser.add_argument("prompt", nargs="+", help="The prompt for image generation, text (e.g. A beautiful painting)")
    parser.add_argument("--model", default="schnell", help="The model to use for generation (default: schnell), (schnell, dev, pro, black-forest-labs/flux-schnell, flux-dev, ...)")
    parser.add_argument("--aspect", choices=["1:1", "16:9", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"], default="1:1", help="The aspect ratio of the output image (default: 1:1)")
    parser.add_argument("--steps", type=int, default=30, help="The number of denoising steps to use (default: 30) (ignored for flux-schnell)")
    parser.add_argument("--guidance", type=float, default=3.5, help="Guidance scale, how much the model follows your prompt (default: 3.5) (ignored for flux-schnell)")
    parser.add_argument("--seed", type=int, default=None, help="The seed to use (default: random)")
    parser.add_argument("--format", default="png", help="The output format of the image (default: png)")
    parser.add_argument("--quality", type=int, default=90, help="The output quality of the image (1-100) (default: 90)")
    parser.add_argument("--bypass", type=bool, default=True, help="Bypass the safety checker (default: True)")
    parser.add_argument("--path", default="", help="The path to download the output file to (default: prints image URL)")

    args = parser.parse_args()

    prompt = " ".join(args.prompt)
    model = args.model
    aspect = args.aspect
    steps = args.steps
    guidance = args.guidance
    seed = args.seed
    format = args.format
    quality = args.quality
    bypass = args.bypass
    
    if seed is None:
        seed = random.randint(0, 2147483647)

    output_url = run_model(prompt, model, aspect, steps, guidance, seed, format, quality, bypass)
    print(f"{output_url}")
    if args.path != "":
        download_image(output_url, args.path)

if __name__ == "__main__":
    main()