<template>
    <div>
      <h1>Speech Recognition</h1>
      <div>
        <label for="audio-upload" class="microphone-icon">
          <i class="fas fa-microphone"></i> <!-- آیکون میکروفن -->
        </label>
        <input 
          id="audio-upload" 
          type="file" 
          accept="audio/*" 
          @change="handleFileUpload" 
          style="display: none;" 
        />
      </div>
      <p v-if="transcription">Transcription: {{ transcription }}</p>
      <p v-if="answer">Answer: {{ answer }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        transcription: '',  // متن تبدیل‌شده
        answer: ''          // پاسخ از API
      };
    },
    methods: {
      async handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
          const formData = new FormData();
          formData.append('audio', file);
  
          try {
            // ارسال فایل صوتی به API برای تبدیل به متن
            const response = await axios.post('http://localhost:8000/api/transcribe/', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            });
  
            // ذخیره متن تبدیل‌شده در متغیر transcription
            this.transcription = response.data.transcription;
  
            // ارسال متن به API get_answer
            const answerResponse = await axios.post('http://localhost:8000/api/get_answer/', {
              question: this.transcription // استفاده از متن تبدیل‌شده
            });
  
            // ذخیره پاسخ در متغیر answer
            this.answer = answerResponse.data.answer;
          } catch (error) {
            console.error('Error during API requests:', error);
            alert('An error occurred while processing your request. Please try again.');
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .microphone-icon {
    font-size: 2rem;
    cursor: pointer;
    color: #007bff; /* رنگ دلخواه برای آیکون */
  }
  .microphone-icon:hover {
    color: #0056b3; /* رنگ هنگام هاور */
  }
  </style>