import { initializeApp } from "https://www.gstatic.com/firebasejs/12.13.0/firebase-app.js";
import { getMessaging, onBackgroundMessage } from "https://www.gstatic.com/firebasejs/12.13.0/firebase-messaging.js";

const firebaseConfig = {
  apiKey: "AIzaSyBMgDxQuCD1dhuqeAOPGAHgh2J63ZzSlGg",
  authDomain: "senaemocional.firebaseapp.com",
  projectId: "senaemocional",
  storageBucket: "senaemocional.firebasestorage.app",
  messagingSenderId: "399564857109",
  appId: "1:399564857109:web:4ff7b86a91e79de216931c",
  measurementId: "G-ZJGEB5XVSF"
};

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

onBackgroundMessage(messaging, (payload) => {
  const title = payload.notification?.title ?? "SENA";
  const options = {
    body: payload.notification?.body ?? "",
    icon: "/favicon.png",
    data: payload.data,
  };
  self.registration.showNotification(title, options);
});
