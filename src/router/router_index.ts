import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import StudentLayout from '../layouts/StudentLayout.vue'
import TeacherLayout from '../layouts/TeacherLayout.vue'
import StudentForum from '../components/student/Forum.vue'
import StudentAnnouncements from '../components/student/Announcements.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminLayout,
      children: [
        { path: 'personal', name: 'AdminPersonal', component: () => import('../components/admin/PersonalCenter.vue') },
        { path: 'teachers', name: 'TeacherManagement', component: () => import('../components/admin/TeacherManagement.vue') },
        { path: 'students', name: 'StudentManagement', component: () => import('../components/admin/StudentManagement.vue') },
        { path: 'resources', name: 'ResourceManagement', component: () => import('../components/admin/AdminCourseResourceManagement.vue') },
        { path: 'forum', name: 'ForumManagement', component: () => import('../components/admin/ForumManagement.vue') },
        { path: 'forum/:id', name: 'AdminPostDetail', component: () => import('../components/student/PostDetail.vue') },
        { path: 'announcements', name: 'AnnouncementManagement', component: () => import('../components/admin/AnnouncementManagement.vue') },
        { path: 'announcements/:id', name: 'AdminAnnouncementDetail', component: () => import('../components/student/AnnouncementDetail.vue') },
        { path: 'types', name: 'TypeManagement', component: () => import('../components/admin/TypeManagement.vue') },
        { path: 'analysis', name: 'DataAnalysis', component: () => import('../components/admin/DataAnalysis.vue') },
        { path: 'user-overview', name: 'AdminUserOverview', component: () => import('../components/admin/UserOverview.vue') },
        { path: 'resource-overview', name: 'AdminResourceOverview', component: () => import('../components/admin/ResourceOverview.vue') },
        { path: 'forum-overview', name: 'AdminForumOverview', component: () => import('../components/admin/ForumOverview.vue') },
        { path: 'pending-resources', name: 'AdminPendingResources', component: () => import('../components/admin/AdminCourseResourceManagement.vue') },
        { path: 'points', name: 'PointsManagement', component: () => import('../components/admin/PointsManagement.vue') },
        { path: 'system', name: 'SystemManagement', component: () => import('../components/admin/SystemManagement.vue') },
        { path: 'settings', name: 'SystemSettings', component: () => import('../components/admin/SystemSettings.vue') },
        { path: '', redirect: '/admin/analysis' }
      ]
    },
    {
      path: '/student',
      name: 'Student',
      component: StudentLayout,
      children: [
        { path: 'forum', name: 'StudentForum', component: () => import('../components/student/Forum.vue') },
        { path: 'forum/:id', name: 'PostDetail', component: () => import('../components/student/PostDetail.vue') },
        { path: 'announcements', name: 'StudentAnnouncements', component: () => import('../components/student/Announcements.vue') },
        { path: 'announcements/:id', name: 'AnnouncementDetail', component: () => import('../components/student/AnnouncementDetail.vue') },
        { path: 'courses', name: 'StudentCourses', component: () => import('../components/student/Courses.vue') },
        { path: 'courses/:id', name: 'CourseDetail', component: () => import('../components/student/CourseDetail.vue') },
        { path: 'personal', name: 'StudentPersonal', component: () => import('../components/student/PersonalCenter.vue') },
        { path: 'collections', name: 'CollectionManagement', component: () => import('../components/student/CollectionManagement.vue') },
        { path: 'points', name: 'MyPoints', component: () => import('../components/student/MyPoints.vue') },
        // 👇 新增的：学生我的上传/分享页面
        { path: 'uploads', name: 'StudentUploads', component: () => import('../components/student/MyUpload.vue') },
        { path: '', redirect: '/student/forum' }
      ]
    },
    {
      path: '/teacher',
      name: 'Teacher',
      component: TeacherLayout,
      children: [
        { path: 'personal', name: 'TeacherPersonal', component: () => import('../components/teacher/PersonalCenter.vue') },
        { path: 'courses', name: 'TeacherCourseManagement', component: () => import('../components/teacher/CourseResourceManagement.vue') },
        { path: 'comments', name: 'CourseResourceComments', component: () => import('../components/teacher/CourseResourceComments.vue') },
        { path: 'announcements', name: 'TeacherAnnouncements', component: StudentAnnouncements },
        { path: 'announcements/:id', name: 'TeacherAnnouncementDetail', component: () => import('../components/student/AnnouncementDetail.vue') },
        { path: 'forum', name: 'TeacherForum', component: StudentForum },
        { path: 'forum/:id', name: 'TeacherPostDetail', component: () => import('../components/student/PostDetail.vue') },
        { path: 'students', name: 'TeacherStudentManagement', component: () => import('../components/teacher/StudentManagement.vue') },
        { path: '', redirect: '/teacher/personal' },
        { path: 'ai', name: 'TeacherAI', component: () => import('../components/teacher/AITeacherInsight.vue') }
      ]
    },
    {
      path: '/',
      redirect: '/login'
    }
  ]
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  if (to.path === '/login') return next()
  if (!token) return next('/login')

  if (to.path.startsWith('/admin') && user.role !== 'admin') return next('/login')
  if (to.path.startsWith('/teacher') && user.role !== 'teacher') return next('/login')
  if (to.path.startsWith('/student') && user.role !== 'student') return next('/login')

  next()
})

export default router