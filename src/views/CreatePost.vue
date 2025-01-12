<template>
  <div class="create-post">
    <h2>Create New Post</h2>
    <form @submit.prevent="createPost">
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
      <button type="submit">Schedule Post</button>
    </form>
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
      postContent: {},
      scheduledTime: ''
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
      this.postContent = {};
    },
    handleFileUpload(event, fieldName) {
      const file = event.target.files[0];
      this.postContent[fieldName] = {
        type: file.type.split('/')[0],
        file: file
      };
    },
    async createPost() {
      try {
        const formData = new FormData();
        for (const [key, value] of Object.entries(this.postContent)) {
          if (value && value.file) {
            formData.append(key, value.file);
          } else {
            formData.append(key, value);
          }
        }
        formData.append('channel_id', this.selectedChannel);
        formData.append('template_id', this.selectedTemplate);
        formData.append('scheduled_time', this.scheduledTime);

        await axios.post('http://localhost:5000/api/posts', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.$router.push('/posts');
      } catch (error) {
        console.error('Error creating post:', error);
      }
    }
  }
}
</script>