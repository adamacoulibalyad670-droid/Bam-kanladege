import os
import time
import traceback

import gradio as gr
from TTS.api import TTS
from langdetect import LangDetectException, detect

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED_LANGUAGES = ["auto", "ar", "en", "fr", "tr", "es", "bm"]

print("جاري تحميل نموذج الاستنساخ... قد يستغرق بعض الوقت أول مرة.")
try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)
except Exception as e:
    print(f"فشل تحميل النموذج: {e}")
    raise


def detect_language_from_text(text):
    """يكتشف اللغة تلقائيًا من النص، مع دعم البامبارا إن أمكن."""
    if not text or not text.strip():
        return "ar"
    try:
        lang = detect(text.strip())
        if lang in SUPPORTED_LANGUAGES:
            return lang
        # بعض المحاولات قد تُرجع رموزًا ذات تنويع لا يدعمها النموذج مباشرة
        # في هذه الحالة نرجع العربية كخيار آمن أو نستخدم bm إذا كانت الجملة بامبارا.
        if lang == "bm":
            return "bm"
        return "ar"
    except (LangDetectException, ValueError):
        return "ar"


def clone_voice(text, ref_audio, language="auto"):
    if not text or ref_audio is None:
        return "ادخل النص والصوت المرجعي"

    selected_language = detect_language_from_text(text) if language == "auto" else language

    try:
        timestamp = int(time.time() * 1000)
        output_path = os.path.join(OUTPUT_DIR, f"clone_{timestamp}.wav")

        tts.tts_to_file(
            text=text,
            speaker_wav=ref_audio,
            language=selected_language,
            file_path=output_path,
        )
        return output_path, selected_language
    except Exception as exc:
        traceback.print_exc()
        return f"حدث خطأ أثناء إنشاء الصوت: {exc}", selected_language


with gr.Blocks(title="تطبيق استنساخ الصوت") as demo:
    gr.Markdown(
        """
        # تطبيق استنساخ الصوت
        قم برفع ملف صوتي مرجعي (3-10 ثوانٍ)، ثم اكتب النص الذي تريد أن يقولَه الصوت نفسه.
        يتم اكتشاف اللغة تلقائيًا عند اختيار "auto"، مع دعم اللغة البامبارا (bm).
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
                choices=SUPPORTED_LANGUAGES,
                label="اللغة",
                value="auto",
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

        if isinstance(result, tuple):
            generated_path, detected_lang = result
            if isinstance(generated_path, str) and generated_path.endswith(".wav") and os.path.exists(generated_path):
                return generated_path, f"تم إنشاء الصوت بنجاح. اللغة المستخدمة: {detected_lang}"
            return None, f"{generated_path}"

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
