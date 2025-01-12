<template>
  <div class="create-post">
    <h2>Create New Post</h2>
    <form @submit.prevent="schedulePost">
      <select v-model="selectedTemplate" @change="loadTemplate" required>
        <option value="">Select a template</option>
        <option v-for="template in templates" :key="template.id" :value="template.id">
          {{ template.name }}
        </option>
      </select>
      <div v-if="selectedTemplate">
        <div v-if="currentTemplate && currentTemplate.fields">
          <div v-for="field in currentTemplate.fields" :key="field.name">
            <label>{{ field.name }}</label>
            <input v-if="field.type === 'text'" v-model="postContent[field.name]" :placeholder="field.name">
            <input v-if="field.type === 'media'" type="file" @change="handleFileUpload($event, field.name)">
            <input v-if="field.type === 'link'" v-model="postContent[field.name]" placeholder="Enter URL">
          </div>
        </div>
      </div>
      <select v-model="selectedChannel" required>
        <option value="">Select a channel</option>
        <option v-for="channel in channels" :key="channel.id" :value="channel.id">
          {{ channel.name }}
        </option>
      </select>
      <input type="datetime-local" v-model="scheduledTime" required>
      <div>
        <button type="submit">Schedule Post</button>
        <button type="button" @click="publishPost">Publish Now</button>
      </div>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="success" class="success">{{ success }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreatePost',
  data() {
    return {
      templates: [],
      channels: [],
      selectedTemplate: '',
      selectedChannel: '',
      currentTemplate: null,
      postContent: {
        text: ''  // Ensure 'text' field is included
      },
      scheduledTime: '',
      error: null,
      success: null
    }
  },
  async mounted() {
    try {
      const [templatesResponse, channelsResponse] = await Promise.all([
        axios.get('http://localhost:5000/api/templates'),
        axios.get('http://localhost:5000/api/channels')
      ]);
      this.templates = templatesResponse.data;
      this.channels = channelsResponse.data;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  },
  methods: {
    loadTemplate() {
      this.currentTemplate = this.templates.find(t => t.id === this.selectedTemplate);
      this.postContent = { text: '' };  // Reset postContent and include 'text' field
    },
    handleFileUpload(event, fieldName) {
      const file = event.target.files[0];
      this.postContent[fieldName] = {
        type: file.type.split('/')[0],
        file: file
      };
    },
    async schedulePost() {
      this.error = null;
      this.success = null;
      try {
        const formData = {
          channel_id: this.selectedChannel,
          template_id: this.selectedTemplate,
          content: this.postContent,
          scheduled_time: this.scheduledTime
        };

        await axios.post('http://localhost:5000/api/posts', formData, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        this.success = 'Post scheduled successfully';
        this.$router.push('/posts');
      } catch (error) {
        if (error.response && error.response.data) {
          this.error = error.response.data.error;
        } else {
          this.error = error.message;
        }
      }
    },
    async publishPost() {
      this.error = null;
      this.success = null;
      try {
        const formData = {
          channel_id: this.selectedChannel,
          template_id: this.selectedTemplate,
          content: this.postContent
        };

        await axios.post('http://localhost:5000/api/posts', formData, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        this.success = 'Post published successfully';
        this.$router.push('/posts');
      } catch (error) {
        if (error.response && error.response.data) {
          this.error = error.response.data.error;
        } else {
          this.error = error.message;
        }
      }
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
}
.success {
  color: green;
}
</style>