<template>
    <div class="create-template">
      <h2>Create New Template</h2>
      <form @submit.prevent="createTemplate">
        <input v-model="templateName" placeholder="Template Name" required>
        <div v-for="(field, index) in fields" :key="index">
          <select v-model="field.type">
            <option value="text">Text</option>
            <option value="media">Media</option>
            <option value="link">Link</option>
          </select>
          <input v-model="field.name" placeholder="Field Name" required>
          <button type="button" @click="removeField(index)">Remove</button>
        </div>
        <button type="button" @click="addField">Add Field</button>
        <button type="submit">Create Template</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'CreateTemplate',
    data() {
      return {
        templateName: '',
        fields: []
      }
    },
    methods: {
      addField() {
        this.fields.push({ type: 'text', name: '' })
      },
      removeField(index) {
        this.fields.splice(index, 1)
      },
      async createTemplate() {
        try {
          await axios.post('http://localhost:5000/api/templates', {
            name: this.templateName,
            fields: this.fields
          })
          this.$router.push('/templates')
        } catch (error) {
          console.error('Error creating template:', error)
        }
      }
    }
  }
  </script>