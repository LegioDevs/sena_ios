import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.senaemocional.app',
  appName: 'Sena',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    iosScheme: 'https',
    allowNavigation: [
      'api.senaemocional.com',
      'files.senaemocional.com'
    ]
  },
  plugins: {
    CapacitorHttp: {
      enabled: true
    },
    PushNotifications: {
      presentationOptions: ["badge", "sound", "alert"],
    }
  }
};

export default config;
