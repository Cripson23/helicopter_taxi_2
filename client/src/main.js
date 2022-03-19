import { createApp } from 'vue/dist/vue.esm-bundler';
import App from './App.vue';
import router from './router';
import store from './store';
import BootstrapVue3 from 'bootstrap-vue-3';
import print from 'vue3-print-nb';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';

const app = createApp(App);
app.use(store);
app.use(router);
app.use(BootstrapVue3);
app.use(print)
app.mount('#app');