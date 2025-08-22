<template>
  <div class="app-container">
    <ChatSidebar
      :chat-history="chatHistory"
      :current-chat-id="currentChatId"
      :show-user-menu="showUserMenu"
      :user-avatar="userAvatar"
      :user-name="userName"
      @new-chat="startNewChat"
      @load-chat="loadChat"
      @toggle-user-menu="toggleUserMenu"
      @open-profile-settings="openProfileSettings"
      @open-preferences="openPreferences"
      @clear-history="clearHistory"
      @delete-chat="deleteChat"
      @sidebar-toggle="handleSidebarToggle"
      @logout="logout"
    />

    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <div class="chat-container">
        <ChatMessages :messages="messages" />
        <ChatInput
          :is-loading="isLoading"
          @send="handleSend"
          @audio-recorded="handleAudioRecorded"
          @file-uploaded="handleFileUploaded"
        />
      </div>
    </div>

    <ProfileSettings
      :show="showProfileSettings"
      :avatar="userAvatar"
      :username="userName"
      :email="userEmail"
      :bio="userBio"
      @close="closeProfileSettings"
      @save="saveProfileSettings"
      @avatar-upload="handleAvatarUpload"
    />
  </div>
</template>

<script lang="ts">
import ChatSidebar from './ChatSidebar.vue';
import ChatMessages from './ChatMessages.vue';
import ChatInput from './ChatInput.vue';
import ProfileSettings from './ProfileSettings.vue';

interface Message {
  text: string;
  type: 'user' | 'assistant';
  response?: string;
}

interface ChatHistory {
  id: number;
  title: string;
  date: Date;
  messages: Message[];
}

export default {
  components: {
    ChatSidebar,
    ChatMessages,
    ChatInput,
    ProfileSettings
  },
  data() {
    return {
      messages: [] as Message[],
      currentChatId: undefined as number | undefined,
      showUserMenu: false,
      showProfileSettings: false,
      isSidebarCollapsed: false,
      userAvatar: 'https://via.placeholder.com/150',
      userName: 'John Doe',
      userEmail: 'john@example.com',
      userBio: '',
      chatHistory: [] as ChatHistory[],
      isLoading: false,
    };
  },
  methods: {
    handleSend(data: { text: string; response: string }) {
      const userMessage: Message = { 
    text: data.text, 
    type: 'user' 
  };
  
  this.messages = [...this.messages, userMessage];

    // افزودن پاسخ مدل
    const assistantMessage: Message = {
    text: data.response,
    type: 'assistant'
  };
  this.messages = [...this.messages, assistantMessage];
  
  if (this.currentChatId) {
    const chatIndex = this.chatHistory.findIndex(c => c.id === this.currentChatId);
    if (chatIndex !== -1) {
      const updatedChat = { 
        ...this.chatHistory[chatIndex],
        messages: [...this.chatHistory[chatIndex].messages, userMessage, assistantMessage],
        title: data.text.slice(0, 30) + (data.text.length > 30 ? '...' : '')
      };
      this.chatHistory = [
        ...this.chatHistory.slice(0, chatIndex),
        updatedChat,
        ...this.chatHistory.slice(chatIndex + 1)
      ];
    }
  }
},
    async handleAudioRecorded(audioBlob: Blob) {
      await this.sendAudioToServer(audioBlob);
    },
    async handleFileUploaded(file: File) {
      await this.sendAudioToServer(file);
    },
    async sendAudioToServer(audioBlob: Blob) {
      this.isLoading = true;
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');

      try {
        const response = await fetch('http://127.0.0.1:8000/api/transcribe/', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();
        const message: Message = { text: data.transcription, type: 'user' };
        this.messages = [...this.messages, message];
        
        if (this.currentChatId) {
          const chatIndex = this.chatHistory.findIndex(c => c.id === this.currentChatId);
          if (chatIndex !== -1) {
            const updatedChat = {
              ...this.chatHistory[chatIndex],
              messages: [...this.chatHistory[chatIndex].messages, message],
              title: data.transcription.slice(0, 30) + (data.transcription.length > 30 ? '...' : '')
            };
            this.chatHistory = [
              ...this.chatHistory.slice(0, chatIndex),
              updatedChat,
              ...this.chatHistory.slice(chatIndex + 1)
            ];
          }
        }
      } catch (error) {
        console.error('Error sending audio to server:', error);
        alert('Error sending audio file to server. Please try again.');
      } finally {
        this.isLoading = false;
      }
    },
    startNewChat() {
      const newChat: ChatHistory = {
        id: this.chatHistory.length + 1,
        title: 'New Chat',
        date: new Date(),
        messages: []
      };
      this.chatHistory = [newChat, ...this.chatHistory];
      this.currentChatId = newChat.id;
      this.messages = [];
    },
    loadChat(chatId: number) {
      this.currentChatId = chatId;
      const chat = this.chatHistory.find(c => c.id === chatId);
      if (chat) {
        this.messages = [...chat.messages];
      }
    },
    deleteChat(chatId: number) {
      const chatIndex = this.chatHistory.findIndex(c => c.id === chatId);
      if (chatIndex !== -1) {
        this.chatHistory = [
          ...this.chatHistory.slice(0, chatIndex),
          ...this.chatHistory.slice(chatIndex + 1)
        ];
        
        if (this.currentChatId === chatId) {
          this.currentChatId = this.chatHistory.length > 0 ? this.chatHistory[0].id : undefined;
          this.messages = this.currentChatId ? [...this.chatHistory[0].messages] : [];
        }
      }
    },
    handleSidebarToggle(isCollapsed: boolean) {
      this.isSidebarCollapsed = isCollapsed;
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    openProfileSettings() {
      this.showProfileSettings = true;
      this.showUserMenu = false;
    },
    closeProfileSettings() {
      this.showProfileSettings = false;
    },
    saveProfileSettings(settings: { username: string; email: string; bio: string }) {
      this.userName = settings.username;
      this.userEmail = settings.email;
      this.userBio = settings.bio;
      this.showProfileSettings = false;
    },
    handleAvatarUpload() {
      // Implement avatar upload logic
      console.log('Avatar upload clicked');
    },
    openPreferences() {
      // Implement preferences logic
      console.log('Preferences clicked');
    },
    clearHistory() {
      if (confirm('Are you sure you want to clear all chat history?')) {
        this.chatHistory = [];
        this.messages = [];
        this.currentChatId = undefined;
        this.startNewChat();
      }
    },
    logout() {
      // Implement logout logic
      this.showUserMenu = false;
    }
  },
  mounted() {
    // Load Font Awesome
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
    document.head.appendChild(link);

    // Start with a new chat
    this.startNewChat();
  }
};
</script>

<style scoped>
.app-container {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  display: flex;
  background-color: #343541;
}

.main-content {
  flex: 1;
  height: 100vh;
  overflow: hidden;
  transition: margin-left 0.3s ease;
}

.main-content.sidebar-collapsed {
  margin-left: -200px;
}

@media (max-width: 768px) {
  .main-content.sidebar-collapsed {
    margin-left: 0;
  }
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background-color: #343541;
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
}

/* Global styles */
:global(body) {
  margin: 0;
  padding: 0;
  overflow: hidden;
}

:global(#app) {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
}

/* Fix for Font Awesome icons */
:global(.fas) {
  font-family: 'Font Awesome 6 Free';
  font-weight: 900;
}

:global(.far) {
  font-family: 'Font Awesome 6 Free';
  font-weight: 400;
}

:global(.fab) {
  font-family: 'Font Awesome 6 Brands';
  font-weight: 400;
}
</style>