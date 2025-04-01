<template>
  <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <div class="sidebar-header">
      <button class="new-chat-button" @click="$emit('new-chat')" :class="{ 'icon-only': isCollapsed }">
        <i class="fas fa-plus"></i>
        <span v-if="!isCollapsed">New Chat</span>
      </button>
      <button class="toggle-button" @click="toggleSidebar">
        <i :class="['fas', isCollapsed ? 'fa-circle-up' : 'fa-circle-down']"></i>
      </button>
    </div>
    <div class="chat-history">
      <div 
        v-for="(chat, index) in chatHistory" 
        :key="chat.id"
        class="history-item"
        :class="{ 
          'active': currentChatId === chat.id,
          'icon-only': isCollapsed 
        }"
      >
        <div class="history-item-content" @click="$emit('load-chat', chat.id)">
          <i class="fas fa-comment"></i>
          <span v-if="!isCollapsed">{{ chat.title }}</span>
          <div v-if="!isCollapsed" class="chat-date">{{ formatDate(chat.date) }}</div>
        </div>
        <button 
          v-if="!isCollapsed" 
          class="delete-chat" 
          @click.stop="confirmDeleteChat(chat.id)"
          title="Delete Chat"
        >
          <i class="fas fa-circle-xmark"></i>
        </button>
      </div>
    </div>
    <div class="sidebar-footer">
      <div class="user-profile" @click="$emit('toggle-user-menu')" :class="{ 'icon-only': isCollapsed }">
        <img :src="userAvatar" alt="User Avatar" class="avatar" />
        <span v-if="!isCollapsed">{{ userName }}</span>
        <i v-if="!isCollapsed" class="fas fa-circle-user"></i>
      </div>
      
      <!-- User Menu -->
      <div v-if="showUserMenu && !isCollapsed" class="user-menu">
        <div class="menu-item" @click="$emit('open-profile-settings')">
          <i class="fas fa-user-cog"></i>
          <span>Profile Settings</span>
        </div>
        <div class="menu-item" @click="$emit('open-preferences')">
          <i class="fas fa-cog"></i>
          <span>Preferences</span>
        </div>
        <div class="menu-item danger" @click="$emit('clear-history')">
          <i class="fas fa-circle-xmark"></i>
          <span>Clear All History</span>
        </div>
        <div class="menu-item" @click="$emit('logout')">
          <i class="fas fa-sign-out-alt"></i>
          <span>Logout</span>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="delete-modal">
      <div class="delete-modal-content">
        <h3>Delete Chat</h3>
        <p>Are you sure you want to delete this chat?</p>
        <div class="delete-modal-actions">
          <button class="cancel-button" @click="showDeleteModal = false">Cancel</button>
          <button class="delete-button" @click="handleDeleteConfirm">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
interface ChatHistory {
  id: number;
  title: string;
  date: Date;
  messages: Array<{text: string, type: 'user' | 'assistant'}>;
}

export default {
  props: {
    chatHistory: {
      type: Array as () => ChatHistory[],
      required: true
    },
    currentChatId: {
      type: Number,
      default: null
    },
    showUserMenu: {
      type: Boolean,
      default: false
    },
    userAvatar: {
      type: String,
      required: true
    },
    userName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isCollapsed: false,
      showDeleteModal: false,
      chatToDelete: null as number | null
    };
  },
  methods: {
    formatDate(date: Date) {
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
      this.$emit('sidebar-toggle', this.isCollapsed);
    },
    confirmDeleteChat(chatId: number) {
      this.chatToDelete = chatId;
      this.showDeleteModal = true;
    },
    handleDeleteConfirm() {
      if (this.chatToDelete) {
        this.$emit('delete-chat', this.chatToDelete);
        this.showDeleteModal = false;
        this.chatToDelete = null;
      }
    }
  }
};
</script>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background-color: #202123;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #4d4d4f;
  transition: width 0.3s ease;
  position: relative;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 12px;
  border-bottom: 1px solid #4d4d4f;
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.new-chat-button {
  flex: 1;
  padding: 12px;
  background-color: #343541;
  border: 1px solid #565869;
  border-radius: 6px;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  justify-content: center;
}

.new-chat-button.icon-only {
  padding: 8px;
}

.new-chat-button.icon-only span {
  display: none;
}

.toggle-button {
  padding: 8px;
  background-color: #343541;
  border: 1px solid #565869;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.toggle-button:hover {
  background-color: #40414f;
}

.history-item {
  position: relative;
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  color: #fff;
  gap: 8px;
  border-radius: 6px;
  margin: 4px 8px;
  transition: all 0.2s;
}

.history-item-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.history-item.icon-only .history-item-content {
  justify-content: center;
}

.history-item:hover {
  background-color: #343541;
}

.history-item.active {
  background-color: #343541;
}

.chat-date {
  font-size: 12px;
  color: #8e8ea0;
  margin-left: auto;
}

.delete-chat {
  opacity: 0;
  background: none;
  border: none;
  color: #ff4444;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.history-item:hover .delete-chat {
  opacity: 1;
}

.delete-chat:hover {
  background-color: rgba(255, 68, 68, 0.1);
}

/* Delete Modal Styles */
.delete-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.delete-modal-content {
  background-color: #343541;
  padding: 24px;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
}

.delete-modal-content h3 {
  margin: 0 0 16px 0;
  color: #fff;
}

.delete-modal-content p {
  margin: 0 0 24px 0;
  color: #8e8ea0;
}

.delete-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.delete-modal-actions button {
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s;
}

.cancel-button {
  background-color: #40414f;
  color: #fff;
}

.cancel-button:hover {
  background-color: #4a4b5a;
}

.delete-button {
  background-color: #ff4444;
  color: #fff;
}

.delete-button:hover {
  background-color: #ff5555;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 100;
    transform: translateX(0);
  }

  .sidebar.collapsed {
    transform: translateX(-100%);
  }

  .toggle-button {
    position: absolute;
    right: -40px;
    top: 12px;
    background-color: #202123;
    border-radius: 0 6px 6px 0;
    border-left: none;
  }
}

.sidebar-footer {
  margin-top: auto;
  padding: 12px;
  border-top: 1px solid #4d4d4f;
  position: relative;
  flex-shrink: 0;
  background-color: #202123;
  width: 100%;
  bottom: 0;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: #343541;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-menu {
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  background-color: #202123;
  border: 1px solid #4d4d4f;
  border-radius: 6px;
  margin: 8px;
  overflow: hidden;
}

.menu-item {
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #fff;
}

.menu-item:hover {
  background-color: #343541;
}

.menu-item i {
  width: 20px;
  text-align: center;
}

.menu-item.danger {
  color: #ff4444;
}

.menu-item.danger i {
  color: #ff4444;
}

.menu-item.danger:hover {
  background-color: rgba(255, 68, 68, 0.1);
}

/* اضافه کردن استایل اسکرول‌بار برای chat-history */
.chat-history::-webkit-scrollbar {
  width: 6px;
}

.chat-history::-webkit-scrollbar-track {
  background: transparent;
}

.chat-history::-webkit-scrollbar-thumb {
  background: #4d4d4f;
  border-radius: 3px;
}

.chat-history::-webkit-scrollbar-thumb:hover {
  background: #565869;
}
</style> 