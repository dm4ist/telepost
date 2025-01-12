<template>
    <div class="manage-channels">
      <h2>Manage Channels</h2>
      <form @submit.prevent="addChannel">
        <input v-model="newChannel.name" placeholder="Channel Name" required>
        <input v-model="newChannel.chat_id" placeholder="Chat ID" required>
        <input v-model="newChannel.bot_token" placeholder="Bot Token" required>
        <button type="submit">Add Channel</button>
      </form>
      <ul>
        <li v-for="channel in channels" :key="channel.id">
          {{ channel.name }} ({{ channel.chat_id }})
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ManageChannels',
    data() {
      return {
        channels: [],
        newChannel: {
          name: '',
          chat_id: '',
          bot_token: ''
        }
      }
    },
    async mounted() {
      try {
        const response = await axios.get('http://localhost:5000/api/channels');
        this.channels = response.data;
      } catch (error) {
        console.error('Error fetching channels:', error);
      }
    },
    methods: {
      async addChannel() {
        try {
          await axios.post('http://localhost:5000/api/channels', this.newChannel);
          this.channels.push(this.newChannel);
          this.newChannel = { name: '', chat_id: '', bot_token: '' };
        } catch (error) {
          console.error('Error adding channel:', error);
        }
      }
    }
  }
  </script>