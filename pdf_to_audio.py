import openai
import PyPDF2
import os
from gtts import gTTS
from pydub import AudioSegment

# Função para extrair texto de um arquivo PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                # Remove quebras de linha do texto extraído
                text += page.extract_text().replace('-\n','').replace('‑\n','').replace('\n', ' ').replace('  ', ' ') + ' '
            return text
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None

# Função para particionar o texto no último ponto antes do limite de caracteres
def partition_text(text, max_length):
    partitions = []
    while len(text) > max_length:
        # Encontrar o último ". " antes do limite
        split_index = text.rfind(". ", 0, max_length)
        if split_index == -1:  # Caso não encontre ". ", particiona no limite
            split_index = max_length
        partitions.append(text[:split_index + 1].strip())  # Inclui o ponto final
        text = text[split_index + 1:].strip()
    if text:
        partitions.append(text)
    return partitions

# Função para ajustar a velocidade do áudio
#def change_audio_speed(input_audio_path, output_audio_path, speed=1.0):
#    try:
#        audio = AudioSegment.from_file(input_audio_path)
#        altered_audio = audio.speedup(playback_speed=speed)
#        altered_audio.export(output_audio_path, format="mp3")
#        print(f"Áudio ajustado salvo em: {output_audio_path}")
#    except Exception as e:
#        print(f"Erro ao ajustar a velocidade do áudio: {e}")

# Função para converter texto em áudio usando gTTS (ou qualquer API de voz desejada)
def text_to_audio(text, output_audio_path, speed=1.0):
    try:
        temp_audio_path = "temp_audio.mp3"
        tts = gTTS(text, lang='pt')  # Altere 'pt' para outro idioma, se necessário
        tts.save(temp_audio_path)
        audio = AudioSegment.from_mp3(temp_audio_path)
        audio.export(output_audio_path, format="ogg", codec="libopus")
#        if speed != 1.0:
#            change_audio_speed(temp_audio_path, output_audio_path, speed)
#        else:
#        os.rename(temp_audio_path, output_audio_path)
 
        print(f"Áudio salvo em: {output_audio_path}")
    except Exception as e:
        print(f"Erro ao converter texto em áudio: {e}")

# Caminho do arquivo PDF
def pdf_to_audio(pdf_path: str, output_audio_base_path: str):
    # Extraindo texto do PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    #pdf_text = "oi"
    os.makedirs(output_audio_base_path, exist_ok=True) 
    result = []

    if pdf_text:
        # Limitando o texto para evitar problemas de processamento em textos longos
        max_length = 5000  # Ajuste conforme necessário
        text_partitions = partition_text(pdf_text, max_length)

        # Convertendo as partes do texto em áudio
        for i, partition in enumerate(text_partitions):
            output_audio_path = f"{output_audio_base_path}parte_{i + 1}.ogg"
            text_to_audio(partition, output_audio_path, speed=1.0)        
            result.append(output_audio_path)
            #break
        return True, result
    else:
        return False, result

    