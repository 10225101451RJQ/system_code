import Cookie from 'js-cookie'

export default {
    state: {
        language: '',
    },
    mutations: {
        setLanguage(state, val) {
            state.language = val
            Cookie.set('language', val)
        },
        clearLanguage(state) {
            state.language = ""
            Cookie.remove('language')
        },
        getLanguage(state) {
            state.language = state.language || Cookie.get('language')
        },
    }
}