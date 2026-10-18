import os
import time
import traceback

import gradio as gr
from TTS.api import TTS

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("جاري تحميل نموذج الاستنساخ... قد يستغرق بعض الوقت أول مرة.")
try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)
except Exception as e:
    print(f"فشل تحميل النموذج: {e}")
    raise


def clone_voice(text, ref_audio, language="ar"):
    if not text or ref_audio is None:
        return "ادخل النص والصوت المرجعي"

    try:
        timestamp = int(time.time() * 1000)
        output_path = os.path.join(OUTPUT_DIR, f"clone_{timestamp}.wav")

        tts.tts_to_file(
            text=text,
            speaker_wav=ref_audio,
            language=language,
            file_path=output_path,
        )
        return output_path
    except Exception as exc:
        traceback.print_exc()
        return f"حدث خطأ أثناء إنشاء الصوت: {exc}"


with gr.Blocks(title="تطبيق استنساخ الصوت") as demo:
    gr.Markdown(
        """
        # تطبيق استنساخ الصوت
        قم برفع ملف صوتي مرجعي (3-10 ثوانٍ)، ثم اكتب النص الذي تريد أن يقولَه الصوت نفسه.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="النص الذي سيقوله الصوت المستنسخ",
                lines=4,
                placeholder="اكتب النص هنا...",
            )
            language_input = gr.Dropdown(
                choices=["ar", "en", "fr", "tr", "es"],
                label="اللغة",
                value="ar",
            )
            ref_audio = gr.Audio(label="الصوت المرجعي (3-10 ثواني)", type="filepath")
            generate_btn = gr.Button("توليد الصوت")

        with gr.Column(scale=1):
            output_audio = gr.Audio(label="الصوت المستنسخ")
            status_box = gr.Textbox(label="الحالة", interactive=False)

    def handle_generate(text, audio_path, language):
        if not text or not audio_path:
            return None, "يرجى إدخال النص والصوت المرجعي."

        result = clone_voice(text, audio_path, language)

        if isinstance(result, str) and result.endswith(".wav") and os.path.exists(result):
            return result, "تم إنشاء الصوت بنجاح."
        return None, str(result)

    generate_btn.click(
        handle_generate,
        inputs=[text_input, ref_audio, language_input],
        outputs=[output_audio, status_box],
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
