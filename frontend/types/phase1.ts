export type Platform = 'instagram' | 'twitter' | 'youtube'
export type Language = 'en' | 'fa'

export interface SocialConnection {
  id: number
  provider: Platform
  display_name: string
  external_url: string
  is_active: boolean
  social_account: { id: number; provider: Platform; uid: string; extra_data: Record<string, unknown> }
}

export interface GeneratedContent {
  id: number
  generated_text: string
  title: string
  description: string
  suggested_hashtags: string
  hashtags: string[]
  suggested_publish_time: string | null
  provider: string
}

export interface ContentPost {
  id: number
  platform: Platform
  language: Language
  tone: string
  content: string
  visual_idea: string
  status: string
  created_at: string
  generated_content?: GeneratedContent
}

export interface Schedule {
  id: number
  post: ContentPost
  scheduled_for: string
  timezone: string
  status: string
  last_error: string
}

export interface DashboardData {
  summary: Record<string, number>
  analytics: Record<string, number>
  platforms: Array<{ platform: Platform; posts: number }>
  recent_posts: ContentPost[]
  upcoming: Schedule[]
}

export interface AnalyticsSnapshot {
  id: number
  platform: Platform
  impressions: number
  reach: number
  likes: number
  comments: number
  shares: number
  clicks: number
  views: number
  followers: number
  engagement_rate: number
  captured_at: string
}

export interface Plan {
  id: number
  slug: string
  name: string
  price: string
  duration_days: number
  monthly_post_limit: number | null
  social_account_limit: number
  features: string[]
}
