// openapi-ts.config.ts

import { defineConfig } from '@hey-api/openapi-ts';
import dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
  input: 'http://localhost:9000/openapi.json',
  output: {
    format: 'prettier',
    lint: 'eslint',
    path: 'src/lib/client'
  },
  plugins: [
    '@hey-api/client-fetch',
    '@hey-api/schemas',
    {
      dates: true,
      name: '@hey-api/transformers',
    },
    {
      enums: 'javascript',
      name: '@hey-api/typescript',
    },
    {
      name: '@hey-api/sdk',
      transformer: true,
    },
  ],
});