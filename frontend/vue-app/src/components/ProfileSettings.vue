<template>
  <div v-if="show" class="modal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Profile Settings</h2>
        <button class="close-button" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Profile Picture</label>
          <div class="avatar-upload">
            <img :src="avatar" alt="Current Avatar" />
            <button class="upload-button" @click="handleAvatarUpload">
              <i class="fas fa-camera"></i>
              Change
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>Username</label>
          <input 
            type="text" 
            :value="localUsername" 
            @input="localUsername = ($event.target as HTMLInputElement).value"
            placeholder="Enter your username" 
          />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input 
            type="email" 
            :value="localEmail" 
            @input="localEmail = ($event.target as HTMLInputElement).value"
            placeholder="Enter your email" 
          />
        </div>
        <div class="form-group">
          <label>Bio</label>
          <textarea 
            :value="localBio" 
            @input="localBio = ($event.target as HTMLInputElement).value"
            placeholder="Tell us about yourself"
          ></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="cancel-button" @click="$emit('close')">Cancel</button>
        <button class="save-button" @click="handleSave">Save Changes</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    show: {
      type: Boolean,
      required: true
    },
    avatar: {
      type: String,
      required: true
    },
    username: {
      type: String,
      required: true
    },
    email: {
      type: String,
      required: true
    },
    bio: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      localUsername: this.username,
      localEmail: this.email,
      localBio: this.bio
    };
  },
  watch: {
    username(newValue: string) {
      this.localUsername = newValue;
    },
    email(newValue: string) {
      this.localEmail = newValue;
    },
    bio(newValue: string) {
      this.localBio = newValue;
    }
  },
  methods: {
    handleAvatarUpload() {
      // Implement avatar upload logic
      this.$emit('avatar-upload');
    },
    handleSave() {
      this.$emit('save', {
        username: this.localUsername,
        email: this.localEmail,
        bio: this.localBio
      });
    }
  }
};
</script>

<style scoped>
.modal {
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

.modal-content {
  background-color: #343541;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #4d4d4f;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  color: #fff;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #8e8ea0;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  background-color: #40414f;
  border: 1px solid #565869;
  border-radius: 6px;
  color: #fff;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-upload img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
}

.upload-button {
  padding: 8px 16px;
  background-color: #10a37f;
  border-radius: 6px;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s;
}

.upload-button:hover {
  background-color: #0d8a6c;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #4d4d4f;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-button,
.save-button {
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

.save-button {
  background-color: #10a37f;
  color: #fff;
}

.save-button:hover {
  background-color: #0d8a6c;
}

.close-button {
  background: none;
  border: none;
  color: #8e8ea0;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.close-button:hover {
  background-color: #40414f;
}
</style> 