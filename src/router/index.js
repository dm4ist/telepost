import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import CreateTemplate from '../views/CreateTemplate.vue'
import CreatePost from '../views/CreatePost.vue'
import ManageChannels from '../views/ManageChannels.vue'
import EditChannel from '../views/EditChannel.vue'
import Statistics from '../views/Statistics.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/templates',
    name: 'Templates',
    component: CreateTemplate
  },
  {
    path: '/posts',
    name: 'Posts',
    component: CreatePost
  },
  {
    path: '/channels',
    name: 'Channels',
    component: ManageChannels
  },
  {
    path: '/channels/edit/:id',
    name: 'EditChannel',
    component: EditChannel
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router