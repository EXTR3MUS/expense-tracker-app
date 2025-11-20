import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Categories
  getCategories() {
    return api.get('/categories')
  },
  getCategory(id) {
    return api.get(`/categories/${id}`)
  },
  createCategory(data) {
    return api.post('/categories', data)
  },
  updateCategory(id, data) {
    return api.put(`/categories/${id}`, data)
  },
  deleteCategory(id) {
    return api.delete(`/categories/${id}`)
  },

  // Transactions
  getTransactions() {
    return api.get('/transactions')
  },
  getTransaction(id) {
    return api.get(`/transactions/${id}`)
  },
  createTransaction(data) {
    return api.post('/transactions', data)
  },
  updateTransaction(id, data) {
    return api.put(`/transactions/${id}`, data)
  },
  deleteTransaction(id) {
    return api.delete(`/transactions/${id}`)
  },

  // Statistics
  getMonthlyStatistics() {
    return api.get('/statistics/monthly')
  },
  getBudget() {
    return api.get('/statistics/budget')
  },
  getCategoryStatistics() {
    return api.get('/statistics/by-category')
  },

  // Audit Logs
  getAuditLogs() {
    return api.get('/audit-logs')
  }
}
