import axios from 'axios'

// 全局设置 baseURL，覆盖所有 axios 实例
axios.defaults.baseURL = import.meta.env.VITE_API_BASE

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE
})

request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// 同时给全局 axios 也加上 token 拦截
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default request