'use client'

import { useState } from 'react'

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Front-end only, no backend
    alert('Thank you for your message! (This is a demo form - no data is being sent)')
    setFormData({ name: '', email: '', message: '' })
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
      <div className="space-y-6">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-text-main mb-2">
            Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-text-main/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-text-main mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-text-main/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
          />
        </div>
        <div>
          <label htmlFor="message" className="block text-sm font-medium text-text-main mb-2">
            Message
          </label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            required
            rows={6}
            className="w-full px-4 py-2 border border-text-main/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white resize-none"
          />
        </div>
        <button
          type="submit"
          className="w-full px-8 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary/90 transition-colors cursor-pointer"
        >
          Send Message
        </button>
      </div>
    </form>
  )
}

