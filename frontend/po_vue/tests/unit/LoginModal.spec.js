import { shallowMount } from '@vue/test-utils'
import axios from 'axios'
import LoginModal from '@/components/LoginModal.vue'

jest.mock('axios')

describe('LoginModal', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(LoginModal)
  })

  describe('validInputEmail', () => {
    it('returns true for valid email', () => {
      expect(wrapper.vm.validInputEmail('test@example.com')).toBe(true)
    })

    it('returns false for invalid email', () => {
      expect(wrapper.vm.validInputEmail('invalid-email')).toBe(false)
    })
  })

  describe('resetPassword', () => {
    it('shows error message for invalid email', async () => {
      wrapper.setData({ resetEmail: 'invalid-email' })
      await wrapper.vm.resetPassword()
      expect(wrapper.vm.errorMsg).toBe('Please enter a valid email.')
    })

    it('calls API and shows success message for valid email', async () => {
      const mockResponse = { data: { message: 'An email has been send to your email address.' } }
      axios.post.mockResolvedValue(mockResponse)

      wrapper.setData({ resetEmail: 'valid@email.com' })
      await wrapper.vm.resetPassword()

      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8020/auth/password-reset/',
        { email: 'valid@email.com' }
      )
      expect(wrapper.vm.successMsg).toBe('An email has been send to your email address.')
    })

    it('handles API error', async () => {
      const mockError = { response: { data: { message: 'An error occurred during reset.' } } }
      axios.post.mockRejectedValue(mockError)

      wrapper.setData({ resetEmail: 'valid@email.com' })
      await wrapper.vm.resetPassword()

      expect(wrapper.vm.errorMsg).toBe('An error occurred during reset.')
    })
  })
})
