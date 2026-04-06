module.exports = {
    devServer: {
        port: 8090, // npm run serve时前端开在的端口
        host: '0.0.0.0',
        // 跨域1：基本没用
        // proxy: "http://localhost:8080"
        // proxy: "http://127.0.0.1:4523/m1/1428114-0-default"
        // 跨域2：通常用这个
        proxy: {
            '/api': {
                // target: 'http://localhost:8080/',            // 后端url，如果调试时本地运行真实后端，使用这个，改为后端url
                target: 'http://127.0.0.1:4523/m1/1428114-0-default',   //  mock用，使用诸如apifox时，使用这个，改为mock的url
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    "^/api": ""
                }
            }
        },
    },
    lintOnSave: false,
    publicPath: "./"
}