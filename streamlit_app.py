import os
import time
import tempfile
import traceback

import streamlit as st
from langdetect import detect, LangDetectException

try:
    from TTS.api import TTS
except Exception:
    TTS = None

# Optional lazy Qwen3 import
qwen3_model = None

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED_LANGUAGES = ["auto", "ar", "en", "fr", "tr", "es", "bm"]
XTTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
xtts = None


def load_xtts():
    global xtts
    if xtts is None:
        if TTS is None:
            raise RuntimeError("TTS library is not installed. Please install TTS (Coqui TTS).")
        xtts = TTS(XTTS_MODEL, progress_bar=True)
    return xtts


def detect_language_from_text(text: str) -> str:
    if not text or not text.strip():
        return "ar"
    try:
        lang = detect(text.strip())
        if lang in SUPPORTED_LANGUAGES:
            return lang
        if lang == "bm":
            return "bm"
        return "ar"
    except (LangDetectException, Exception):
        return "ar"


def load_qwen3_model(model_id: str = "QwenLM/qwen3-tts-base"):
    global qwen3_model
    if qwen3_model is not None:
        return qwen3_model
    try:
        from qwen_tts.inference.qwen3_tts_model import Qwen3TTSModel
    except Exception as e:
        raise RuntimeError(f"Qwen3 package not installed or import failed: {e}")
    st.info(f"Loading Qwen3 model {model_id} (may require GPU and take time)...")
    model = Qwen3TTSModel.from_pretrained(model_id)
    qwen3_model = model
    return qwen3_model


def save_uploaded_file(uploaded, suffix=".wav"):
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tf.write(uploaded.read())
    tf.flush()
    tf.close()
    return tf.name


def clone_with_xtts(text: str, ref_audio_path: str, language: str):
    load_xtts()
    ts = int(time.time() * 1000)
    out_path = os.path.join(OUTPUT_DIR, f"clone_{ts}.wav")
    xtts.tts_to_file(text=text, speaker_wav=ref_audio_path, language=language, file_path=out_path)
    return out_path


def clone_with_qwen3(text: str, ref_audio_path: str, language: str, x_vector_only: bool, model_id: str):
    model = load_qwen3_model(model_id)
    lang_arg = None if language in (None, "auto") else language
    wavs, sr = model.generate_voice_clone(
        text=text,
        language=lang_arg,
        ref_audio=ref_audio_path,
        x_vector_only_mode=x_vector_only,
    )
    wav = wavs[0] if isinstance(wavs, list) else wavs
    ts = int(time.time() * 1000)
    out_path = os.path.join(OUTPUT_DIR, f"clone_qwen3_{ts}.wav")
    import numpy as np
    import soundfile as sf
    sf.write(out_path, np.asarray(wav).astype(np.float32), sr)
    return out_path


st.set_page_config(page_title="Bam-kanladege", layout="centered")
st.title("تطبيق استنساخ الصوت")

st.sidebar.header("إعدادات")
engine = st.sidebar.selectbox("محرك التوليد", ("xtts_v2", "qwen3"))
language_choice = st.sidebar.selectbox("اللغة", SUPPORTED_LANGUAGES, index=0)
qwen_model_id = st.sidebar.text_input("Qwen3 Model repo id", value="QwenLM/qwen3-tts-base")
x_vector_only = st.sidebar.checkbox("استخدام X-vector", value=True)

st.markdown("- ارفع ملف صوتي مرجعي (3-10 ثواني)\n- اكتب النص\n- اختر اللغة أو auto\n- اضغط توليد")

uploaded_audio = st.file_uploader("الصوت المرجعي", type=["wav", "mp3", "m4a", "ogg"])
text_input = st.text_area("النص", height=140, placeholder="اكتب النص هنا...")

if st.button("توليد الصوت"):
    if not text_input or uploaded_audio is None:
        st.error("يرجى إدخال النص ورفع ملف صوتي مرجعي.")
    else:
        try:
            ref_path = save_uploaded_file(uploaded_audio)
            selected_lang = detect_language_from_text(text_input) if language_choice == "auto" else language_choice
            st.info(f"اللغة المختارة: {selected_lang} | المحرك: {engine}")

            if engine == "xtts_v2":
                out_path = clone_with_xtts(text_input, ref_path, selected_lang)
            else:
                out_path = clone_with_qwen3(text_input, ref_path, selected_lang, x_vector_only, qwen_model_id)

            with open(out_path, "rb") as f:
                data = f.read()

            st.success("تم إنشاء الصوت بنجاح.")
            st.audio(data)
            st.download_button("تحميل الملف الناتج", data=data, file_name=os.path.basename(out_path), mime="audio/wav")
        except Exception as e:
            st.error(f"حدث خطأ أثناء التوليد: {e}")
            st.code(traceback.format_exc())
