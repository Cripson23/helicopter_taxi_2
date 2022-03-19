import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import { sessionModule } from './sessionModule'

export default createStore({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  modules: {
    session: sessionModule,
  }
})
