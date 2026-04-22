// 头像管理工具
// 用于统一管理用户头像的获取、更新和缓存

// 获取用户头像
export function getAvatar() {
  const userStr = localStorage.getItem('user')
  if (!userStr) return ''
  
  try {
    const user = JSON.parse(userStr)
    return user.avatar || ''
  } catch {
    return ''
  }
}

// 获取用户信息
export function getUser() {
  const userStr = localStorage.getItem('user')
  if (!userStr) return null
  
  try {
    return JSON.parse(userStr)
  } catch {
    return null
  }
}

// 更新用户头像
export function updateAvatar(avatarUrl: string) {
  const user = getUser()
  if (user) {
    user.avatar = avatarUrl
    localStorage.setItem('user', JSON.stringify(user))
  }
}

// 清除用户信息
export function clearUser() {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
}

// 获取用户首字母
export function getUserInitial() {
  const user = getUser()
  if (!user) return 'U'
  const name = user.name || user.username || ''
  return name.charAt(0).toUpperCase() || 'U'
}

// 获取用户姓名
export function getUserName() {
  const user = getUser()
  if (!user) return '用户'
  return user.name || user.username || '用户'
}

// 获取用户积分
export function getUserPoints() {
  const user = getUser()
  if (!user) return 0
  return user.points || 0
}