import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import Vuex from 'vuex'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'
import store from './store'
import md5 from 'js-md5'
import * as echarts from 'echarts'
import i18n from "./lang";

Vue.config.productionTip = false
Vue.use(ElementUI, {
    i18n: (key, value) => i18n.t(key, value)
});
Vue.prototype.$md5 = md5;
Vue.prototype.$echarts = echarts;

router.beforeEach((to, from, next) => {
    store.commit('getToken');
    const token = store.state.user.token
    if (!token && to.name === 'register') {
        next()
    } else if (!token && to.name === 'getBackPasswd') {
        next()
    } else if (!token && to.name !== 'login') {
        next({
            name: 'login'
        })
    } else if (token && (to.name === 'login' || to.name === 'register')) {
        next({path: "batch"})
    } else {
        next()
    }
})

new Vue({
    i18n,
    store,
    router,
    // 全局事件总线
    beforeCreate() {
        Vue.prototype.$bus = this
    },
    render: h => h(App),
}).$mount('#app')