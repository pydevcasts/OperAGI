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
