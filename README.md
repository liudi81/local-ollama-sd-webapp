# Ollama SD WebApp

🧠💬🎨 A local web app that lets you **chat with Ollama** and **generate images using Stable Diffusion**, all in one conversational interface. Run it entirely offline using open-source models. It's created with the help of **ChatGPT**.

---

## ✨ Features

- 💬 Chat with lightweight local LLMs via [Ollama](https://ollama.com)
- 🎨 Generate images with your own prompts using [Stable Diffusion](https://github.com/huggingface/diffusers)
- 🔁 Share context between chat and image generation
- 🖥️ Runs locally — no cloud needed
- 🌐 Simple web interface (Flask backend + HTML frontend)

---

## 🖥️ Requirements

- Python 3.9+
- pip
- At least **2 GB RAM** (more recommended for larger models)
- [Ollama](https://ollama.com) installed
- Optional: [diffusers](https://github.com/huggingface/diffusers) + Stable Diffusion model

---

## 🛠️ Installation

```bash
git clone https://github.com/liudi81/local-ollama-sd-webapp.git
cd local-ollama-sd-webapp

# Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull a small model (e.g. tinyllama) to avoid memory issues
ollama pull tinyllama

# Run the app
python3 app.py

## 🧠 Lessons learned
  - Ollama models (like TinyLlama) only generate text — they do not create real images.
  - When LLMs return image links (e.g. Imgur), they are usually made up and not connected to your Stable Diffusion output.
  - Image generation with Stable Diffusion on CPU is slow; smaller resolutions (like 256×256) help. But the quality for 256x256 images is not good, and it failed sometimes.
  - Some models (like `llama3`) require more memory than lightweight devices can handle.
  - You can combine image and chat in a shared session, but need logic to distinguish between the two tasks.
  - It's quite slow to use CPUs in my laptop to generate images. It takes 7+ minutes to generate one 512x512 image.

