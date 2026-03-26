/**
 * 格式化时间为 xxxx 年 x 月 x 日 xx:xx:xx 格式
 */
export function formatTime(dateString: string): string {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = date.getHours()
  const minutes = date.getMinutes()
  const seconds = date.getSeconds()
  
  return `${year}年${month}月${day}日 ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

/**
 * 格式化日期为 xxxx 年 x 月 x 日
 */
export function formatDate(dateString: string): string {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  
  return `${year}年${month}月${day}日`
}

/**
 * 格式化日期时间为 xxxx年x月x日 xx:xx:xx 格式（与formatTime相同，用于兼容）
 */
export function formatDateTime(dateString: string): string {
  return formatTime(dateString)
}
