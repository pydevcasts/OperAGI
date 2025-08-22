<template>
  <div class="user-menu" v-if="show">
    <div class="menu-item" @click="$emit('openProfile')">
      <i class="fas fa-user-cog"></i>
      <span>Profile Settings</span>
    </div>
    <div class="menu-item" @click="$emit('openPreferences')">
      <i class="fas fa-cog"></i>
      <span>Preferences</span>
    </div>
    <div class="menu-item danger" @click="$emit('clearHistory')">
      <i class="fas fa-circle-xmark"></i>
      <span>Clear History</span>
    </div>
    <div class="menu-item" @click="$emit('logout')">
      <i class="fas fa-sign-out-alt"></i>
      <span>Logout</span>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  emits: ['openProfile', 'openPreferences', 'clearHistory', 'logout']
};
</script>

<style scoped>
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
</style> 