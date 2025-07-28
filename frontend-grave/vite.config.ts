/// <reference types="vitest" />

import { defineConfig } from 'vite';
import analog from '@analogjs/platform';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  console.log('🔧 Vite is building in mode:', mode);

  return {
    build: {
      target: ['es2020'],
    },
    resolve: {
      mainFields: ['module'],
    },
    plugins: [
      analog({
        ssr: false,
        static: true,
        nitro: {},
        prerender: {
          routes: [],
        },
      }),
    ],
  };
});
