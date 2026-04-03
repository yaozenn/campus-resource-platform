const uncollect = async (item: any) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/api/courses/uncollect/${item.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    collections.value = collections.value.filter(c => c.id !== item.id)
    alert('已取消收藏！')
  } catch (e: any) {
    console.error('取消收藏失败:', e)
    const msg = e.response?.data?.detail || e.response?.data?.error || '取消失败，请稍后重试'
    alert(msg)
  }
}