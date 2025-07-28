/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_DEV_BASE_URL: string;
  // other env variables
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
