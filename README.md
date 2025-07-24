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
git clone https://github.com/yourusername/ollama-sd-webapp.git
cd ollama-sd-webapp

# Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull a small model (e.g. tinyllama) to avoid memory issues
ollama pull tinyllama

# Run the app
python app.py

