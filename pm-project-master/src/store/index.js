import Vue from 'vue'
import Vuex from 'vuex'
import user from '@/store/user'
import lang from '@/store/lang'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        user, lang
    }
})