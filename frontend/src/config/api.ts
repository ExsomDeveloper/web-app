// src/config/api.ts
export interface ApiConfig {
  local: string;
  production: string;
}

export const API_CONFIG: ApiConfig = {
  local: 'http://localhost:8000',
  production: 'https://unslighted-complaisantly-erma.ngrok-free.dev'
};

export const getApiUrl = (): string => {
  // Определяем окружение по hostname
  const isLocal = window.location.hostname === 'localhost' || 
                  window.location.hostname === '127.0.0.1' ||
                  window.location.hostname === '';
  
  return isLocal ? API_CONFIG.local : API_CONFIG.production;
};

// Экспортируем текущий URL для удобства
export const API_URL = getApiUrl();
