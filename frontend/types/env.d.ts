// frontend/types/env.d.ts

declare namespace NodeJS {
  interface ProcessEnv {
    // PRIVATE variables (Server-side only)
    NUXT_INSTAGRAM_CLIENT_ID: string; // Should be defined in .env
    NUXT_INSTAGRAM_CLIENT_SECRET: string; // Should be defined in .env
    NUXT_INSTAGRAM_REDIRECT_URI: string; // Should be defined in .env
    NUXT_SESSION_PASSWORD: string; // Should be defined in .env

    // Google OAuth variables (if used - PRIVATE)
    NUXT_OAUTH_GOOGLE_CLIENT_ID?: string; // Optional, define in .env if used
    NUXT_OAUTH_GOOGLE_CLIENT_SECRET?: string; // Optional, define in .env if used

    // PUBLIC variables (will be exposed to client via runtimeConfig.public)
    NUXT_PUBLIC_API_BASE_URL: string; // Should be defined in .env
  }
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $config: {
      // PRIVATE config values are directly on $config
      // INSTAGRAM_CLIENT_ID: string; // Example if needed on server-side
      // INSTAGRAM_CLIENT_SECRET: string;
      // INSTAGRAM_REDIRECT_URI: string;
      // NUXT_OAUTH_GOOGLE_CLIENT_ID?: string;
      // NUXT_OAUTH_GOOGLE_CLIENT_SECRET?: string;

      // PUBLIC config values are under $config.public
      public: {
        API_BASE_URL: string;
        // GOOGLE_CLIENT_ID?: string; // Example if you make it public
      }
    }
  }
}
