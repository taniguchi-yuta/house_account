import { createI18n } from 'vue-i18n'

import gbMessages from './locales/gb.json'

const messages = {
  gb: gbMessages,
  // 他のロケールもここに追加
}

export default createI18n({
  legacy: false,
  locale: 'gb',
  fallbackLocale: 'gb',
  messages
})
