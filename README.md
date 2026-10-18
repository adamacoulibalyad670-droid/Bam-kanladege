# Bam-kanladege
pip install TTS gradio
import gradio as gr
from TTS.api import TTS

# تحميل نموذج الاستنساخ (يحمله مرة واحدة فقط)
print("جاري تحميل نموذج الاستنساخ...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)

def clone_voice(text, ref_audio, language):
    if not text or ref_audio is None:
        return "ادخل النص والصوت المرجعي"
    
    output_path = "output_clone.wav"
    tts.tts_to_file(
        text=text,
        speaker_wav=ref_audio,
        language=language,
        file_path=output_path
    )
    return output_path

# واجهة الاستخدام
demo = gr.Interface(
    fn=clone_voice,
    inputs=[
        gr.Textbox(label="النص الذي سيقوله الصوت المستنسخ", lines=3),
        gr.Audio(label="الصوت المرجعي (3-10 ثواني)", type="filepath"),
        gr.Dropdown(["ar", "en", "fr", "tr", "es"], label="اللغة", value="ar")
    ],
    outputs=gr.Audio(label="الصوت المستنسخ"),
    title="نظام استنساخ الصوت",
    description="ارفع صوت 10 ثواني + اكتب النص وسيتكلم بنفس الصوت"
)

demo.launch()
python voice_clone.py
Bamanankan tts Fɔlɔ 
import torch
import soundfile as sf
from transformers import VitsModel, AutoTokenizer

# Available languages: bambara, boomu, dogon, pular, songhoy, tamasheq
language = "bambara"
model_id = "Bamanakan-tts"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id, subfolder=f"models/{language}")
model = VitsModel.from_pretrained(model_id, subfolder=f"models/{language}")

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Synthesize speech
text = "Nin ye bamanankan nimɔrɔko ɲɛjiralan dafalen ye. Jateden minnu bɛ bɔ 0 la ka se 10 ma : 0: fu 1: kelen 2: fila (walima fla) 3: saba 4: naani 5: duuru 6: wɔɔrɔ 7: wolonwula (walima wolonwufla) 8: lajɛ 9: 1 conton la code pour les nombres entre 11 Ani 19, 11: tan ni kelen (10 Ani 1) 12: tan ni fila (10 Ani 2) 13: tan ni saba 14: tan ni naani 15: tan ni duuru16: tan ni wɔɔrɔ17: tan ni wolonwula18: tan ni seegin19: tan ni kɔnɔntɔn Tan tɔw bɛɛ kama k’a ta 30 na ka se 90 ma, an bɛ baara kɛ ni daɲɛ fɔlɔ bi- ye min bɛ tugu ɲɔgɔn kɔ ni jateden cayalen ye :20: mugan30: bisaba (Tan ka bɔ 3 la)40: binaani
50: biduuru
60: biwɔɔrɔ 
70:Biwolwula
80: Biseegin
90:Bikɔnɔntɔn
Jatedenba 100: kɛmɛ 
1 000: Bakelen (walima Wakelen walima Wagakelen) . 
1 111 : bakelen ani kɛmɛ ni tan ni kelen 
1 000000: miliyɔn kelen 
1 111111: miliyɔn kelen ani bakɛmɛ kɛmɛ ni tan ni kelen ani kɛmɛ ni tan ni kelen  
1 000000000: miliyari kelen
1 111111111: miliyari kelen ani miliyɔn kelen ni kɛmɛ ni tan ni kelen ani bakɛmɛ kɛmɛ ni tan ni kelen ani kɛmɛ ni tan ni kelen 
1 000000000000:tiriliyɔni kelen 
1 111111111111 : tiriliyɔni kelen ani miliyari kelen ni kɛmɛ ni tan ni kelen ani miliyɔn kelen ni kɛmɛ ni tan ni kelen ani bakɛmɛ ni tan ni kelen ani kɛmɛ ni tan ni kelen 
1,1% : kɛmɛsarada la kelen n'a kunkanfɛn kelen 
1%: kɛmɛsarada la kelen 
1001%: kɛmɛsarada la bakelen an'a kunkanfɛn kelen
A kɛ a ka kalan kɛ lɛrɛ la
10:30:01 : nɛgɛ kanɲɛ tan tɛmɛnen ye ni sanga bisaba ye ani segɔni kelen  
18h02:01: nɛgɛ kanɲɛ tan ni seegin tɛmɛnen ye ni sanga fila ye ani segɔni kelen 
18:00: nɛgɛ kanɲɛ tan ni seegin
100.000:bakɛmɛ
II: fila 
I: kelen 
1,1: kelen n'a kunkanfɛn kelen 
1,100: kelen an'a kunkanfɛn kɛmɛ
B: be
C: ce
D: de
F: fe
G: ge
H: he
J: je
K:ke
L: le
M: me
N: ne
Ɲ: ɲe
Ŋ: ŋe
P: pe 
R: re 
S: se
T: te 
W: we 
Y: ye 
Z: ze
A E I Ɛ U O Ɔ 
B ba be bi bɛ bu bo bɔ
C ca ce ci cɛ cu co cɔ 
D da de di dɛ du do dɔ
F fa fe fi fɛ fu fo fɔ
G ga ge gi gɛ gu go gɔ 
H ha he hi hɛ hu ho hɔ 
J  ja je ji jɛ ju jo jɔ
K  ka ke ki kɛ ku ko kɔ
L  la le li lɛ lu lo lɔ
M  ma me mi mɛ mu mo mɔ
N  na ne ni nɛ nu no nɔ
Ɲ ɲa ɲe ɲi ɲɛ ɲu ɲo ɲɔ
Ŋ ŋa ŋe ŋi ŋɛ ŋu ŋo ŋɔ
P pa pe pi pɛ pu po pɔ 
R ra re ri rɛ ru ro rɔ
S sa se si sɛ su so sɔ 
T ta te ti tɛ tu to tɔ 
W wa we wi wɛ wu wo wɔ 
Y ya ye yi yɛ yu yo yɔ 
Z za ze zi zɛ zu zo zɔ

AA EE II ƐƐ UU OO ƆƆ 
B baa bee bii bɛɛ buu boo bɔɔ
C caa cee cii cɛɛ cuu coo cɔɔ 
D daa dee dii dɛɛ duu doo dɔɔ
F faa fee fii fɛɛ fuu foo fɔɔ
G gaa gee gii gɛɛ guu goo gɔɔ 
H haa hee hii hɛɛ huu hoo hɔɔ 
J  jaa jee jii jɛɛ juu joo jɔɔ
K  kaa kee kii kɛɛ kuu koo kɔɔ
L  laa lee lii lɛɛ luu loo lɔɔ
M  maa mee mii mɛɛ muu moo mɔɔ
N  naa nee nii nɛɛ nuu noo nɔɔ
Ɲ ɲaa ɲee ɲii ɲɛɛ ɲuu ɲoo ɲɔɔ
Ŋ ŋaa ŋee ŋii ŋɛɛ ŋuu ŋoo ŋɔɔ
P paa pee pii pɛɛ puu poo pɔɔ 
R raa ree rii rɛɛ ruu roo rɔɔ
S saa see sii sɛɛ suu soo sɔɔ 
T taa tee tii tɛɛ tuu too tɔɔ 
W waa wee wii wɛɛ wuu woo wɔɔ 
Y yaa yee yii yɛɛ yuu yoo yɔɔ 
Z zaa zee zii zɛɛ zuu zoo zɔɔ

AKA EKE IKI ƐKƐ UKU OKO ƆKƆ 
B baka beke biki bɛkɛ buku boko bɔkɔ
C caka ceke ciki cɛkɛ cuku coko cɔkɔ 
D daka deke diki dɛkɛ duku doko dɔkɔ
F faka feke fiki fɛkɛ fuku foko fɔlɔ
G gaka geke giki gɛkɛ guku goko gɔkɔ 
H haka heke hiki hɛkɛ huku hoko hɔkɔ 
J  jaka jeke jiki jɛkɛ juku joko jɔkɔ
K  kaka keke kiki kɛkɛ kuku koko kɔkɔ
L  laka leke liki lɛkɛ luku loko lɔkɔ
M  maka meke miki mɛkɛ muku moko mɔkɔ
N  naka neke niki nɛkɛ nuku noko nɔkɔ
Ɲ ɲaka ɲeke ɲiki ɲɛkɛ ɲuku ɲoko ɲɔkɔ
Ŋ ŋaka ŋeke ŋiki ŋɛkɛ ŋuku ŋoko ŋɔkɔ
P paka peke piki pɛkɛ puku poko pɔkɔ 
R raka reke riki rɛkɛ ruku roko rɔkɔ
S saka seke siki sɛkɛ suku soko sɔkɔ 
T taka teke tiki tɛkɛ tuku toko tɔkɔ 
W waka weje wiki wɛkɛ wuku woko wɔkɔ 
Y yaka yeke yiki yɛkɛ yuku yoko yɔkɔ 
Z zaka zeke ziki zɛkɛ zuku zoko zɔkɔ

AGA EGE IGI ƐGƐ UGU OGO ƆGƆ 
B baga bege bigi bɛgɛ bugu bogo bɔgɔ
C caga cege cigi cɛgɛ cugu cogo cɔgɔ 
D daga dege digi dɛgɛ dugu dogo dɔgɔ
F faga fege figi fɛgɛ fugu fogo fɔgɔ
G gaga gege gigi gɛgɛ gugu gogo gɔgɔ 
H haga hege higi hɛgɛ hugu hogo hɔgɔ 
J  jaga jege jigi jɛgɛ jugu jogo jɔgɔ
 K kaga kege kigi kɛgɛ kugu kogo kɔgɔ
L  laga lege ligi lɛgɛ lugu logo lɔgɔ
M  maga mege migi mɛgɛ mugu mogo mɔgɔ
N  naga nege nigi nɛgɛ nugu nogo nɔgɔ
Ɲ ɲaga ɲege ɲigi ɲɛgɛ ɲugu ɲogo ɲɔgɔ
Ŋ ŋaga ŋege ŋigi ŋɛgɛ ŋugu ŋogo ŋɔgɔ
P paga pege pigi pɛgɛ pugu pogo pɔgɔ 
R raga rege rigi rɛgɛ rugu rogo rɔgɔ
S saga sege sigi sɛgɛ sugu sogo sɔgɔ 
T taga tege tigi tɛgɛ tugu togo tɔgɔ 
W waga wege wigi wɛgɛ wugu wogo wɔgɔ 
Y yaga yege yigi yɛgɛ yugu yogo yɔgɔ 
Z zaga zege zigi zɛgɛ zugu zogo zɔgɔ
AN EN IN ƐN UN ON ƆN 
B ban ben bin bɛn bun bon bɔn
C can cen cin cɛn cun con cɔn 
D dan den din dɛn dun don dɔn
F fan fen fin fɛn fun fon fɔn
G gan gen gin gɛn gun gon gɔn 
H han hen hin hɛn hun hon hɔn 
J  jan jen jin jɛn jun jon jɔn
K  kan ken kin kɛn kun kon kɔn
L  lan len lin lɛn lun lon lɔn
M  man men min mɛn mun mon mɔn
N  nan nen nin nɛn nun non nɔn
Ɲ ɲan ɲen ɲin ɲɛn ɲun ɲon ɲɔn
Ŋ ŋan ŋen ŋin ŋɛn ŋun ŋon ŋɔn
P pan pen pin pɛn pun pon pɔn 
R ran ren rin rɛn run ron rɔn
S san sen sin sɛn sun son sɔn 
T tan ten tin tɛn tun ton tɔn 
W wan wen win wɛn wun won wɔn 
Y yan yen yin yɛn yun yon yɔn 
Z zan zen zin zɛn zun zon zɔn
40.000: babinaani
40,000: babinaani
 5,5: duuru n'a kunkanfɛn duuru 
5,100:duuru an'a kunkanfɛn kɛmɛ 
30.000: babisaba
30,000:babisaba
26,000: bamugan ni wɔɔrɔ
26.000:bamugan ni wɔɔrɔ
26000:bamugan ni wɔɔrɔ
16nan: tan ni wɔɔrɔnan
21,9%: kɛmɛsarada la mugan ni kelen n'a kunkanfɛn kɔnɔntɔn
42,7%: kɛmɛsarada la binaani ni fila n'a kunkanfɛn wolonwula
7,4%: kɛmɛsarada la wolonwula n'a kunkanfɛn naani
11,7%: kɛmɛsarada la tan ni kelen n'a kunkanfɛn wolonwula
111,7%: kɛmɛsarada la kɛmɛ ni tan ni kelen n'a kunkanfɛn wolonwula
12nan: tan ni filanan
18h: nɛgɛ kanɲɛ tan ni seegin
J-10CE: J-tan CE
2026: bafila ani Mugan ni Wɔɔrɔ 
Misaliw faralen ɲɔgɔn kancogo gɛlɛnw kanWalisa ka cɛmancɛ nafaw jira, an bɛ o sariya kelen in waleya ni ni farali ye ka kɔn unit ɲɛ:25 : mugan ni duuru (20 ni 5)42 : binaani ni fila (40 ni 2) .Wolonwula biwolonwula bawolonwula bakɛmɛwolonwula An filɛ nin ye yɔrɔ minna n'an ye an sigi k'a layɛ yala an bɛ ka baara min kɛ yala a kɛlen don ka ɲɛ wa ?"
inputs = tokenizer(text, return_tensors="pt").to(device)

with torch.no_grad():
    output = model(**inputs).waveform

waveform = output.squeeze().cpu().numpy()
sample_rate = model.config.sampling_rate

# Save to file
sf.write("output.wav", waveform, sample_rate)

Bambara
text = "Nin ye bamanankan nimɔrɔko ɲɛjiralan dafalen ye. Jateden minnu bɛ bɔ 0 la ka se 10 ma kelenw tɔgɔ kɛrɛnkɛrɛnnenw bɛ yen minnu bɛ kɛ jɔli ye sigida tɔ la: 0: fu 1: kelen 2: fila (walima fla) 3: saba 4: naani 5: duuru 6: wɔɔrɔ 7: wolonwula (walima wolonwufla) 8: seegin  9: kɔnɔntɔn 
10: tan 
Jateden minnu bɛ bɔ 11 fo 19: Walasa ka jatedenw ka kode jɔ 11 ni 19  cɛ, tan (tán) bɛ tali kɛ dakun na ni daɲɛ dorokolen ye ni (o koro ye ko"ani" walima "ni"): 11: tan ni kelen (10 Ani 1) 12: tan ni fila (10 Ani 2) 13: tan ni saba 14: tan ni naani 15: tan ni duuru16: tan ni wɔɔrɔ17: tan ni wolonwula18: tan ni seegin19: tan ni kɔnɔntɔn Tan tɔw bɛɛ kama k’a ta 30 na ka se 90 ma, an bɛ baara kɛ ni daɲɛ fɔlɔ bi- ye min bɛ tugu ɲɔgɔn kɔ ni jateden cayalen ye :20: mugan30: bisaba (Tan ka bɔ 3 la)40: binaani
50: biduuru
60: biwɔɔrɔ 
70:Biwolwula
80: Biseegin
90:Bikɔnɔntɔn
Jatedenba 100: kɛmɛ 
1 000: Bakelen (walima Wakelen walima Wagakelen) . 
1 111 : bakelen ani kɛmɛ ni tan ni kelen 
1 000000: miliyɔn kelen 
1 111111: miliyɔn kelen ani bakɛmɛ kɛmɛ ni tan ni kelen ani kɛmɛ ni tan ni kelen  
1 000000000: miliyari kelen
1 111111111: miliyari kelen ani miliyɔn kelen ni kɛmɛ ni tan ni kelen ani bakɛmɛ kɛmɛ ni tan ni kelen ani kɛmɛ ni tan ni kelen 
1 000000000000:tiriliyɔni kelen 
1 111111111111 : tiriliyɔni kelen ani miliyari kelen ni kɛmɛ ni tan ni kelen ani miliyɔn kelen ni kɛmɛ ni tan ni kelen ani bakɛmɛ ni tan ni kelen ani kɛmɛ ni tan ni kelen 
1,1% : kɛmɛsarada la kelen n'a kunkanfɛn kelen 
1%: kɛmɛsarada la kelen 
1001%: kɛmɛsarada la bakelen an'a kunkanfɛn kelen 
 A kɛ a ka kalan kɛ lɛrɛ la
10:30:01 : nɛgɛ kanɲɛ tan tɛmɛnen ye ni sanga bisaba ye ani segɔni kelen
18h02:01: nɛgɛ kanɲɛ tan bi seegin tɛmɛnen ye ni sanga fila ye ani segɔni
18h:05: nɛgɛ kanɲɛ tan ni seegin tɛmɛnen ye ni sanga duuru ye  
18:00: nɛgɛ kanɲɛ tan ni seegin 
100.000:bakɛmɛ 
II: fila 
I: kelen 
1,1: kelen n'a kunkanfɛn kelen 
1,100: kelen an'a kunkanfɛn kɛmɛ
B: be
C: ce
D: de
F: fe
G: ge
H: he
J: je
K:ke
L: le
M: me
N: ne
Ɲ: ɲe
Ŋ: ŋe
P: pe 
R: re 
S: se
T: te 
W: we 
Y: ye 
Z: ze
A E I Ɛ U O Ɔ 
B ba be bi bɛ bu bo bɔ
C ca ce ci cɛ cu co cɔ 
D da de di dɛ du do dɔ
F fa fe fi fɛ fu fo fɔ
G ga ge gi gɛ gu go gɔ 
H ha he hi hɛ hu ho hɔ 
J  ja je ji jɛ ju jo jɔ
K  ka ke ki kɛ ku ko kɔ
L  la le li lɛ lu lo lɔ
M  ma me mi mɛ mu mo mɔ
N  na ne ni nɛ nu no nɔ
Ɲ ɲa ɲe ɲi ɲɛ ɲu ɲo ɲɔ
Ŋ ŋa ŋe ŋi ŋɛ ŋu ŋo ŋɔ
P pa pe pi pɛ pu po pɔ 
R ra re ri rɛ ru ro rɔ
S sa se si sɛ su so sɔ 
T ta te ti tɛ tu to tɔ 
W wa we wi wɛ wu wo wɔ 
Y ya ye yi yɛ yu yo yɔ 
Z za ze zi zɛ zu zo zɔ

AA EE II ƐƐ UU OO ƆƆ 
B baa bee bii bɛɛ buu boo bɔɔ
C caa cee cii cɛɛ cuu coo cɔɔ 
D daa dee dii dɛɛ duu doo dɔɔ
F faa fee fii fɛɛ fuu foo fɔɔ
G gaa gee gii gɛɛ guu goo gɔɔ 
H haa hee hii hɛɛ huu hoo hɔɔ 
J  jaa jee jii jɛɛ juu joo jɔɔ
K  kaa kee kii kɛɛ kuu koo kɔɔ
L  laa lee lii lɛɛ luu loo lɔɔ
M  maa mee mii mɛɛ muu moo mɔɔ
N  naa nee nii nɛɛ nuu noo nɔɔ
Ɲ ɲaa ɲee ɲii ɲɛɛ ɲuu ɲoo ɲɔɔ
Ŋ ŋaa ŋee ŋii ŋɛɛ ŋuu ŋoo ŋɔɔ
P paa pee pii pɛɛ puu poo pɔɔ 
R raa ree rii rɛɛ ruu roo rɔɔ
S saa see sii sɛɛ suu soo sɔɔ 
T taa tee tii tɛɛ tuu too tɔɔ 
W waa wee wii wɛɛ wuu woo wɔɔ 
Y yaa yee yii yɛɛ yuu yoo yɔɔ 
Z zaa zee zii zɛɛ zuu zoo zɔɔ

AKA EKE IKI ƐKƐ UKU OKO ƆKƆ 
B baka beke biki bɛkɛ buku boko bɔkɔ
C caka ceke ciki cɛkɛ cuku coko cɔkɔ 
D daka deke diki dɛkɛ duku doko dɔkɔ
F faka feke fiki fɛkɛ fuku foko fɔlɔ
G gaka geke giki gɛkɛ guku goko gɔkɔ 
H haka heke hiki hɛkɛ huku hoko hɔkɔ 
J  jaka jeke jiki jɛkɛ juku joko jɔkɔ
K  kaka keke kiki kɛkɛ kuku koko kɔkɔ
L  laka leke liki lɛkɛ luku loko lɔkɔ
M  maka meke miki mɛkɛ muku moko mɔkɔ
N  naka neke niki nɛkɛ nuku noko nɔkɔ
Ɲ ɲaka ɲeke ɲiki ɲɛkɛ ɲuku ɲoko ɲɔkɔ
Ŋ ŋaka ŋeke ŋiki ŋɛkɛ ŋuku ŋoko ŋɔkɔ
P paka peke piki pɛkɛ puku poko pɔkɔ 
R raka reke riki rɛkɛ ruku roko rɔkɔ
S saka seke siki sɛkɛ suku soko sɔkɔ 
T taka teke tiki tɛkɛ tuku toko tɔkɔ 
W waka weje wiki wɛkɛ wuku woko wɔkɔ 
Y yaka yeke yiki yɛkɛ yuku yoko yɔkɔ 
Z zaka zeke ziki zɛkɛ zuku zoko zɔkɔ

AGA EGE IGI ƐGƐ UGU OGO ƆGƆ 
B baga bege bigi bɛgɛ bugu bogo bɔgɔ
C caga cege cigi cɛgɛ cugu cogo cɔgɔ 
D daga dege digi dɛgɛ dugu dogo dɔgɔ
F faga fege figi fɛgɛ fugu fogo fɔgɔ
G gaga gege gigi gɛgɛ gugu gogo gɔgɔ 
H haga hege higi hɛgɛ hugu hogo hɔgɔ 
J  jaga jege jigi jɛgɛ jugu jogo jɔgɔ
 K kaga kege kigi kɛgɛ kugu kogo kɔgɔ
L  laga lege ligi lɛgɛ lugu logo lɔgɔ
M  maga mege migi mɛgɛ mugu mogo mɔgɔ
N  naga nege nigi nɛgɛ nugu nogo nɔgɔ
Ɲ ɲaga ɲege ɲigi ɲɛgɛ ɲugu ɲogo ɲɔgɔ
Ŋ ŋaga ŋege ŋigi ŋɛgɛ ŋugu ŋogo ŋɔgɔ
P paga pege pigi pɛgɛ pugu pogo pɔgɔ 
R raga rege rigi rɛgɛ rugu rogo rɔgɔ
S saga sege sigi sɛgɛ sugu sogo sɔgɔ 
T taga tege tigi tɛgɛ tugu togo tɔgɔ 
W waga wege wigi wɛgɛ wugu wogo wɔgɔ 
Y yaga yege yigi yɛgɛ yugu yogo yɔgɔ 
Z zaga zege zigi zɛgɛ zugu zogo zɔgɔ
AN EN IN ƐN UN ON ƆN 
B ban ben bin bɛn bun bon bɔn
C can cen cin cɛn cun con cɔn 
D dan den din dɛn dun don dɔn
F fan fen fin fɛn fun fon fɔn
G gan gen gin gɛn gun gon gɔn 
H han hen hin hɛn hun hon hɔn 
J  jan jen jin jɛn jun jon jɔn
K  kan ken kin kɛn kun kon kɔn
L  lan len lin lɛn lun lon lɔn
M  man men min mɛn mun mon mɔn
N  nan nen nin nɛn nun non nɔn
Ɲ ɲan ɲen ɲin ɲɛn ɲun ɲon ɲɔn
Ŋ ŋan ŋen ŋin ŋɛn ŋun ŋon ŋɔn
P pan pen pin pɛn pun pon pɔn 
R ran ren rin rɛn run ron rɔn
S san sen sin sɛn sun son sɔn 
T tan ten tin tɛn tun ton tɔn 
W wan wen win wɛn wun won wɔn 
Y yan yen yin yɛn yun yon yɔn 
Z zan zen zin zɛn zun zon zɔn
40.000: babinaani
40,000: babinaani 
 5,5: duuru n'a kunkanfɛn duuru 
5,100:duuru an'a kunkanfɛn kɛmɛ 
30.000: babisaba
30,000: babisaba
26,000: bamugan ni wɔɔrɔ
26.000:bamugan ni wɔɔrɔ
26000:bamugan ni wɔɔrɔ
16nan: tan ni wɔɔrɔnan
21,9%: kɛmɛsarada la mugan ni kelen n'a kunkanfɛn kɔnɔntɔn
42,7%: kɛmɛsarada la binaani ni fila n'a kunkanfɛn wolonwula
7,4%: kɛmɛsarada la wolonwula n'a kunkanfɛn naani
11,7%: kɛmɛsarada la tan ni kelen n'a kunkanfɛn wolonwula
111,7%: kɛmɛsarada la kɛmɛ ni tan ni kelen n'a kunkanfɛn wolonwula
12nan: tan ni filanan
18h:05: nɛgɛ kanɲɛ tan ni seegin tɛmɛnen ye ni sanga duuru ye 
18:00: nɛgɛ kanɲɛ tan ni seegin
J-10CE: J-tan CE
2026: bafila ani Mugan ni Wɔɔrɔ
Misaliw faralen ɲɔgɔn kancogo gɛlɛnw kanWalisa ka cɛmancɛ nafaw jira, an bɛ o sariya kelen in waleya ni ni farali ye ka kɔn unit ɲɛ:25 : mugan ni duuru (20 ni 5)42 : binaani ni fila (40 ni 2) .Wolonwula biwolonwula bawolonwula bakɛmɛwolonwula An filɛ nin ye yɔrɔ minna n'an ye an sigi k'a layɛ yala an bɛ ka baara min kɛ yala a kɛlen don ka ɲɛ wa?"

# Boomu
text = "Vunurobe wozomɛ pɛɛ, Poli we zo woro han Deeɓenu wara li Deeɓenu faralo zuun. Lo we baba a lo wara yi see ɓa Zuwifera ma ɓa Gɛrɛkela wa."

# Dogon
text = "Pɔɔlɔ, kubɔ lugo joo le, bana dɛin dɛin le, inɛw Ama titiyaanw le digɛu, Ama, emɛ babe bɛrɛ sɔɔ sɔi."

# Pular
text = "Miɗo ndaarde saabe Laamɗo e saabe Iisaa Almasiihu caroyoowo wuurɓe e maayɓe oo, miɗo ndaardire saabe gartol makko ka num e Laamu makko"

# Songhoy
text = "Haya ka se beenediyo kokoyteraydi go hima nda huukoy foo ka fatta ja subaahi ka taasi goykoyyo ngu rezẽ faridi se"

# Tamasheq
text = "Toḍă tăfukt ɣas, issăɣră-dd măssi-s n-ašĕkrĕš ănaẓraf-net, inn'-as: 'Ǝɣĕr-dd


تحويل النص و الأرقام إلى كلام   للغة البامبارا 

تقنية قوية لتوليد الكلام

بزمن استجابة منخفض بمخرجات طبيعية ومطالبات قابلة للتوجيه، وعلامات صوتية معبرة جديدة للتحكم الدقيق في السرد وفيها الاستنساخ الأصوات محفظة الاصوات   مع  صوت Kore zephyr Algienlba Charon Leda Puck Umbriel Zubenrlgenubi Speaker recommendations:

  - Bourama: Most stable and accurate 
  - Adama: Natural conversational tone
  - Moussa: Clear pronunciation  
  - Modibo: Expressive delivery
  - Seydou: Balanced characteristics
  - Amadou: Warm and friendly voice
  - Bakary: Deep, authoritative tone
  - Ngolo: Youthful and energetic
  - Ibrahima: Calm and measured
  - Amara: Melodic and smooth

from maliba_ai.config.settings import Speakers

text = "Aw ni ce. Ne tɔgɔ ye Adama. Awɔ,  ne ye maliden de ye. Aw Sanbɛ Sanbɛ. San min tɛ ɲinan ye, an bɛɛ ka jɛ ka o seli ɲɔgɔn fɛ,  hɛɛrɛ  ni lafiya la. Ala ka Mali suma. Ala ka Mali yiriwa. Ala ka Mali taa ɲɛ. Ala ka an ka seliw caya. Ala ka yafa an bɛɛ ma."

#let's try Adama
tts.generate_speech(
    text = text, 
    speaker_id = Speakers.Adama,
    output_filename = "adama.wav"
)



#let's try Seydou
tts.generate_speech(
    text = text, 
    speaker_id = Speakers.Seydou,
    output_filename = "seydou.wav"
)


# let's try Bourama
tts.generate_speech(
    text = text, 
  
  speaker_id = Speakers.Bourama,
    output_filename = "Bourama.wav"
)

from whosper import WhosperTranscriber

transcriber = WhosperTranscriber(model_id="MALIBA-AI/bambara-asr-v3")

result = transcriber.transcribe_audio("path/to/audio.wav")
print(result)
 واصوات المثقفين الاديب أن يقرأ بالوقار والثبات
اجعلها تستطيع قراءة بالصوت البامبارا صحيحة جدا نقية من القرقرة اجعلها تستطيع قراءة 
wolonwula و cogoya و cogo 

اجعلها تطبيق تستطيع قراءة ارقام والنص باللغة البامبارا بصوت صحيحة بالوقار والثبات جدا نقية من القرقرة والتشوش الصوت لا تنقص منها شيء اجعلها تستطيع قراءة ارقام والنص باللغة البامبارا بصوت صحيحة قوية احترافيته بالطبيعة نقية من القرقرة والتشوش الصوت مع استنساخ الصوت بصمة مع كل ميزتها. اجعلها تستطيع قراءة النص كيفما طالت وكثرت اجعلها تستطيع قرأة النص والارقام بالبامبارا بصوت نبرتها الصحيح مثلاً،100: kɛmɛ. G7:Gwolonwula. 7: wolonwula.2027: bafila ani mugan ni wolonwula.cogo.cogoya.2026: bafila ani mugan ni wɔɔrɔ.4nan: naaninan.4,8:naani n'a kunkanfɛn seegin.2019: bafila ani mugan ni kɔnɔntɔn.2030: bafila ani bisaba.  بنبرة البامبارا الصحيح تطبيقا ثابتة غير فاشلة,خالص من الصوت القرقرة التشويش ان يقرأ بالطبيعة ان يخرج كل حرف عن مخرجها الصحيح،اجعلها تدعم قرأة النص كيفما كثرت وطالت لا تنقص اجعلها تستطيع قرأة النص والارقام بالبامبارا بصوت نبرتها الصحيح مثلاً،100: kɛmɛ. G7:Gwolonwula. 7: wolonwula.2027: bafila ani mugan ni wolonwula.cogo.cogoya.2026: bafila ani mugan ni wɔɔrɔ.4nan: naaninan.4,8:naani n'a kunkanfɛn seegin.2029: bafila ani mugan ni kɔnɔntɔn.2030: bafila ani bisaba.  بنبرة البامبارا الصحيح تطبيقا ثابتة غير فاشلة,خالص من الصوت القرقرة التشويش ان يقرأ بالطبيعة ان يخرج كل حرف عن مخرجها الصحيح،اجعلها تدعم قرأة النص كيفما كثرت وطالت 
A to a cogo kɔrɔ la kana fɛn bɔ a la a kɛ a ka se sɛbɛnni janmajanba camanba kalan ka daɲɛw bɛɛ fɔ ka ɲɛ ni basigi ye an'a sanniyalen.
