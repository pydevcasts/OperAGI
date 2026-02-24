<!-- pages/dashboard.vue -->
<script setup lang="ts">
import {ref} from 'vue'

// pages/dashboard.vue
definePageMeta({}) // ← بدون middleware

const { user, clear, loggedIn } = useUserSession()

const handleLogout = async () => {
  await clear()
  await navigateTo('/login')
}

const sidebarOpen = ref(false)
const activeNav = ref('dashboard')

const navItems = [
  { id: 'dashboard', label: 'داشبورد', icon: 'home', to: '/dashboard' },
  { id: 'text', label: 'تولید متن', icon: 'pen', to: '/text-generator' },
  { id: 'image', label: 'تولید تصویر', icon: 'image', to: '/image-generator' },
  { id: 'summarizer', label: 'خلاصه‌ساز', icon: 'file', to: '/file-summarizer' },
  { id: 'chat', label: 'چت هوشمند', icon: 'chat', to: '/rag-chat' },
  { id: 'translate', label: 'مترجم هوش مصنوعی', icon: 'globe', to: '/translator' },
  { id: 'code', label: 'دستیار کدنویسی', icon: 'code', to: '/code-assistant' },
]

const services = [
  {
    id: 'text',
    title: 'تولید محتوا',
    desc: 'پست‌های شبکه اجتماعی، مقاله، ایمیل و هر نوع محتوایی را با هوش مصنوعی بنویسید.',
    icon: 'pen',
    gradient: 'from-violet-500 to-indigo-500',
    glow: 'rgba(139,92,246,0.3)',
    tag: 'محبوب',
    to: '/text-generator'
  },
  {
    id: 'image',
    title: 'تولید تصویر',
    desc: 'تصاویر خیره‌کننده از توضیحات متنی شما بسازید.',
    icon: 'image',
    gradient: 'from-pink-500 to-rose-500',
    glow: 'rgba(236,72,153,0.3)',
    tag: 'جدید',
    to: '/image-generator'
  },
  {
    id: 'summarizer',
    title: 'خلاصه‌ساز فایل',
    desc: 'PDF و اسناد را آپلود کنید و خلاصه دقیق دریافت کنید.',
    icon: 'file',
    gradient: 'from-cyan-500 to-blue-500',
    glow: 'rgba(6,182,212,0.3)',
    tag: '',
    to: '/file-summarizer'
  },
  {
    id: 'chat',
    title: 'چت RAG',
    desc: 'روی اسناد خودتان با هوش مصنوعی چت کنید و جواب دقیق دریافت کنید.',
    icon: 'chat',
    gradient: 'from-emerald-500 to-teal-500',
    glow: 'rgba(16,185,129,0.3)',
    tag: '',
    to: '/rag-chat'
  },
  {
    id: 'translate',
    title: 'مترجم هوشمند',
    desc: 'ترجمه حرفه‌ای با درک معنا، نه کلمه به کلمه.',
    icon: 'globe',
    gradient: 'from-amber-500 to-orange-500',
    glow: 'rgba(245,158,11,0.3)',
    tag: '',
    to: '/translator'
  },
  {
    id: 'code',
    title: 'دستیار کدنویسی',
    desc: 'کد بنویسید، باگ پیدا کنید و مستندات تولید کنید.',
    icon: 'code',
    gradient: 'from-slate-400 to-slate-600',
    glow: 'rgba(148,163,184,0.2)',
    tag: 'بتا',
    to: '/code-assistant'
  },
]

const stats = [
  { label: 'محتوا تولید شده', value: '142', unit: 'مورد', color: '#818cf8' },
  { label: 'فایل خلاصه شده', value: '67', unit: 'فایل', color: '#34d399' },
  { label: 'پرسش پاسخ داده', value: '1.2K', unit: 'سوال', color: '#f472b6' },
  { label: 'اعتبار باقی‌مانده', value: '850', unit: 'توکن', color: '#fb923c' },
]

const recentActivity = [
  { action: 'تولید متن', detail: 'پست اینستاگرام برای محصول جدید', time: '۵ دقیقه پیش', icon: 'pen' },
  { action: 'خلاصه‌سازی', detail: 'گزارش مالی Q3.pdf', time: '۲ ساعت پیش', icon: 'file' },
  { action: 'چت RAG', detail: '۱۴ سوال از سند قرارداد', time: 'دیروز', icon: 'chat' },
]
</script>

<template>
  <div class="dashboard-root">
    <!-- Ambient background -->
    <div class="ambient">
      <div class="amb-1" />
      <div class="amb-2" />
      <div class="amb-3" />
      <div class="bg-grid" />
    </div>

    <!-- Mobile overlay -->
    <div v-if="sidebarOpen" class="overlay" @click="sidebarOpen = false" />

    <!-- ═══════════════ SIDEBAR ═══════════════ -->
    <aside :class="['sidebar', { 'sidebar-open': sidebarOpen }]">
      <!-- Logo -->
      <div class="sidebar-logo">
        <div class="logo-mark">
          <svg width="22" height="22" viewBox="0 0 28 28" fill="none">
            <path d="M14 2L26 8V20L14 26L2 20V8L14 2Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 8L20 11V17L14 20L8 17V11L14 8Z" fill="currentColor" opacity="0.5"/>
            <circle cx="14" cy="14" r="2" fill="currentColor"/>
          </svg>
        </div>
        <div>
          <span class="logo-text">OperAGI</span>
          <span class="logo-sub">AI Platform</span>
        </div>
      </div>

      <!-- Nav -->
      <nav class="sidebar-nav">
        <NuxtLink
          v-for="item in navItems"
          :key="item.id"
          :to="loggedIn ? '/item.to' : '/login'"
          :class="['nav-item', { 'nav-active': activeNav === item.id }]"
          @click="activeNav = item.id; sidebarOpen = false"
        >
          <!-- Icons -->
          <span class="nav-icon">
            <svg v-if="item.icon === 'home'" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1L1 7v8h5v-4h4v4h5V7L8 1z"/></svg>
            <svg v-if="item.icon === 'pen'" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M11.013 1.427a1.75 1.75 0 012.474 0l1.086 1.086a1.75 1.75 0 010 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 01-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61z"/></svg>
            <svg v-if="item.icon === 'image'" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M1.5 2.5A1.5 1.5 0 013 1h10a1.5 1.5 0 011.5 1.5v11A1.5 1.5 0 0113 15H3a1.5 1.5 0 01-1.5-1.5v-11zM3 2.5v5.293l2.146-2.147a.5.5 0 01.708 0L8 7.793l2.146-2.147a.5.5 0 01.707 0L13 7.793V2.5H3zM3 13.5h10v-3.793l-2.146-2.147L8 9.707l-2.146-2.147L3 9.793v3.707z"/></svg>
            <svg v-if="item.icon === 'file'" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M4 1.5H3a2 2 0 00-2 2V14a2 2 0 002 2h10a2 2 0 002-2V3.5a2 2 0 00-2-2h-1v1h1a1 1 0 011 1V14a1 1 0 01-1 1H3a1 1 0 01-1-1V3.5a1 1 0 011-1h1v-1z"/><path d="M9.5 1a.5.5 0 01.5.5v1a.5.5 0 01-.5.5h-3a.5.5 0 01-.5-.5v-1a.5.5 0 01.5-.5h3z"/></svg>
            <svg v-if="item.icon === 'chat'" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M2.678 11.894a1 1 0 01.287.801 10.97 10.97 0 01-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 01.71-.074A8.06 8.06 0 008 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894z"/></svg>
            <svg v-if="item.icon === 'globe'" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M0 8a8 8 0 1116 0A8 8 0 010 8zm7.5-6.923c-.67.204-1.335.82-1.887 1.855-.143.268-.276.56-.395.872.705.157 1.472.257 2.282.287V1.077zM4.249 3.539c.142-.384.304-.744.481-1.078a6.7 6.7 0 01.597-.933A7.01 7.01 0 002.255 4.504 11.565 11.565 0 014.249 3.54zm2.5.133a14.25 14.25 0 00-2.57-.366A7.018 7.018 0 007.5 1.077a14.25 14.25 0 00-.75 2.595zm.186 1.394a13.216 13.216 0 00-2.721-.403 6.993 6.993 0 00-.217.732 14.06 14.06 0 002.938.409v-.738zm.246.737a14.06 14.06 0 002.938-.409 6.993 6.993 0 00-.217-.732 13.216 13.216 0 00-2.721.403v.738zm0 .762v.738a14.04 14.04 0 002.938.409c-.07-.247-.14-.49-.217-.732a13.225 13.225 0 00-2.721-.415zm0 1.5v3.584a14.253 14.253 0 002.282-.287c-.12-.312-.252-.604-.395-.872-.552-1.035-1.218-1.651-1.887-1.855v.43zm2.5 2.122c.705-.157 1.472-.257 2.282-.287a14.252 14.252 0 00-.395-.872c-.552-1.035-1.218-1.651-1.887-1.855V8.7z"/></svg>
            <svg v-if="item.icon === 'code'" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M5.854 4.854a.5.5 0 10-.708-.708l-3.5 3.5a.5.5 0 000 .708l3.5 3.5a.5.5 0 00.708-.708L2.707 8l3.147-3.146zm4.292 0a.5.5 0 01.708-.708l3.5 3.5a.5.5 0 010 .708l-3.5 3.5a.5.5 0 01-.708-.708L13.293 8l-3.147-3.146z"/></svg>
          </span>
          <span>{{ item.label }}</span>
        </NuxtLink>
      </nav>

      <!-- User & Logout -->
      <div class="sidebar-bottom">
        <div class="sidebar-user">
          <div class="user-avatar-sm">
            <img v-if="user?.picture" :src="user.picture" alt="avatar" />
            <span v-else>{{ (user?.name || user?.email || 'U')[0].toUpperCase() }}</span>
          </div>
          <div class="user-info">
            <p class="user-name-sm">{{ user?.name || user?.email?.split('@')[0] }}</p>
            <p class="user-plan">پلن رایگان</p>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M10 12.5a.5.5 0 01-.5.5h-8a.5.5 0 01-.5-.5v-9a.5.5 0 01.5-.5h8a.5.5 0 01.5.5v2a.5.5 0 001 0v-2A1.5 1.5 0 009.5 2h-8A1.5 1.5 0 000 3.5v9A1.5 1.5 0 001.5 14h8a1.5 1.5 0 001.5-1.5v-2a.5.5 0 00-1 0v2z"/><path d="M15.854 8.354a.5.5 0 000-.708l-3-3a.5.5 0 00-.708.708L14.293 7.5H5.5a.5.5 0 000 1h8.793l-2.147 2.146a.5.5 0 00.708.708l3-3z"/></svg>
          خروج
        </button>
      </div>
    </aside>

    <!-- ═══════════════ MAIN ═══════════════ -->
    <main class="main">
      <!-- Topbar -->
      <header class="topbar">
        <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/></svg>
        </button>

        <div class="topbar-search">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" class="search-icon"><path d="M11.742 10.344a6.5 6.5 0 10-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 001.415-1.414l-3.85-3.85a1.007 1.007 0 00-.115-.099zm-5.242.656a5 5 0 110-10 5 5 0 010 10z"/></svg>
          <input type="text" placeholder="جستجو در خدمات..." class="search-input" />
        </div>

        <div class="topbar-right">
          <button class="topbar-btn notif-btn">
            <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor"><path d="M8 16a2 2 0 002-2H6a2 2 0 002 2zm.995-14.901a1 1 0 10-1.99 0A5.002 5.002 0 003 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/></svg>
            <span class="notif-dot" />
          </button>

          <div class="topbar-user">
            <div class="user-avatar">
              <img v-if="user?.picture" :src="user.picture" alt="avatar" />
              <span v-else>{{ (user?.name || user?.email || 'U')[0].toUpperCase() }}</span>
            </div>
            <span class="topbar-username">{{ user?.name || user?.email?.split('@')[0] }}</span>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <div class="content">

        <!-- Welcome -->
        <div class="welcome-section">
          <div class="welcome-text">
            <h1 class="welcome-title">
              سلام، {{ user?.name || user?.email?.split('@')[0] }} 👋
            </h1>
            <p class="welcome-sub">امروز با هوش مصنوعی چه کاری می‌خواهید انجام دهید؟</p>
          </div>
          <div class="welcome-badge">
            <span class="badge-dot" />
            سیستم فعال است
          </div>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
          <div v-for="(stat, i) in stats" :key="i" class="stat-card" :style="{ '--glow': stat.color, animationDelay: i * 0.08 + 's' }">
            <p class="stat-value" :style="{ color: stat.color }">{{ stat.value }}</p>
            <p class="stat-unit">{{ stat.unit }}</p>
            <p class="stat-label">{{ stat.label }}</p>
            <div class="stat-bar">
              <div class="stat-bar-fill" :style="{ background: stat.color, width: (parseInt(stat.value) % 100) + '%' }" />
            </div>
          </div>
        </div>

        <!-- Services -->
        <div class="section-header">
          <h2 class="section-title">خدمات هوش مصنوعی</h2>
          <p class="section-sub">ابزارهای قدرتمند برای افزایش بهره‌وری</p>
        </div>

        <div class="services-grid">
          <NuxtLink
            v-for="(s, i) in services"
            :key="s.id"
            :to="loggedIn ? '/s.to' : '/login'"
            class="service-card"
            :style="{ '--glow': s.glow, animationDelay: i * 0.07 + 's' }"
          >
            <div class="service-top">
              <div :class="['service-icon-wrap', `bg-gradient-to-br ${s.gradient}`]">
                <svg v-if="s.icon === 'pen'" width="20" height="20" viewBox="0 0 16 16" fill="white"><path d="M11.013 1.427a1.75 1.75 0 012.474 0l1.086 1.086a1.75 1.75 0 010 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 01-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61z"/></svg>
                <svg v-if="s.icon === 'image'" width="20" height="20" viewBox="0 0 16 16" fill="white"><path d="M1.5 2.5A1.5 1.5 0 013 1h10a1.5 1.5 0 011.5 1.5v11A1.5 1.5 0 0113 15H3a1.5 1.5 0 01-1.5-1.5v-11zM3 2.5v5.293l2.146-2.147a.5.5 0 01.708 0L8 7.793l2.146-2.147a.5.5 0 01.707 0L13 7.793V2.5H3z"/></svg>
                <svg v-if="s.icon === 'file'" width="20" height="20" viewBox="0 0 16 16" fill="white"><path d="M4 1.5H3a2 2 0 00-2 2V14a2 2 0 002 2h10a2 2 0 002-2V3.5a2 2 0 00-2-2h-1v1h1a1 1 0 011 1V14a1 1 0 01-1 1H3a1 1 0 01-1-1V3.5a1 1 0 011-1h1v-1z"/></svg>
                <svg v-if="s.icon === 'chat'" width="20" height="20" viewBox="0 0 16 16" fill="white"><path d="M2.678 11.894a1 1 0 01.287.801 10.97 10.97 0 01-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 01.71-.074A8.06 8.06 0 008 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894z"/></svg>
                <svg v-if="s.icon === 'globe'" width="20" height="20" viewBox="0 0 16 16" fill="white"><path d="M0 8a8 8 0 1116 0A8 8 0 010 8zm7.5-6.923c-.67.204-1.335.82-1.887 1.855-.143.268-.276.56-.395.872.705.157 1.472.257 2.282.287V1.077z"/></svg>
                <svg v-if="s.icon === 'code'" width="20" height="20" viewBox="0 0 16 16" fill="white"><path d="M5.854 4.854a.5.5 0 10-.708-.708l-3.5 3.5a.5.5 0 000 .708l3.5 3.5a.5.5 0 00.708-.708L2.707 8l3.147-3.146zm4.292 0a.5.5 0 01.708-.708l3.5 3.5a.5.5 0 010 .708l-3.5 3.5a.5.5 0 01-.708-.708L13.293 8l-3.147-3.146z"/></svg>
              </div>
              <span v-if="s.tag" :class="['service-tag', { 'tag-new': s.tag === 'جدید', 'tag-hot': s.tag === 'محبوب', 'tag-beta': s.tag === 'بتا' }]">
                {{ s.tag }}
              </span>
            </div>
            <h3 class="service-title">{{ s.title }}</h3>
            <p class="service-desc">{{ s.desc }}</p>
            <div class="service-cta">
              شروع کنید
              <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M1 8a.5.5 0 01.5-.5h11.793l-3.147-3.146a.5.5 0 01.708-.708l4 4a.5.5 0 010 .708l-4 4a.5.5 0 01-.708-.708L13.293 8.5H1.5A.5.5 0 011 8z"/></svg>
            </div>
          </NuxtLink>
        </div>

        <!-- Recent + Upgrade -->
        <div class="bottom-grid">
          <!-- Recent Activity -->
          <div class="recent-card">
            <h3 class="card-title-sm">فعالیت‌های اخیر</h3>
            <div class="activity-list">
              <div v-for="(a, i) in recentActivity" :key="i" class="activity-item">
                <div class="activity-icon">
                  <svg v-if="a.icon === 'pen'" width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M11.013 1.427a1.75 1.75 0 012.474 0l1.086 1.086a1.75 1.75 0 010 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 01-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61z"/></svg>
                  <svg v-if="a.icon === 'file'" width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M4 1.5H3a2 2 0 00-2 2V14a2 2 0 002 2h10a2 2 0 002-2V3.5a2 2 0 00-2-2h-1v1h1a1 1 0 011 1V14a1 1 0 01-1 1H3a1 1 0 01-1-1V3.5a1 1 0 011-1h1v-1z"/></svg>
                  <svg v-if="a.icon === 'chat'" width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M2.678 11.894a1 1 0 01.287.801 10.97 10.97 0 01-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 01.71-.074A8.06 8.06 0 008 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894z"/></svg>
                </div>
                <div class="activity-text">
                  <p class="activity-action">{{ a.action }}</p>
                  <p class="activity-detail">{{ a.detail }}</p>
                </div>
                <span class="activity-time">{{ a.time }}</span>
              </div>
            </div>
          </div>

          <!-- Upgrade card -->
          <div class="upgrade-card">
            <div class="upgrade-glow" />
            <div class="upgrade-icon">⚡</div>
            <h3 class="upgrade-title">ارتقا به پرمیوم</h3>
            <p class="upgrade-desc">به توکن‌های نامحدود، مدل‌های پیشرفته‌تر و پشتیبانی اولویت‌دار دسترسی داشته باشید.</p>
            <ul class="upgrade-features">
              <li>✓ توکن نامحدود</li>
              <li>✓ GPT-4 و Claude Opus</li>
              <li>✓ API اختصاصی</li>
              <li>✓ پشتیبانی ۲۴/۷</li>
            </ul>
            <button class="upgrade-btn">ارتقا به پرو</button>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard-root {
  font-family: 'Vazirmatn', sans-serif;
  direction: rtl;
  display: flex;
  min-height: 100vh;
  background: #060912;
  color: #e2e8f0;
  position: relative;
  overflow-x: hidden;
}

/* ─── Ambient ─── */
.ambient { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.amb-1 {
  position: absolute;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 65%);
  top: -200px; right: -100px;
  animation: drift 12s ease-in-out infinite;
}
.amb-2 {
  position: absolute;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 65%);
  bottom: -150px; left: -50px;
  animation: drift 15s ease-in-out infinite reverse;
}
.amb-3 {
  position: absolute;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(236,72,153,0.07) 0%, transparent 65%);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  animation: drift 10s ease-in-out infinite 3s;
}
.bg-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
  background-size: 48px 48px;
}
@keyframes drift {
  0%, 100% { transform: translate(0,0); }
  33% { transform: translate(30px, -20px); }
  66% { transform: translate(-20px, 20px); }
}

/* ─── Overlay (mobile) ─── */
.overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.6);
  z-index: 40;
  backdrop-filter: blur(2px);
}

/* ─── Sidebar ─── */
.sidebar {
  position: fixed;
  top: 0; right: 0;
  width: 240px; height: 100vh;
  background: rgba(10, 14, 26, 0.95);
  border-left: 1px solid rgba(255,255,255,0.06);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  z-index: 50;
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
}
@media (min-width: 1024px) {
  .sidebar { transform: translateX(0); }
}
.sidebar-open { transform: translateX(0) !important; }

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.logo-mark {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: white;
  box-shadow: 0 4px 16px rgba(99,102,241,0.4);
  flex-shrink: 0;
}
.logo-text {
  display: block;
  font-size: 1.1rem;
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.02em;
}
.logo-sub {
  display: block;
  font-size: 0.7rem;
  color: #475569;
  margin-top: 1px;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.65rem 0.85rem;
  border-radius: 10px;
  font-size: 0.875rem;
  color: #64748b;
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
}
.nav-item:hover { background: rgba(255,255,255,0.05); color: #94a3b8; }
.nav-active {
  background: rgba(99,102,241,0.15) !important;
  color: #a5b4fc !important;
}
.nav-icon { display: flex; align-items: center; flex-shrink: 0; }

.sidebar-bottom {
  padding: 1rem 0.75rem;
  border-top: 1px solid rgba(255,255,255,0.05);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.sidebar-user {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.5rem 0.65rem;
}
.user-avatar-sm {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem;
  font-weight: 600;
  overflow: hidden;
  flex-shrink: 0;
}
.user-avatar-sm img { width: 100%; height: 100%; object-fit: cover; }
.user-name-sm { font-size: 0.825rem; font-weight: 600; color: #cbd5e1; }
.user-plan { font-size: 0.72rem; color: #475569; }
.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem;
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 10px;
  color: #f87171;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.15s;
}
.logout-btn:hover { background: rgba(239,68,68,0.2); }

/* ─── Main ─── */
.main {
  flex: 1;
  margin-left: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  z-index: 1;
}
@media (min-width: 1024px) {
  .main { margin-right: 240px; }
}

/* ─── Topbar ─── */
.topbar {
  position: sticky;
  top: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1.5rem;
  background: rgba(6,9,18,0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.menu-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.35rem;
  display: flex;
  align-items: center;
  border-radius: 8px;
  transition: color 0.15s, background 0.15s;
}
.menu-btn:hover { color: #94a3b8; background: rgba(255,255,255,0.05); }
@media (min-width: 1024px) { .menu-btn { display: none; } }

.topbar-search {
  flex: 1;
  max-width: 380px;
  position: relative;
  display: flex;
  align-items: center;
}
.search-icon { position: absolute; right: 0.8rem; color: #334155; pointer-events: none; }
.search-input {
  width: 100%;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  padding: 0.55rem 2.2rem 0.55rem 1rem;
  color: #94a3b8;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem;
  outline: none;
  transition: border-color 0.2s;
  direction: rtl;
}
.search-input::placeholder { color: #334155; }
.search-input:focus { border-color: rgba(99,102,241,0.4); }

.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-right: auto;
}
.topbar-btn {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  position: relative;
  transition: background 0.15s;
}
.topbar-btn:hover { background: rgba(255,255,255,0.08); }
.notif-dot {
  position: absolute;
  top: 6px; left: 6px;
  width: 7px; height: 7px;
  background: #6366f1;
  border-radius: 50%;
  border: 2px solid #060912;
}
.topbar-user {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.user-avatar {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem;
  font-weight: 700;
  overflow: hidden;
  border: 2px solid rgba(99,102,241,0.4);
}
.user-avatar img { width: 100%; height: 100%; object-fit: cover; }
.topbar-username { font-size: 0.875rem; font-weight: 500; color: #cbd5e1; display: none; }
@media (min-width: 640px) { .topbar-username { display: block; } }

/* ─── Content ─── */
.content {
  padding: 2rem 1.5rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

/* Welcome */
.welcome-section {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  animation: fadeUp 0.5s ease forwards;
}
.welcome-title {
  font-size: clamp(1.4rem, 3vw, 1.9rem);
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.03em;
  margin-bottom: 0.3rem;
}
.welcome-sub { font-size: 0.9rem; color: #64748b; }
.welcome-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(16,185,129,0.1);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 20px;
  padding: 0.4rem 0.9rem;
  font-size: 0.8rem;
  color: #34d399;
  white-space: nowrap;
}
.badge-dot {
  width: 7px; height: 7px;
  background: #34d399;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.85); }
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.875rem;
  margin-bottom: 2.5rem;
}
@media (min-width: 768px) {
  .stats-grid { grid-template-columns: repeat(4, 1fr); }
}
.stat-card {
  background: rgba(15,20,35,0.8);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
  padding: 1.1rem 1.25rem;
  animation: fadeUp 0.5s ease forwards;
  opacity: 0;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
  border-color: rgba(255,255,255,0.12);
  box-shadow: 0 0 20px var(--glow, rgba(99,102,241,0.1));
}
.stat-value { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 0.1rem; }
.stat-unit { font-size: 0.75rem; color: #475569; }
.stat-label { font-size: 0.78rem; color: #64748b; margin-top: 0.3rem; }
.stat-bar { height: 3px; background: rgba(255,255,255,0.05); border-radius: 2px; margin-top: 0.75rem; overflow: hidden; }
.stat-bar-fill { height: 100%; border-radius: 2px; opacity: 0.7; }

/* Section header */
.section-header { margin-bottom: 1.25rem; }
.section-title { font-size: 1.15rem; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; margin-bottom: 0.25rem; }
.section-sub { font-size: 0.825rem; color: #475569; }

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}
@media (min-width: 640px) { .services-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .services-grid { grid-template-columns: repeat(3, 1fr); } }

.service-card {
  background: rgba(12,16,30,0.9);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 1.4rem;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  animation: fadeUp 0.5s ease forwards;
  opacity: 0;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}
.service-card:hover {
  border-color: rgba(255,255,255,0.12);
  transform: translateY(-3px);
  box-shadow: 0 12px 40px var(--glow, rgba(99,102,241,0.15));
}
.service-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 0.3rem;
}
.service-icon-wrap {
  width: 44px; height: 44px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.service-tag {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
}
.tag-hot { background: rgba(239,68,68,0.15); color: #f87171; }
.tag-new { background: rgba(16,185,129,0.15); color: #34d399; }
.tag-beta { background: rgba(245,158,11,0.15); color: #fbbf24; }

.service-title { font-size: 1rem; font-weight: 700; color: #f1f5f9; }
.service-desc { font-size: 0.825rem; color: #64748b; line-height: 1.6; flex: 1; }
.service-cta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.825rem;
  font-weight: 600;
  color: #818cf8;
  margin-top: 0.4rem;
  transition: gap 0.15s;
}
.service-card:hover .service-cta { gap: 0.7rem; }

/* Bottom grid */
.bottom-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
@media (min-width: 768px) { .bottom-grid { grid-template-columns: 1fr 320px; } }

/* Recent */
.recent-card {
  background: rgba(12,16,30,0.9);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 1.4rem;
}
.card-title-sm {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 1rem;
}
.activity-list { display: flex; flex-direction: column; gap: 0; }
.activity-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.activity-item:last-child { border-bottom: none; }
.activity-icon {
  width: 32px; height: 32px;
  background: rgba(99,102,241,0.12);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #818cf8;
  flex-shrink: 0;
}
.activity-text { flex: 1; min-width: 0; }
.activity-action { font-size: 0.825rem; font-weight: 600; color: #cbd5e1; }
.activity-detail { font-size: 0.775rem; color: #475569; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.activity-time { font-size: 0.75rem; color: #334155; white-space: nowrap; }

/* Upgrade */
.upgrade-card {
  background: rgba(12,16,30,0.9);
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: 16px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}
.upgrade-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at top right, rgba(99,102,241,0.12) 0%, transparent 60%);
  pointer-events: none;
}
.upgrade-icon { font-size: 1.75rem; margin-bottom: 0.75rem; }
.upgrade-title { font-size: 1rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.5rem; }
.upgrade-desc { font-size: 0.825rem; color: #64748b; line-height: 1.6; margin-bottom: 1rem; }
.upgrade-features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  margin-bottom: 1.25rem;
}
.upgrade-features li { font-size: 0.825rem; color: #94a3b8; }
.upgrade-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 10px;
  color: white;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(99,102,241,0.35);
  transition: opacity 0.2s, transform 0.15s;
}
.upgrade-btn:hover { opacity: 0.9; transform: translateY(-1px); }

/* Animation */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>