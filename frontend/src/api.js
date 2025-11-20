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

  // Expenses
  getExpenses() {
    return api.get('/expenses')
  },
  getExpense(id) {
    return api.get(`/expenses/${id}`)
  },
  createExpense(data) {
    return api.post('/expenses', data)
  },
  updateExpense(id, data) {
    return api.put(`/expenses/${id}`, data)
  },
  deleteExpense(id) {
    return api.delete(`/expenses/${id}`)
  },

  // Statistics
  getSummaryStatistics() {
    return api.get('/statistics/summary')
  },
  getCategoryStatistics() {
    return api.get('/statistics/by-category')
  }
}
