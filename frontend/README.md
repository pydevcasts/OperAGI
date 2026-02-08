# Nuxt Minimal Starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.
1. کاربر با گوگل وارد می‌شود
   ↓
2. Better Auth سیشن ایجاد می‌کند (در کوکی)
   ↓
3. صفحه کالبک بارگذاری می‌شود
   ↓
4. اطلاعات کاربر از Better Auth دریافت می‌شود
   ↓
5. اطلاعات به بک‌اند ارسال می‌شود
   ↓
6. بک‌اند کاربر را در دیتابیس ذخیره می‌کند
   ↓
7. بک‌اند توکن JWT برمی‌گرداند
   ↓
8. توکن‌ها و اطلاعات کاربر در localStorage ذخیره می‌شود