<template>
    <div class="edit-channel">
      <h2>Edit Channel</h2>
      <form v-if="channelLoaded" @submit.prevent="updateChannel">
        <div>
          <label for="name">Channel Name:</label>
          <input type="text" v-model="channel.name" required>
        </div>
        <div>
          <label for="chat_id">Channel ID:</label>
          <input type="text" v-model="channel.chat_id" required>
        </div>
        <div>
          <label for="bot_token">Bot Token:</label>
          <input type="text" v-model="channel.bot_token" required>
        </div>
        <button type="submit">Save Changes</button>
      </form>
      <div v-else>
        Loading...
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'EditChannel',
    data() {
      return {
        channel: {
          name: '',
          chat_id: '',
          bot_token: ''
        },
        channelLoaded: false
      };
    },
    async created() {
      const channelId = this.$route.params.id;
      try {
        const response = await axios.get(`http://localhost:5000/api/channels/${channelId}`);
        this.channel = response.data;
        this.channelLoaded = true;
      } catch (error) {
        console.error('Error fetching channel data:', error);
      }
    },
    methods: {
      async updateChannel() {
        const channelId = this.$route.params.id;
        try {
          await axios.put(`http://localhost:5000/api/channels/${channelId}`, this.channel);
          this.$router.push('/channels');
        } catch (error) {
          console.error('Error updating channel:', error);
        }
      }
    }
  };
  </script>