# PPT2Video

generate video with voice narration from ppt/pdf Slides. Make your slides (`Slides.pdf`) and write down your narration manuscript (`speech.txt`) here, then you can generate the video presentation using `generate.py`.

For Linux/macOS, the procedure goes like:

```bash
python3 -m venv ./speech
source ./speech/bin/activate

pip install google-cloud-storage
pip install --upgrade google-cloud-texttospeech
pip install moviepy
pip install pdf2image

python generate.py
```

Should you have any problems please leave me messages in `issue`.
