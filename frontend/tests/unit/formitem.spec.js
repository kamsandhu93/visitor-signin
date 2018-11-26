import '@/plugins/element.js'
import { shallowMount } from '@vue/test-utils'
import FormItem from '@/components/common/FormItem.vue'

describe('FormItem.vue', () => {
    it('test props being passed correctly', () => {
        const label = 'new message'
        const wrapper = shallowMount(FormItem, {
            propsData: { label }
        })
        console.log(wrapper)
        expect(wrapper.text()).toMatch(label)
    })

    it('test v-model of input field', () => {
        const wrapper = shallowMount(FormItem)
        wrapper.setData({ body: 'input text' })
        expect(wrapper.find('v-model').exists()).toBe(true)
    })
})
