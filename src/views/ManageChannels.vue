<template>
  <div class="manage-channels">
    <h2>Manage Channels</h2>
    <form @submit.prevent="addChannel">
      <div>
        <label for="name">Channel Name:</label>
        <input type="text" v-model="newChannel.name" required>
      </div>
      <div>
        <label for="chat_id">Channel ID:</label>
        <input type="text" v-model="newChannel.chat_id" required>
      </div>
      <div>
        <label for="bot_token">Bot Token:</label>
        <input type="text" v-model="newChannel.bot_token" required>
      </div>
      <button type="submit">Add Channel</button>
    </form>
    <ul>
      <li v-for="channel in channels" :key="channel.id">
        {{ channel.name }}
        <button @click="editChannel(channel.id)">Edit</button>
        <button @click="deleteChannel(channel.id)">Delete</button>
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
    };
  },
  async mounted() {
    await this.fetchChannels();
  },
  methods: {
    async fetchChannels() {
      try {
        const response = await axios.get('http://localhost:5000/api/channels');
        this.channels = response.data;
      } catch (error) {
        console.error('Error fetching channels:', error);
      }
    },
    async addChannel() {
      try {
        const response = await axios.post('http://localhost:5000/api/channels', this.newChannel);
        this.channels.push(response.data);
        this.newChannel.name = '';
        this.newChannel.chat_id = '';
        this.newChannel.bot_token = '';
      } catch (error) {
        console.error('Error adding channel:', error);
      }
    },
    editChannel(channelId) {
      this.$router.push(`/channels/edit/${channelId}`);
    },
    async deleteChannel(channelId) {
      try {
        await axios.delete(`http://localhost:5000/api/channels/${channelId}`);
        this.channels = this.channels.filter(channel => channel.id !== channelId);
      } catch (error) {
        console.error('Error deleting channel:', error);
      }
    }
  }
};
</script>