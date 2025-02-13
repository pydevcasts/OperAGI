<template>
  <div>
    <h1>Record Audio</h1>
    <button @click="startRecording" :disabled="isRecording">Start Recording</button>
    <button @click="stopRecording" :disabled="!isRecording">Stop Recording</button>
    <audio v-if="audioUrl" :src="audioUrl" controls></audio>
    <div v-if="transcription">
      <h2>Transcription:</h2>
      <p>{{ transcription }}</p>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      isRecording: false,
      audioUrl: '',
      mediaRecorder: null as MediaRecorder | null,
      audioChunks: [] as Blob[],
      transcription: ''
    };
  },
  methods: {
    async startRecording() {
      // بررسی وجود navigator.mediaDevices.getUserMedia
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error('getUserMedia is not supported on this browser.');
        alert('Your browser does not support audio recording.');
        return;
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        this.audioChunks = [];

        this.mediaRecorder.ondataavailable = (event) => {
          this.audioChunks.push(event.data);
        };

        this.mediaRecorder.onstop = this.handleStopRecording;

        this.mediaRecorder.start();
        this.isRecording = true;
      } catch (error) {
        console.error('Error accessing audio devices:', error);
        alert('Could not access your microphone. Please check your permissions.');
      }
    },
    stopRecording() {
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
        this.isRecording = false;
      }
    },
    async handleStopRecording() {
      const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
      this.audioUrl = URL.createObjectURL(audioBlob);
      await this.sendAudioToServer(audioBlob);
    },
    async sendAudioToServer(audioBlob: Blob) {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');

      try {
        const response = await fetch('http://operagi.com:8000/api/transcribe/', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        this.transcription = data.transcription;
      } catch (error) {
        console.error('Error sending audio to server:', error);
      }
    }
  }
};
</script>

<style scoped>
h1 {
  font-size: 24px;
}
button {
  margin: 10px;
}
</style>