import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token de autenticación
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => Promise.reject(error))

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authService = {
  preLogin(email) {
    return api.post('/auth/pre-login', { email })
  },
  login(email, authHash) {
    return api.post('/auth/login', { email, auth_hash: authHash })
  }
}

export const secretsService = {
  list(filters = {}) {
    return api.get('/secrets', { params: filters })
  },
  get(id) {
    return api.get(`/secrets/${id}`)
  },
  create(secret) {
    return api.post('/secrets', secret)
  },
  update(id, secret) {
    return api.put(`/secrets/${id}`, secret)
  },
  delete(id) {
    return api.delete(`/secrets/${id}`)
  },
  toggleFavorite(id) {
    return api.post(`/secrets/${id}/favorite`)
  }
}

export const usersService = {
  getCurrentUser() {
    return api.get('/users/me')
  },
  updateCurrentUser(data) {
    return api.put('/users/me', data)
  },
  changePassword(authHash) {
    return api.post('/users/change-password', { auth_hash: authHash })
  }
}

export const adminService = {
  listUsers() {
    return api.get('/admin/users')
  },
  getUser(id) {
    return api.get(`/admin/users/${id}`)
  },
  createUser(user) {
    return api.post('/admin/users', user)
  },
  updateUser(id, user) {
    return api.put(`/admin/users/${id}`, user)
  },
  deleteUser(id) {
    return api.delete(`/admin/users/${id}`)
  }
}

export default api
