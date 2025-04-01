<template>
  <div class="chat-input-container">
    <div class="input-wrapper">
      <textarea
        v-model="message"
        placeholder="Type your message..."
        @keydown.enter.prevent="sendMessage"
        :disabled="isDisabled"
      ></textarea>
      
      <div class="action-buttons">
        <button 
          class="upload-button" 
          @click="triggerFileUpload"
          :disabled="isDisabled"
          :class="{ 'disabled': isDisabled }"
        >
          <i class="fas fa-file"></i>
        </button>
        
        <button 
          class="record-button" 
          @click="toggleRecording"
          :disabled="isDisabled"
          :class="{ 
            'recording': isRecording,
            'disabled': isDisabled 
          }"
        >
          <i class="fas fa-circle-play"></i>
          <span v-if="isRecording" class="recording-pulse"></span>
        </button>

        <button 
          class="send-button" 
          @click="sendMessage"
          :disabled="!message.trim() || isDisabled"
          :class="{ 'disabled': !message.trim() || isDisabled }"
        >
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
    
    <div v-if="isDisabled" class="loading-indicator">
      <div class="loading-spinner"></div>
      <span>Processing your message...</span>
    </div>

    <input
      type="file"
      ref="fileInput"
      style="display: none"
      @change="handleFileUpload"
      accept="audio/*,video/*,image/*"
    >
  </div>
</template>
<script lang="ts">
import axios from 'axios';

export default {
  props: {
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      message: '',
      isRecording: false,
      mediaRecorder: null as MediaRecorder | null,
      audioChunks: [] as BlobPart[],
      localLoading: false
    };
  },
  computed: {
    isDisabled() {
      return this.isLoading || this.localLoading;
    }
  },
  methods: {
    async sendMessage() {
      if (this.message.trim()) {
        try {
          this.localLoading = true;
          
          // ارسال درخواست به API
          const response = await axios.post('http://127.0.0.1:8000/api/chat/', {
            text: this.message
          });
          
          // ارسال پاسخ به کامپوننت والد
          this.$emit('send', {
            text: this.message,
            response: response.data.response
          });
          
          this.message = '';
        } catch (error) {
          console.error('Error sending message:', error);
          alert('Error getting response from AI. Please try again.');
        } finally {
          this.localLoading = false;
        }
      }
    },
    triggerFileUpload() {
      (this.$refs.fileInput as HTMLInputElement).click();
    },
    handleFileUpload(event: Event) {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (file) {
        this.$emit('file-uploaded', file);
      }
    },
    async toggleRecording() {
      if (this.isRecording) {
        this.stopRecording();
      } else {
        await this.startRecording();
      }
    },
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        this.audioChunks = [];

        this.mediaRecorder.addEventListener('dataavailable', (event) => {
          this.audioChunks.push(event.data);
        });

        this.mediaRecorder.addEventListener('stop', () => {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
          this.$emit('audio-recorded', audioBlob);
          this.isRecording = false;
          stream.getTracks().forEach(track => track.stop());
        });

        this.mediaRecorder.start();
        this.isRecording = true;
      } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Error accessing microphone. Please check your permissions.');
      }
    },
    stopRecording() {
      if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop();
      }
    }
  }
};
</script>

<style scoped>
.chat-input-container {
  padding: 20px;
  background-color: #343541;
  border-top: 1px solid #565869;
  width: 100%;
}

.input-wrapper {
  position: relative;
  display: flex;
  gap: 10px;
  align-items: flex-end;
  background-color: #40414f;
  border-radius: 12px;
  padding: 8px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

textarea {
  flex: 1;
  min-height: 40px;
  max-height: 120px;
  padding: 10px;
  padding-right: 90px;
  border-radius: 8px;
  border: 1px solid #565869;
  background-color: #40414f;
  color: #fff;
  resize: none;
  font-size: 14px;
  line-height: 1.4;
}

textarea:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.action-buttons {
  display: flex;
  gap: 12px;
  position: absolute;
  right: 10px;
  bottom: 25px;
}

button {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  min-height: 36px;
}

button i {
  font-size: 18px;
}

button:hover:not(.disabled) {
  background-color: #565869;
}

.disabled {
  opacity: 0.5;
  cursor: not-allowed !important;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 8px;
  background-color: rgba(52, 53, 65, 0.9);
  border-radius: 8px;
  margin-top: 8px;
  color: #fff;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.recording-pulse {
  position: absolute;
  width: 12px;
  height: 12px;
  background-color: #ff4444;
  border-radius: 50%;
  right: 0;
  top: 0;
  animation: pulse 1.5s ease infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.5);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.record-button.recording {
  color: #ff4444;
  position: relative;
}

.file-upload {
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}

.file-upload i {
  font-size: 18px;
}

.file-upload:hover {
  background-color: #565869;
}

.hidden {
  display: none;
}
</style> 