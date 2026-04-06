import Vue from 'vue';
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'Main',
    component: () => import('@/views/Main.vue'),
    redirect: '/login',
    meta: {login: true},
    children: [
        // 批次及样品数据管理
        {
            path: 'batch',
            component: () => import('@/views/Batch/index.vue'),
            redirect: '/batch/batchList',  // 该配置是若点击选择一级菜单时，默认选中并跳转到该一级菜单下的第一个二级菜单
            children: [
                {
                    path: 'batchList', name: 'batch_batchList',
                    component: () => import('@/views/Batch/BatchList'),
                    meta: {login: true}
                },
                {
                    path: 'detailBatch', name: 'batch_detailBatch',
                    component: () => import('@/views/Batch/DetailBatch'),
                },
                {
                    path: 'postBatch', name: 'batch_postBatch',
                    component: () => import('@/views/Batch/PostBatch'),
                },
                {
                    path: 'recycleBin', name: 'batch_recycleBin',
                    component: () => import('@/views/Batch/RecycleBin'),
                },
                {
                    path: 'postStandardSample', name: 'batch_postStandardSample',
                    component: () => import('@/views/Batch/Sample/PostStandardSample'),
                },
                {
                    path: 'postSourceSample', name: 'batch_postSourceSample',
                    component: () => import('@/views/Batch/Sample/PostSourceSample'),
                },
                {
                    path: 'postConfigSample', name: 'batch_postConfigSample',
                    component: () => import('@/views/Batch/Sample/PostConfigSample'),
                },
                {
                    path: 'postActualSample', name: 'batch_postActualSample',
                    component: () => import('@/views/Batch/Sample/PostActualSample'),
                },
                {
                    path: 'postBlankSample', name: 'batch_postBlankSample',
                    component: () => import('@/views/Batch/Sample/PostBlankSample'),
                },
            ]
        },
        // 分析功能管理
        {
            path: 'analysis',
            component: () => import('@/views/Analysis/index.vue'),
            redirect: '/analysis/detectionLimitCalculation',  // 该配置是若点击选择一级菜单时，默认选中并跳转到该一级菜单下的第一个二级菜单
            children: [
                {
                    path: 'detectionLimitCalculation', name: 'analysis_detectionLimitCalculation',
                    component: () => import('@/views/Analysis/DetectionLimitCalculation'),
                },
                {
                    path: 'particle', name: 'analysis_particle',
                    component: () => import('@/views/Analysis/Particle'),
                },
                {
                    path: 'supportX', name: 'analysis_supportX',
                    component: () => import('@/views/Analysis/SupportX'),
                },
                {
                    path: 'analysisSource', name: 'analysis_analysisSource',
                    component: () => import('@/views/Analysis/AnalysisSource'),
                },
                {
                    path: 'analysisNotSource', name: 'analysis_analysisNotSource',
                    component: () => import('@/views/Analysis/AnalysisNotSource'),
                },
                {
                    path: 'traceabilityAnalysis', name: 'analysis_traceabilityAnalysis',
                    component: () => import('@/views/Analysis/TraceabilityAnalysis'),
                },
                {
                    path: 'fingerprintDiffSame', name: 'analysis_fingerprintDiffSame',
                    component: () => import('@/views/Analysis/FingerprintDiffSame'),
                },
            ]
        },
    ]
},
    {
        path: '/getBackPasswd',
        name: 'getBackPasswd',
        component: () => import('@/views/GetBackPasswd.vue'),
        meta: {login: false}
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('@/views/Login'),
        meta: {login: false}
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('@/views/Register'),
        meta: {login: false}
    }
]

const router = new VueRouter({
    mode: 'hash',
    routes
})

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

export default router