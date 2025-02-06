<template>
  <div>
    <h1>Speech Recognition</h1>
    <button @click="startRecording">Start Recording</button>
    <button @click="stopRecording" :disabled="!isRecording">Stop Recording</button>
    <p v-if="transcription">Transcription: {{ transcription }}</p>
    <p v-if="answer">Answer: {{ answer }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
      transcription: '',  // متن تبدیل‌شده
      answer: ''          // پاسخ از API
    };
  },
  methods: {
    async startRecording() {
      this.audioChunks = [];
      this.isRecording = true;

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      
      this.mediaRecorder.ondataavailable = event => {
        this.audioChunks.push(event.data);
      };

      this.mediaRecorder.start();
    },
    stopRecording() {
      this.mediaRecorder.stop();
      this.isRecording = false;

      this.mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        const wavBlob = await this.convertToWav(audioBlob);
        const formData = new FormData();
        formData.append('audio', wavBlob, 'audio.wav');

        try {
          const response = await axios.post('http://localhost:8000/api/transcribe/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          // ذخیره متن تبدیل‌شده در متغیر transcription
          this.transcription = response.data.transcription;

          // ارسال متن به API get_answer
          const answerResponse = await axios.post('http://localhost:8000/api/get_answer/', {
          question: this.transcription, // سوال شما
          detailed: true // فرض بر این است که این پارامتر برای درخواست توضیحات بیشتر استفاده می‌شود
          });

          // ذخیره پاسخ در متغیر answer
          this.answer = answerResponse.data.answer;
        } catch (error) {
          console.error('Error during API requests:', error);
          alert('An error occurred while processing your request. Please try again.');
        }
      };
    },
    async convertToWav(blob) {
      const arrayBuffer = await blob.arrayBuffer();
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
      const wavData = this.audioBufferToWav(audioBuffer);
      return new Blob([new Uint8Array(wavData)], { type: 'audio/wav' });
    },
    audioBufferToWav(buffer) {
      const numChannels = buffer.numberOfChannels;
      const sampleRate = buffer.sampleRate;
      const format = numChannels === 1 ? 1 : 2; // 1 for mono, 2 for stereo
      const byteLength = buffer.length * numChannels * 2 + 44; // 44 bytes for WAV header
      const wavArrayBuffer = new ArrayBuffer(byteLength);
      const view = new DataView(wavArrayBuffer);

      // Write WAV header
      this.writeString(view, 0, 'RIFF');
      view.setUint32(4, byteLength - 8, true);
      this.writeString(view, 8, 'WAVE');
      this.writeString(view, 12, 'fmt ');
      view.setUint32(16, 16, true);
      view.setUint16(20, format, true);
      view.setUint16(22, numChannels, true);
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, sampleRate * numChannels * 2, true);
      view.setUint16(32, numChannels * 2, true);
      view.setUint16(34, 16, true);
      this.writeString(view, 36, 'data');
      view.setUint32(40, byteLength - 44, true);

      // Write PCM samples
      const offset = 44;
      for (let i = 0; i < buffer.length; i++) {
        for (let channel = 0; channel < numChannels; channel++) {
          const sample = buffer.getChannelData(channel)[i];
          view.setInt16(offset + (i * numChannels + channel) * 2, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
        }
      }

      return new Uint8Array(wavArrayBuffer);
    },
    writeString(view, offset, string) {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    }
  }
};
</script>

<style scoped>
/* استایل‌های دلخواه */
</style>