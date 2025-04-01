<template>
  <div class="chat-messages" ref="messagesContainer">
    <div v-for="(message, index) in messages" :key="index" 
         :class="['message', message.type === 'user' ? 'user-message' : 'assistant-message']">
      <div class="message-content">
        <div class="message-text">{{ message.text }}</div>
      </div>
      <div class="message-avatar">
        <i :class="message.type === 'user' ? 'fas fa-user' : 'fas fa-robot'"></i>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
interface Message {
  text: string;
  type: 'user' | 'assistant';
}

export default {
  props: {
    messages: {
      type: Array as () => Message[],
      required: true
    }
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer as HTMLElement;
        container.scrollTop = container.scrollHeight;
      });
    }
  },
  watch: {
    messages: {
      handler() {
        this.scrollToBottom();
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 100%;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  max-width: 80%;
  width: fit-content;
}

.user-message {
  align-self: flex-end;
  background-color: #444654;
}

.assistant-message {
  align-self: flex-start;
}

.message-content {
  padding: 12px;
  border-radius: 8px;
  background-color: #444654;
  word-break: break-word;
}

.message-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #10a37f;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.assistant-message .message-avatar {
  background-color: #444654;
}

.message-avatar i {
  color: white;
  font-size: 16px;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #343541;
}

::-webkit-scrollbar-thumb {
  background: #565869;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #676980;
}
</style> 