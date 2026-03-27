/**
 * 表单验证工具函数
 */

export interface ValidationResult {
  valid: boolean
  message?: string
}

/**
 * 验证邮箱格式
 */
export const validateEmail = (email: string): ValidationResult => {
  if (!email) {
    return { valid: false, message: '邮箱不能为空' }
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    return { valid: false, message: '邮箱格式不正确' }
  }
  
  return { valid: true }
}

/**
 * 验证密码强度
 * 返回密码强度等级：weak, medium, strong
 */
export const validatePassword = (password: string): ValidationResult & { strength?: 'weak' | 'medium' | 'strong' } => {
  if (!password) {
    return { valid: false, message: '密码不能为空' }
  }
  
  if (password.length < 6) {
    return { valid: false, message: '密码长度至少 6 位', strength: 'weak' }
  }
  
  if (password.length > 20) {
    return { valid: false, message: '密码长度不能超过 20 位', strength: 'weak' }
  }
  
  let strength = 0
  
  // 包含小写字母
  if (/[a-z]/.test(password)) strength++
  // 包含大写字母
  if (/[A-Z]/.test(password)) strength++
  // 包含数字
  if (/[0-9]/.test(password)) strength++
  // 包含特殊字符
  if (/[^a-zA-Z0-9]/.test(password)) strength++
  
  if (strength >= 3) {
    return { valid: true, strength: 'strong' }
  } else if (strength >= 2) {
    return { valid: true, strength: 'medium' }
  } else {
    return { valid: true, strength: 'weak', message: '密码强度较弱，建议包含大小写字母、数字和特殊字符' }
  }
}

/**
 * 验证密码强度等级（用于显示进度条）
 */
export const getPasswordStrength = (password: string): { level: number; text: string; color: string } => {
  if (!password) {
    return { level: 0, text: '', color: '' }
  }
  
  let level = 0
  let text = '弱'
  let color = '#ff4d4f'
  
  if (password.length >= 6) level++
  if (password.length >= 8) level++
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) level++
  if (/[0-9]/.test(password)) level++
  if (/[^a-zA-Z0-9]/.test(password)) level++
  
  if (level >= 5) {
    text = '强'
    color = '#52c41a'
  } else if (level >= 3) {
    text = '中'
    color = '#faad14'
  } else if (level >= 1) {
    text = '弱'
    color = '#ff4d4f'
  }
  
  return {
    level: Math.min(level, 5),
    text,
    color
  }
}

/**
 * 验证手机号格式
 */
export const validatePhone = (phone: string): ValidationResult => {
  if (!phone) {
    return { valid: false, message: '手机号不能为空' }
  }
  
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(phone)) {
    return { valid: false, message: '手机号格式不正确' }
  }
  
  return { valid: true }
}

/**
 * 验证用户名
 */
export const validateUsername = (username: string): ValidationResult => {
  if (!username) {
    return { valid: false, message: '用户名不能为空' }
  }
  
  if (username.length < 3) {
    return { valid: false, message: '用户名长度至少 3 位' }
  }
  
  if (username.length > 20) {
    return { valid: false, message: '用户名长度不能超过 20 位' }
  }
  
  const usernameRegex = /^[\u4e00-\u9fa5a-zA-Z0-9_]+$/
  if (!usernameRegex.test(username)) {
    return { valid: false, message: '用户名只能包含中文、字母、数字和下划线' }
  }
  
  return { valid: true }
}

/**
 * 验证必填字段
 */
export const validateRequired = (value: any, fieldName = '字段'): ValidationResult => {
  if (!value || (typeof value === 'string' && !value.trim())) {
    return { valid: false, message: `${fieldName}不能为空` }
  }
  
  return { valid: true }
}

/**
 * 验证两次密码是否一致
 */
export const validatePasswordMatch = (password: string, confirmPassword: string): ValidationResult => {
  if (!confirmPassword) {
    return { valid: false, message: '请再次输入密码' }
  }
  
  if (password !== confirmPassword) {
    return { valid: false, message: '两次输入的密码不一致' }
  }
  
  return { valid: true }
}

/**
 * 验证 URL 格式
 */
export const validateUrl = (url: string): ValidationResult => {
  if (!url) {
    return { valid: false, message: 'URL 不能为空' }
  }
  
  try {
    new URL(url)
    return { valid: true }
  } catch {
    return { valid: false, message: 'URL 格式不正确' }
  }
}

/**
 * 验证数字范围
 */
export const validateNumberRange = (
  value: number,
  min?: number,
  max?: number,
  fieldName = '数值'
): ValidationResult => {
  if (min !== undefined && value < min) {
    return { valid: false, message: `${fieldName}不能小于${min}` }
  }
  
  if (max !== undefined && value > max) {
    return { valid: false, message: `${fieldName}不能大于${max}` }
  }
  
  return { valid: true }
}
