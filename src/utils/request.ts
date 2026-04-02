import axios from 'axios'

// 1. 核心修复：仅配置独立的 axios 实例，不修改全局 axios.defaults
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE
})

// 2. 请求拦截器：仅作用于该 request 实例
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    // 如果存在 token，则在请求头中携带 Bearer Token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    // 处理请求错误
    return Promise.reject(error)
  }
)

export default request