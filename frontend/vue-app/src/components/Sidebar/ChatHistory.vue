<template>
  <div class="chat-history">
    <div 
      v-for="chat in chats" 
      :key="chat.id"
      class="history-item"
      :class="{ 'active': currentChatId === chat.id }"
      @click="$emit('selectChat', chat.id)"
    >
      <i class="fas fa-comment"></i>
      <span>{{ chat.title }}</span>
      <div class="chat-date">{{ formatDate(chat.date) }}</div>
    </div>
  </div>
</template>

<script lang="ts">
interface Chat {
  id: number;
  title: string;
  date: Date;
  messages: Array<{ text: string; type: 'user' | 'assistant' }>;
}

export default {
  props: {
    chats: {
      type: Array as () => Chat[],
      required: true
    },
    currentChatId: {
      type: Number,
      default: null
    }
  },
  emits: ['selectChat'],
  methods: {
    formatDate(date: Date) {
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    }
  }
};
</script>

<style scoped>
.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.history-item {
  position: relative;
  padding: 12px 40px 12px 12px;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 6px;
}

.history-item:hover {
  background-color: #343541;
}

.history-item.active {
  background-color: #343541;
}

.history-item i {
  font-size: 16px;
  color: #8e8ea0;
}

.chat-date {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: #8e8ea0;
}
</style> 