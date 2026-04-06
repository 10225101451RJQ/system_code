import axios from "axios";
import store from "../store";

// let base = '/api';  // 开发跨域
// let base = 'http://localhost:8090/api';   // 部署跨域1，正式
let base = 'http://59.78.194.93:8090/api';  // 部署跨域2，测试
// let base = 'http://127.0.0.1:4523/m1/1428114-0-default'


export const postJSON = (url, data, params) => {
    store.commit('getToken')
    const token = store.state.user.token
    return axios({
        method: 'post',
        url: `${base}${url}`,
        data: data,
        params: params,
        transformRequest: [function (data) {
            data = JSON.stringify(data);
            return data
        }],
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    });
}

export const postFormData = (url, data, params) => {
    store.commit('getToken')
    const token = store.state.user.token
    return axios({
        method: 'post',
        url: `${base}${url}`,
        data: data,
        params: params,
        headers: {
            'Content-type': 'multipart/form-data',
            'Authorization': 'Bearer ' + token
        },
    });
}

export const getFormData = (url, params) => {
    store.commit('getToken')
    const token = store.state.user.token
    return axios({
        method: 'get',
        url: `${base}${url}`,
        params: params,
        headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer ' + token
        },
        transformRequest: [function (data) {
            data = JSON.stringify(data);
            return data
        }],
    });
}

export function downloadCSV(resp, filename) {
    let data = resp.data;  //csv数据
    filename = filename + ".csv";   //导出的文件名
    let type = "";                      //头部数据类型
    let file = new Blob(["\ufeff" + data], {type: type});
    if (window.navigator.msSaveOrOpenBlob)
        // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else {
        // Others
        let a = document.createElement("a"),
            url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function () {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}