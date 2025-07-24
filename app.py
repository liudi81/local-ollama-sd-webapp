from datetime import datetime
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from flask import Flask, request, jsonify, render_template, session
from PIL import Image
import ollama
import os, time
import torch


app = Flask(__name__)
app.secret_key = "dummy_secret_key"

# Session state
session = {
    "history": [],
    "last_image": None,
    "last_prompt": None,
}

# Load models
print("Loading Stable Diffusion models...")
txt2img_pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5").to("cpu")
img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5").to("cpu")

# Ensure static image folder exists
os.makedirs("static", exist_ok=True)

# There are issues for 256x256 resolution (failure, bad quality, etc.)
IMG_HEIGHT = 512  #256
IMG_WIDTH = 512  #256

# Commands to create a new image from scratch
new_image_commands = ["NewImage", "ImageFromScratch"]

# Commands to create a new image from a existing image
image_to_image_commands = [
    "Image2Image", "ImageToImage", "ImageFromImage", "Img2Img", "ImgToImg"
]


def contains_any_string_in_list(main_string, substrings_list):
    """
    Checks if a string contains any of the substrings in a list, case-insensitively.

    Args:
        main_string (str): The string to search within.
        substrings_list (list): A list of strings to search for.

    Returns:
        bool: True if any substring is found, False otherwise.
    """
    main_string_lower = main_string.lower(
    )  # Convert main string to lowercase once
    for sub in substrings_list:
        if sub.lower(
        ) in main_string_lower:  # Convert substring to lowercase for comparison
            return True
    return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    if "chat_history" not in session:
        session["chat_history"] = []

    messages = session["chat_history"] + [{
        "role": "user",
        "content": user_msg
    }]
    # llama3 requires 8GB memory, not suitable for my laptop, switch to tinyllama
    #response = ollama.chat(model="llama3", messages=messages)
    response = ollama.chat(model="tinyllama", messages=messages)
    ai_reply = response["message"]["content"]

    session["chat_history"].append({"role": "user", "content": user_msg})
    session["chat_history"].append({"role": "assistant", "content": ai_reply})

    return jsonify({"reply": ai_reply})


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "A fantasy landscape")
    mode = data.get("mode", "auto")

    if contains_any_string_in_list(prompt, new_image_commands):
        mode = "new"
    elif contains_any_string_in_list(prompt, image_to_image_commands):
        mode = "from_image"
    else:
        mode = "auto"

    start = time.time()
    if "last_image_path" in session and mode != "new":
        # Modify previous image
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Will generate image from previous image {session['last_image_path']} ...")
        init_image = Image.open(
            session["last_image_path"]).convert("RGB").resize((IMG_HEIGHT, IMG_WIDTH))
        result = img2img_pipe(prompt=prompt,
                              image=init_image,
                              strength=0.75,
                              guidance_scale=7.5)
    else:
        # Generate from scratch
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Will generate a new image from scratch ...")
        result = txt2img_pipe(prompt=prompt,
                              height=IMG_HEIGHT,
                              width=IMG_WIDTH,
                              guidance_scale=7.5)

    end = time.time()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] It took {end - start:.2f} seconds to generate the image.")

    image = result.images[0]
    filename = f"static/image_{int(time.time())}.png"
    image.save(filename)
    session["last_image_path"] = filename
    session["last_prompt"] = prompt

    return jsonify({"image_url": filename})


if __name__ == "__main__":
    app.run(debug=True)
