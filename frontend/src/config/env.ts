// src/config/env.ts
export const ENV = {
  // API URLs
  API_URL_LOCAL: process.env.REACT_APP_API_URL_LOCAL || 'http://localhost:8000',
  API_URL_PRODUCTION: process.env.REACT_APP_API_URL_PRODUCTION || 'https://unslighted-complaisantly-erma.ngrok-free.dev',
  
  // Environment detection
  IS_LOCAL: process.env.NODE_ENV === 'development' || 
            window.location.hostname === 'localhost' || 
            window.location.hostname === '127.0.0.1' ||
            window.location.hostname === '',
  
  // App info
  APP_NAME: 'Telegram Try-On',
  VERSION: '1.0.0'
};

export const getApiUrl = (): string => {
  return ENV.IS_LOCAL ? ENV.API_URL_LOCAL : ENV.API_URL_PRODUCTION;
};
