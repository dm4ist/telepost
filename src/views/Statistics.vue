<template>
    <div class="statistics">
      <h2>Post Statistics</h2>
      <div v-if="stats">
        <p>Total Posts: {{ stats.total_posts }}</p>
        <p>Total Views: {{ stats.total_views }}</p>
        <p>Average Views per Post: {{ stats.average_views.toFixed(2) }}</p>
      </div>
      <div v-else>
        <p>Loading statistics...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Statistics',
    data() {
      return {
        stats: null
      }
    },
    async mounted() {
      try {
        const response = await axios.get('http://localhost:5000/api/statistics');
        this.stats = response.data;
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    }
  }
  </script>