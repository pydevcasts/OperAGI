import { createRouter, createWebHistory } from 'vue-router'
import AudioRecorder from '../components/AudioRecorder.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'AudioRecorder',
      component: AudioRecorder
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
 
  ],
})

export default router





