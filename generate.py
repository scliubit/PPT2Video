import os
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from pdf2image import convert_from_path
from google.cloud import texttospeech

# Paths and parameters
pdf_path = "./Slides.pdf"
output_image_folder = "./output/"
audio_prefix_path = "./assets/"  # For example, if the audio file is in /audio/P1.wav, then this is /audio/
output_video_file = "output_video.mp4"

if not os.path.exists(output_image_folder):
    os.system("mkdir " + output_image_folder)


if not os.path.exists(audio_prefix_path):
    os.system("mkdir " + audio_prefix_path)


# Convert PDF pages to PNG images
def pdf_to_pngs(pdf_path, output_folder):
    images = convert_from_path(pdf_path, dpi=300)

    for idx, image in enumerate(images):
        image.save(f"{output_folder}/{idx+1}.png", "PNG")


# Create a video from images and audio
def create_video_from_images_and_audio(image_folder, audio_prefix, output_video):
    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.endswith(".png")],
        key=lambda x: int(x.split(".")[0]),
    )

    clips = []
    for idx, image_file in enumerate(image_files):
        audio_path = f"{audio_prefix}P{idx+1}.mp3"

        if os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            img_clip = ImageSequenceClip(
                [os.path.join(image_folder, image_file)], durations=[audio.duration]
            )
            img_clip = img_clip.set_audio(audio)
            clips.append(img_clip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac", fps=24)


if __name__ == "__main__":
    client = texttospeech.TextToSpeechClient()

    with open("speech.txt", "r") as f:
        content = f.readlines()
        for line in content:
            if line[0] == "P":
                temp = line
                page = int(temp.split("::")[0][1:])
                speech = temp.split("::")[1].strip()
                print("P{}\t".format(page) + speech)
                synthesis_input = texttospeech.SynthesisInput(text=speech)
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )
                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )
                with open("./assets/P" + str(page) + ".mp3", "wb") as out:
                    out.write(response.audio_content)
                    # print('Audio content written to file "output.mp3"' + str(page))

    # Check or create the image output folder
    if not os.path.exists(output_image_folder):
        os.mkdir(output_image_folder)

    # Convert PDF to PNGs
    pdf_to_pngs(pdf_path, output_image_folder)

    # Create the video
    create_video_from_images_and_audio(
        output_image_folder, audio_prefix_path, output_video_file
    )
