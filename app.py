import os
import time
import traceback
from typing import Optional

import gradio as gr
from TTS.api import TTS
from langdetect import LangDetectException, detect
import numpy as np
import soundfile as sf

# Optional import for Qwen3-TTS (lazy-loaded)
qwen3_model = None

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED_LANGUAGES = ["auto", "ar", "en", "fr", "tr", "es", "bm"]

# Default TTS engine model
XTTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

print("جاري تهيئة بيئة النماذج... قد يستغرق بعض الوقت أول مرة.")
# Load the lightweight/default TTS (Coqui TTS) lazily when first used
tts = None

def load_xtts():
    global tts
    if tts is None:
        try:
            print(f"تحميل نموذج XTTS: {XTTS_MODEL} ...")
            tts = TTS(XTTS_MODEL, progress_bar=True)
            print("تم تحميل نموذج XTTS.")
        except Exception as e:
            print(f"فشل تحميل نموذج XTTS: {e}")
            raise


def detect_language_from_text(text: str) -> str:
    """يكتشف اللغة تلقائيًا من النص، مع دعم البامبارا إن أمكن."""
    if not text or not text.strip():
        return "ar"
    try:
        lang = detect(text.strip())
        # langdetect قد يرجع رموز مثل 'fr', 'en', 'bm' إن أمكن
        if lang in SUPPORTED_LANGUAGES:
            return lang
        if lang == "bm":
            return "bm"
        # Fall back to Arabic as safe default (مشروعك افتراضيًا عربي)
        return "ar"
    except (LangDetectException, ValueError):
        return "ar"


# Qwen3 lazy loader
def load_qwen3_model(model_id: str = "QwenLM/qwen3-tts-base"):
    """حاول تحميل نموذج Qwen3-TTS من مسار HuggingFace أو دليل محلي. يُخزَّن عالميًا في qwen3_model."""
    global qwen3_model
    if qwen3_model is not None:
        return qwen3_model
    try:
        print(f"محاولة تحميل Qwen3-TTS من: {model_id} (قد يتطلّب GPU والوقت)...")
        from qwen_tts.inference.qwen3_tts_model import Qwen3TTSModel

        model = Qwen3TTSModel.from_pretrained(model_id)
        qwen3_model = model
        print("تم تحميل نموذج Qwen3-TTS بنجاح.")
        return qwen3_model
    except Exception as e:
        print(f"فشل تحميل Qwen3-TTS: {e}")
        raise


def clone_with_xtts(text: str, ref_audio: str, language: str) -> str:
    load_xtts()
    timestamp = int(time.time() * 1000)
    output_path = os.path.join(OUTPUT_DIR, f"clone_{timestamp}.wav")
    tts.tts_to_file(
        text=text,
        speaker_wav=ref_audio,
        language=language,
        file_path=output_path,
    )
    return output_path


def clone_with_qwen3(text: str, ref_audio: str, language: Optional[str], x_vector_only: bool, model_id: str) -> str:
    # model_id can be a HF repo like 'QwenLM/qwen3-tts-base' or custom path
    model = load_qwen3_model(model_id)
    # Qwen expects language like 'Auto' or language names; keep as-is
    try:
        # Use x_vector_only_mode=True to avoid requiring ref_text transcript
        wavs, sr = model.generate_voice_clone(
            text=text,
            language=language if language is not None and language != "auto" else None,
            ref_audio=ref_audio,
            x_vector_only_mode=x_vector_only,
            # you can add sampling kwargs here if desired
        )
        # generate_voice_clone returns list of wavs (np.ndarray)
        if isinstance(wavs, list) and len(wavs) > 0:
            wav = wavs[0]
        else:
            wav = np.asarray(wavs)
        timestamp = int(time.time() * 1000)
        output_path = os.path.join(OUTPUT_DIR, f"clone_qwen3_{timestamp}.wav")
        sf.write(output_path, wav.astype(np.float32), sr)
        return output_path
    except Exception as exc:
        traceback.print_exc()
        raise


def clone_voice(text, ref_audio, language="auto", engine="xtts_v2", qwen3_model_id="QwenLM/qwen3-tts-base", x_vector_only=True):
    if not text or ref_audio is None:
        return "ادخل النص والصوت المرجعي"

    # determine language
    selected_language = detect_language_from_text(text) if language == "auto" else language
    # normalize selected_language for Qwen3 usage: Qwen allows various language names; we pass None to use Auto
    qwen_language = None if selected_language == "auto" else selected_language

    try:
        if engine == "xtts_v2":
            output_path = clone_with_xtts(text, ref_audio, selected_language)
        elif engine == "qwen3":
            # Qwen model loading may throw if not installed or model unavailable
            output_path = clone_with_qwen3(text, ref_audio, qwen_language, x_vector_only, qwen3_model_id)
        else:
            return f"محرك غير مدعوم: {engine}"

        return output_path, selected_language
    except Exception as exc:
        traceback.print_exc()
        return f"حدث خطأ أثناء إنشاء الصوت: {exc}", selected_language


with gr.Blocks(title="تطبيق استنساخ الصوت — يدعم Qwen3 و XTTS") as demo:
    gr.Markdown(
        """
        # تطبيق استنساخ الصوت
        قم برفع ملف صوتي مرجعي (3-10 ثوانٍ)، ثم اكتب النص الذي تريد أن يقولَه الصوت نفسه.
        يمكنك اختيار محرك التوليد: XTTS (خفيف نسبيًا) أو Qwen3-TTS (أقوى لكنه يحتاج موارد أكبر).
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

            engine_input = gr.Dropdown(
                choices=["xtts_v2", "qwen3"],
                label="محرك التوليد",
                value="xtts_v2",
            )

            qwen_model_id = gr.Textbox(
                label="Qwen3 Model repo id (إذا اخترت qwen3)",
                value="QwenLM/qwen3-tts-base",
                placeholder="مثال: QwenLM/qwen3-tts-base أو مسار محلي",
            )

            xvec_checkbox = gr.Checkbox(label="استخدام X-vector (لا يحتاج نص مرجعي للصوت)", value=True)

            ref_audio = gr.Audio(label="الصوت المرجعي (3-10 ثواني)", type="filepath")
            generate_btn = gr.Button("توليد الصوت")

        with gr.Column(scale=1):
            output_audio = gr.Audio(label="الصوت المستنسخ")
            status_box = gr.Textbox(label="الحالة", interactive=False)

    def handle_generate(text, audio_path, language, engine, qwen_id, xvec_only):
        if not text or not audio_path:
            return None, "يرجى إدخال النص والصوت المرجعي."

        # If engine is qwen3 and model not loaded, inform user that Qwen3 requires extra setup
        if engine == "qwen3":
            try:
                # try lazy loading to give immediate error if qwen package missing
                # but do not block UI: we will catch exceptions
                _ = load_qwen3_model(qwen_id)
            except Exception as e:
                return None, f"فشل تحميل Qwen3-TTS. تأكد من تثبيت الحزمة وتشغيل النموذج. خطأ: {e}"

        result = clone_voice(text, audio_path, language, engine, qwen_id, xvec_only)

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
        inputs=[text_input, ref_audio, language_input, engine_input, qwen_model_id, xvec_checkbox],
        outputs=[output_audio, status_box],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
