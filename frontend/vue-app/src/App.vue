
<template>
  <div id="app">
    <AudioRecorder />
    <SpeechRecognition />
  </div>
</template>

<script>
import AudioRecorder from './components/AudioRecorder.vue';
import SpeechRecognition from './components/SpeechRecognition.vue';
export default {
  components: {
    AudioRecorder,
    SpeechRecognition
  }
};
</script>
